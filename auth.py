"""
Authentication module for SweetGF
Handles user registration, login, and session management
"""

import bcrypt
import secrets
import database as db
from functools import wraps
from flask import request, jsonify, session

# Session secret key - should be in environment variable in production
SECRET_KEY = secrets.token_hex(32)

# Password requirements
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def validate_username(username):
    """Validate username format"""
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 20:
        return False, "Username must be less than 20 characters"
    
    if not username.isalnum() and '_' not in username:
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, None

def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    if '@' not in email or '.' not in email:
        return False, "Invalid email format"
    
    if len(email) > 100:
        return False, "Email is too long"
    
    return True, None

def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
    
    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password must be less than {MAX_PASSWORD_LENGTH} characters"
    
    # Check for at least one number
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"
    
    # Check for at least one letter
    if not any(char.isalpha() for char in password):
        return False, "Password must contain at least one letter"
    
    return True, None

def register_user(username, email, password):
    """Register a new user"""
    # Validate username
    valid, error = validate_username(username)
    if not valid:
        return False, error
    
    # Validate email
    valid, error = validate_email(email)
    if not valid:
        return False, error
    
    # Validate password
    valid, error = validate_password(password)
    if not valid:
        return False, error
    
    # Check if username exists
    if db.get_user_by_username(username):
        return False, "Username already exists"
    
    # Check if email exists
    if db.get_user_by_email(email):
        return False, "Email already exists"
    
    # Hash password
    password_hash = hash_password(password)
    
    # Create user
    user_id = db.create_user(username, email, password_hash)
    
    if user_id:
        return True, {"user_id": user_id, "username": username}
    else:
        return False, "Failed to create user"

def login_user(username_or_email, password):
    """Login a user"""
    # Try to find user by username or email
    user = db.get_user_by_username(username_or_email)
    if not user:
        user = db.get_user_by_email(username_or_email)
    
    if not user:
        return False, "Invalid username or password"
    
    # Check if user is active
    if not user['is_active']:
        return False, "Account is deactivated"
    
    # Verify password
    if not verify_password(password, user['password_hash']):
        return False, "Invalid username or password"
    
    # Update last login
    db.update_last_login(user['id'])
    
    # Return user data (without password hash)
    user_data = {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'is_admin': user['is_admin'],
        'subscription_tier': user['subscription_tier']
    }
    
    return True, user_data

def generate_session_token():
    """Generate a secure session token"""
    return secrets.token_urlsafe(32)

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for session token in request
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            auth_token = request.json.get('auth_token') if request.json else None
        
        if not auth_token:
            return jsonify({"error": "Authentication required"}), 401
        
        # Verify token (in production, use JWT or similar)
        # For now, we'll use a simple session-based approach
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Invalid or expired session"}), 401
        
        # Get user
        user = db.get_user_by_id(user_id)
        if not user or not user['is_active']:
            return jsonify({"error": "User not found or inactive"}), 401
        
        # Add user to request context
        request.user = user
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_admin(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check authentication
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            auth_token = request.json.get('auth_token') if request.json else None
        
        if not auth_token:
            return jsonify({"error": "Authentication required"}), 401
        
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Invalid or expired session"}), 401
        
        # Get user
        user = db.get_user_by_id(user_id)
        if not user or not user['is_active']:
            return jsonify({"error": "User not found or inactive"}), 401
        
        # Check if admin
        if not user['is_admin']:
            return jsonify({"error": "Admin privileges required"}), 403
        
        # Add user to request context
        request.user = user
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get currently logged in user"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    
    return db.get_user_by_id(user_id)

def logout_user():
    """Logout current user"""
    session.clear()
    return True
