"""
Authentication and Admin API routes
"""

from flask import Blueprint, request, jsonify, session
import auth
import database as db

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400
        
        # Register user
        success, result = auth.register_user(username, email, password)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "User registered successfully",
                "user": result
            }), 201
        else:
            return jsonify({"error": result}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a regular user (non-admin)"""
    try:
        data = request.json
        username_or_email = data.get('username') or data.get('email')
        password = data.get('password')
        
        if not username_or_email or not password:
            return jsonify({"error": "Username/email and password are required"}), 400
        
        # Login user
        success, result = auth.login_user(username_or_email, password)
        
        if success:
            # Check if user is admin - admins should use admin login
            if result['is_admin']:
                return jsonify({"error": "Admin users must use the admin login page"}), 403
            
            # Set session
            session['user_id'] = result['id']
            session['username'] = result['username']
            session['is_admin'] = result['is_admin']
            
            # Generate session token
            session_token = auth.generate_session_token()
            
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "user": result,
                "session_token": session_token
            })
        else:
            return jsonify({"error": result}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    """Login for admin users only"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        # Login user
        success, result = auth.login_user(username, password)
        
        if success:
            # Check if user is admin
            if not result['is_admin']:
                return jsonify({"error": "Access denied: Admin privileges required"}), 403
            
            # Set session
            session['user_id'] = result['id']
            session['username'] = result['username']
            session['is_admin'] = result['is_admin']
            
            # Generate session token
            session_token = auth.generate_session_token()
            
            return jsonify({
                "status": "success",
                "message": "Admin login successful",
                "user": result,
                "session_token": session_token
            })
        else:
            return jsonify({"error": result}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout current user"""
    try:
        auth.logout_user()
        return jsonify({
            "status": "success",
            "message": "Logged out successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@auth.require_auth
def get_current_user():
    """Get current user info"""
    try:
        user = request.user
        
        # Remove sensitive data
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'is_admin': user['is_admin'],
            'subscription_tier': user['subscription_tier'],
            'created_at': user['created_at'],
            'last_login': user['last_login']
        }
        
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    user = auth.get_current_user()
    
    if user:
        return jsonify({
            "authenticated": True,
            "user": {
                'id': user['id'],
                'username': user['username'],
                'is_admin': user['is_admin']
            }
        })
    else:
        return jsonify({"authenticated": False})


# ============================================================================
# ADMIN ROUTES
# ============================================================================

@admin_bp.route('/users', methods=['GET'])
@auth.require_admin
def get_users():
    """Get all users (admin only)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        offset = (page - 1) * per_page
        
        users = db.get_all_users(limit=per_page, offset=offset)
        total_users = db.get_user_count()
        
        return jsonify({
            "users": users,
            "total": total_users,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_users + per_page - 1) // per_page
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@auth.require_admin
def get_user(user_id):
    """Get specific user details (admin only) - NO PRIVATE DATA"""
    try:
        user = db.get_user_by_id(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get user stats (counts and tokens only, no private content)
        stats = db.get_user_stats_for_admin(user_id)
        
        # Remove password hash and return only non-private data
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'is_admin': user['is_admin'],
            'is_active': user['is_active'],
            'created_at': user['created_at'],
            'last_login': user['last_login'],
            'subscription_tier': user['subscription_tier'],
            'subscription_expires': user['subscription_expires'],
            'stats': stats
        }
        
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@auth.require_admin
def deactivate_user(user_id):
    """Deactivate a user (admin only)"""
    try:
        # Don't allow deactivating yourself
        if user_id == request.user['id']:
            return jsonify({"error": "Cannot deactivate your own account"}), 400
        
        db.deactivate_user(user_id)
        
        return jsonify({
            "status": "success",
            "message": "User deactivated"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@auth.require_admin
def activate_user(user_id):
    """Activate a user (admin only)"""
    try:
        db.activate_user(user_id)
        
        return jsonify({
            "status": "success",
            "message": "User activated"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/users/<int:user_id>/subscription', methods=['PUT'])
@auth.require_admin
def update_subscription(user_id):
    """Update user subscription (admin only)"""
    try:
        data = request.json
        tier = data.get('tier')
        expires_at = data.get('expires_at')
        
        if not tier:
            return jsonify({"error": "Subscription tier is required"}), 400
        
        db.update_user_subscription(user_id, tier, expires_at)
        
        return jsonify({
            "status": "success",
            "message": "Subscription updated"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/stats', methods=['GET'])
@auth.require_admin
def get_admin_stats():
    """Get admin dashboard statistics"""
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) as count FROM users')
        total_users = cursor.fetchone()['count']
        
        # Active users (logged in last 7 days)
        cursor.execute('''
            SELECT COUNT(*) as count FROM users
            WHERE last_login > datetime('now', '-7 days')
        ''')
        active_users = cursor.fetchone()['count']
        
        # Total sessions
        cursor.execute('SELECT COUNT(*) as count FROM sessions')
        total_sessions = cursor.fetchone()['count']
        
        # Total messages
        cursor.execute('SELECT COUNT(*) as count FROM conversations')
        total_messages = cursor.fetchone()['count']
        
        # Total pictures
        cursor.execute('SELECT COUNT(*) as count FROM pictures')
        total_pictures = cursor.fetchone()['count']
        
        # Unlocked pictures
        cursor.execute('SELECT COUNT(*) as count FROM pictures WHERE is_unlocked = 1')
        unlocked_pictures = cursor.fetchone()['count']
        
        # New users today
        cursor.execute('''
            SELECT COUNT(*) as count FROM users
            WHERE DATE(created_at) = DATE('now')
        ''')
        new_users_today = cursor.fetchone()['count']
        
        # Subscription breakdown
        cursor.execute('''
            SELECT subscription_tier, COUNT(*) as count
            FROM users
            GROUP BY subscription_tier
        ''')
        subscription_breakdown = {row['subscription_tier']: row['count'] for row in cursor.fetchall()}
        
        return jsonify({
            "total_users": total_users,
            "active_users": active_users,
            "new_users_today": new_users_today,
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "total_pictures": total_pictures,
            "unlocked_pictures": unlocked_pictures,
            "subscription_breakdown": subscription_breakdown
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/cleanup', methods=['POST'])
@auth.require_admin
def cleanup_old_data():
    """Cleanup old inactive sessions (admin only)"""
    try:
        data = request.json
        days = data.get('days', 30)
        
        deleted = db.cleanup_old_sessions(days)
        
        return jsonify({
            "status": "success",
            "message": f"Deleted {deleted} inactive sessions",
            "deleted_sessions": deleted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/env-settings', methods=['GET'])
@auth.require_admin
def get_env_settings():
    """Get environment settings from .env file (admin only)"""
    try:
        import os
        from dotenv import dotenv_values
        
        # Load .env file
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if not os.path.exists(env_path):
            # Try .env.example as fallback
            env_path = os.path.join(os.path.dirname(__file__), '.env.example')
        
        env_values = dotenv_values(env_path)
        
        # Return relevant settings
        return jsonify({
            # Image generation settings
            "COMFYUI_CHECKPOINT": env_values.get('COMFYUI_CHECKPOINT', 'waiNSFWIllustrious_v110.safetensors'),
            "IMAGE_GENERATION_STEPS": env_values.get('IMAGE_GENERATION_STEPS', '20'),
            "ENABLE_LORA": env_values.get('ENABLE_LORA', 'true'),
            "COMFYUI_LORA": env_values.get('COMFYUI_LORA', 'Better_detailed_pussy_and_anus_v3.0.safetensors'),
            "COMFYUI_LORA_STRENGTH": env_values.get('COMFYUI_LORA_STRENGTH', '0.7'),
            "ENABLE_FACE_DETAILER": env_values.get('ENABLE_FACE_DETAILER', 'true'),
            "FACEDETAILER_STEPS": env_values.get('FACEDETAILER_STEPS', '20'),
            "FACEDETAILER_DENOISE": env_values.get('FACEDETAILER_DENOISE', '0.4'),
            "ENABLE_UPSCALE": env_values.get('ENABLE_UPSCALE', 'true'),
            "IMAGE_GENERATION_TIMEOUT": env_values.get('IMAGE_GENERATION_TIMEOUT', '600'),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/env-settings', methods=['POST'])
@auth.require_admin
def update_env_settings():
    """Update environment settings in .env file (admin only)"""
    try:
        import os
        
        data = request.json
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({"error": "Key is required"}), 400
        
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        
        # If .env doesn't exist, create it from .env.example
        if not os.path.exists(env_path):
            example_path = os.path.join(os.path.dirname(__file__), '.env.example')
            if os.path.exists(example_path):
                import shutil
                shutil.copy(example_path, env_path)
        
        # Read current .env file
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Update or add the key
        key_found = False
        new_lines = []
        
        for line in lines:
            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                new_lines.append(line)
                continue
            
            # Check if this line contains our key
            if '=' in line:
                line_key = line.split('=')[0].strip()
                if line_key == key:
                    new_lines.append(f"{key}={value}\n")
                    key_found = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # If key wasn't found, add it at the end
        if not key_found:
            new_lines.append(f"\n# Added by admin panel\n{key}={value}\n")
        
        # Write back to .env file
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return jsonify({
            "status": "success",
            "message": f"Setting {key} updated to {value}",
            "restart_required": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
