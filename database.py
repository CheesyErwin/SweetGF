"""
Database module for SweetGF
Handles all persistent storage using SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import threading

# Database file location
DB_PATH = Path(__file__).parent / 'sweetgf.db'

# Thread-local storage for database connections
_thread_local = threading.local()

def get_db():
    """Get thread-local database connection"""
    if not hasattr(_thread_local, 'connection'):
        _thread_local.connection = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        _thread_local.connection.row_factory = sqlite3.Row
    return _thread_local.connection

def init_database():
    """Initialize database with all required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table - authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            subscription_tier TEXT DEFAULT 'free',
            subscription_expires TIMESTAMP
        )
    ''')
    
    # Sessions table - core session data (now linked to users)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            language TEXT DEFAULT 'en',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Girlfriends table - girlfriend configuration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS girlfriends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            preset TEXT,
            personality TEXT,
            appearance TEXT,
            reference_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
        )
    ''')
    
    # Affection table - affection and intimacy data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS affection (
            session_id TEXT PRIMARY KEY,
            affection_points INTEGER DEFAULT 0,
            intimacy_tokens INTEGER DEFAULT 0,
            unlocked_intimacy TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
        )
    ''')
    
    # Pictures table - picture unlock tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pictures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            picture_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            level TEXT NOT NULL,
            is_unlocked BOOLEAN DEFAULT 0,
            unlocked_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(session_id, picture_id),
            FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
        )
    ''')
    
    # Gallery settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery_settings (
            session_id TEXT PRIMARY KEY,
            gallery_limit INTEGER DEFAULT 6,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
        )
    ''')
    
    # Conversations table - chat history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pictures_session ON pictures(session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pictures_unlocked ON pictures(session_id, is_unlocked)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)')
    
    conn.commit()
    print("[Database] Initialized successfully")

# ============================================================================
# USER MANAGEMENT
# ============================================================================

def create_user(username, email, password_hash, is_admin=False):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, is_admin)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, is_admin))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None  # Username or email already exists

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    
    return dict(row) if row else None

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    
    return dict(row) if row else None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    
    return dict(row) if row else None

def update_last_login(user_id):
    """Update user's last login timestamp"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET last_login = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (user_id,))
    
    conn.commit()

def update_user_subscription(user_id, tier, expires_at=None):
    """Update user's subscription"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users
        SET subscription_tier = ?, subscription_expires = ?
        WHERE id = ?
    ''', (tier, expires_at, user_id))
    
    conn.commit()

def deactivate_user(user_id):
    """Deactivate a user account"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
    conn.commit()

def activate_user(user_id):
    """Activate a user account"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET is_active = 1 WHERE id = ?', (user_id,))
    conn.commit()

def get_all_users(limit=100, offset=0):
    """Get all users (for admin)"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, is_admin, is_active, created_at, last_login, subscription_tier
        FROM users
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    
    return [dict(row) for row in cursor.fetchall()]

def get_user_count():
    """Get total user count"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM users')
    return cursor.fetchone()['count']

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def create_session(session_id, user_id=None, language='en'):
    """Create a new session"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO sessions (session_id, user_id, language)
        VALUES (?, ?, ?)
    ''', (session_id, user_id, language))
    
    conn.commit()
    return session_id

def update_session_activity(session_id):
    """Update last active timestamp for session"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE sessions 
        SET last_active = CURRENT_TIMESTAMP
        WHERE session_id = ?
    ''', (session_id,))
    
    conn.commit()

def get_session(session_id):
    """Get session data"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
    row = cursor.fetchone()
    
    return dict(row) if row else None

# ============================================================================
# GIRLFRIEND MANAGEMENT
# ============================================================================

def save_girlfriend(session_id, name, preset=None, personality=None, appearance=None, reference_image=None):
    """Save or update girlfriend data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure session exists
    create_session(session_id)
    
    cursor.execute('''
        INSERT INTO girlfriends (session_id, name, preset, personality, appearance, reference_image)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            name = excluded.name,
            preset = excluded.preset,
            personality = excluded.personality,
            appearance = excluded.appearance,
            reference_image = excluded.reference_image
    ''', (session_id, name, preset, personality, appearance, reference_image))
    
    conn.commit()

def get_girlfriend(session_id):
    """Get girlfriend data"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM girlfriends WHERE session_id = ?', (session_id,))
    row = cursor.fetchone()
    
    return dict(row) if row else None


def get_user_girlfriends(user_id):
    """Get all girlfriends for a user"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            g.*,
            s.last_active,
            a.affection_points,
            a.intimacy_tokens
        FROM girlfriends g
        JOIN sessions s ON g.session_id = s.session_id
        LEFT JOIN affection a ON g.session_id = a.session_id
        WHERE s.user_id = ?
        ORDER BY s.last_active DESC
    ''', (user_id,))
    
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def delete_girlfriend(session_id):
    """Delete girlfriend data"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM girlfriends WHERE session_id = ?', (session_id,))
    conn.commit()

# ============================================================================
# AFFECTION & TOKENS
# ============================================================================

def get_affection(session_id):
    """Get affection data for session"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM affection WHERE session_id = ?', (session_id,))
    row = cursor.fetchone()
    
    if row:
        data = dict(row)
        data['unlocked_intimacy'] = json.loads(data['unlocked_intimacy'])
        return data
    
    # Return defaults if not found
    return {
        'session_id': session_id,
        'affection_points': 0,
        'intimacy_tokens': 0,
        'unlocked_intimacy': []
    }

def update_affection(session_id, affection_points=None, intimacy_tokens=None, unlocked_intimacy=None):
    """Update affection data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure session exists
    create_session(session_id)
    
    # Get current data
    current = get_affection(session_id)
    
    # Update values
    if affection_points is not None:
        current['affection_points'] = affection_points
    if intimacy_tokens is not None:
        current['intimacy_tokens'] = intimacy_tokens
    if unlocked_intimacy is not None:
        current['unlocked_intimacy'] = unlocked_intimacy
    
    # Convert list to JSON
    unlocked_json = json.dumps(current['unlocked_intimacy'])
    
    cursor.execute('''
        INSERT INTO affection (session_id, affection_points, intimacy_tokens, unlocked_intimacy)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            affection_points = excluded.affection_points,
            intimacy_tokens = excluded.intimacy_tokens,
            unlocked_intimacy = excluded.unlocked_intimacy,
            updated_at = CURRENT_TIMESTAMP
    ''', (session_id, current['affection_points'], current['intimacy_tokens'], unlocked_json))
    
    conn.commit()

def add_affection_points(session_id, points):
    """Add affection points"""
    current = get_affection(session_id)
    new_points = current['affection_points'] + points
    update_affection(session_id, affection_points=new_points)
    return new_points

def add_intimacy_tokens(session_id, tokens):
    """Add intimacy tokens"""
    current = get_affection(session_id)
    new_tokens = current['intimacy_tokens'] + tokens
    update_affection(session_id, intimacy_tokens=new_tokens)
    return new_tokens

def unlock_intimacy_level(session_id, level):
    """Unlock an intimacy level"""
    current = get_affection(session_id)
    unlocked = current['unlocked_intimacy']
    
    if level not in unlocked:
        unlocked.append(level)
        update_affection(session_id, unlocked_intimacy=unlocked)
    
    return unlocked

# ============================================================================
# PICTURE MANAGEMENT
# ============================================================================

def save_picture(session_id, picture_id, filename, level):
    """Save picture metadata"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure session exists
    create_session(session_id)
    
    cursor.execute('''
        INSERT OR IGNORE INTO pictures (session_id, picture_id, filename, level)
        VALUES (?, ?, ?, ?)
    ''', (session_id, picture_id, filename, level))
    
    conn.commit()

def unlock_picture(session_id, picture_id):
    """Unlock a picture"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE pictures
        SET is_unlocked = 1, unlocked_at = CURRENT_TIMESTAMP
        WHERE session_id = ? AND picture_id = ?
    ''', (session_id, picture_id))
    
    conn.commit()
    return cursor.rowcount > 0

def is_picture_unlocked(session_id, picture_id):
    """Check if picture is unlocked"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT is_unlocked FROM pictures
        WHERE session_id = ? AND picture_id = ?
    ''', (session_id, picture_id))
    
    row = cursor.fetchone()
    return bool(row['is_unlocked']) if row else False

def get_unlocked_pictures(session_id):
    """Get all unlocked picture IDs for session"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT picture_id FROM pictures
        WHERE session_id = ? AND is_unlocked = 1
    ''', (session_id,))
    
    return [row['picture_id'] for row in cursor.fetchall()]

def get_all_pictures(session_id):
    """Get all pictures for session"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM pictures
        WHERE session_id = ?
        ORDER BY created_at DESC
    ''', (session_id,))
    
    return [dict(row) for row in cursor.fetchall()]

# ============================================================================
# GALLERY SETTINGS
# ============================================================================

def get_gallery_limit(session_id):
    """Get gallery limit for session"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT gallery_limit FROM gallery_settings WHERE session_id = ?', (session_id,))
    row = cursor.fetchone()
    
    return row['gallery_limit'] if row else 6  # Default 6

def update_gallery_limit(session_id, new_limit):
    """Update gallery limit"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure session exists
    create_session(session_id)
    
    cursor.execute('''
        INSERT INTO gallery_settings (session_id, gallery_limit)
        VALUES (?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            gallery_limit = excluded.gallery_limit,
            updated_at = CURRENT_TIMESTAMP
    ''', (session_id, new_limit))
    
    conn.commit()

# ============================================================================
# CONVERSATION MANAGEMENT
# ============================================================================

def save_message(session_id, role, content):
    """Save a conversation message"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure session exists
    create_session(session_id)
    
    cursor.execute('''
        INSERT INTO conversations (session_id, role, content)
        VALUES (?, ?, ?)
    ''', (session_id, role, content))
    
    conn.commit()

def get_conversation(session_id, limit=None):
    """Get conversation history"""
    conn = get_db()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute('''
            SELECT role, content, timestamp FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
    else:
        cursor.execute('''
            SELECT role, content, timestamp FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp ASC
        ''', (session_id,))
    
    messages = []
    for row in cursor.fetchall():
        messages.append({
            'role': row['role'],
            'content': row['content'],
            'timestamp': row['timestamp']
        })
    
    return messages

def clear_conversation(session_id):
    """Clear conversation history"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
    conn.commit()

# ============================================================================
# CLEANUP & MAINTENANCE
# ============================================================================

def delete_session(session_id):
    """Delete entire session and all related data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # CASCADE will handle related tables
    cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    conn.commit()

def get_session_stats(session_id):
    """Get statistics for a session (counts only, no private data)"""
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {}
    
    # Message count (no content)
    cursor.execute('SELECT COUNT(*) as count FROM conversations WHERE session_id = ?', (session_id,))
    stats['message_count'] = cursor.fetchone()['count']
    
    # Picture count (no images)
    cursor.execute('SELECT COUNT(*) as count FROM pictures WHERE session_id = ?', (session_id,))
    stats['total_pictures'] = cursor.fetchone()['count']
    
    # Unlocked pictures count (no images)
    cursor.execute('SELECT COUNT(*) as count FROM pictures WHERE session_id = ? AND is_unlocked = 1', (session_id,))
    stats['unlocked_pictures'] = cursor.fetchone()['count']
    
    # Affection data
    affection = get_affection(session_id)
    stats['affection_points'] = affection['affection_points']
    stats['intimacy_tokens'] = affection['intimacy_tokens']
    
    return stats

def get_user_stats_for_admin(user_id):
    """Get user statistics for admin (no private data)"""
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {}
    
    # Get all sessions for this user
    cursor.execute('SELECT session_id FROM sessions WHERE user_id = ?', (user_id,))
    sessions = [row['session_id'] for row in cursor.fetchall()]
    
    # Total messages across all sessions
    cursor.execute('''
        SELECT COUNT(*) as count FROM conversations 
        WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)
    ''', (user_id,))
    stats['total_messages'] = cursor.fetchone()['count']
    
    # Total pictures
    cursor.execute('''
        SELECT COUNT(*) as count FROM pictures 
        WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)
    ''', (user_id,))
    stats['total_pictures'] = cursor.fetchone()['count']
    
    # Unlocked pictures
    cursor.execute('''
        SELECT COUNT(*) as count FROM pictures 
        WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)
        AND is_unlocked = 1
    ''', (user_id,))
    stats['unlocked_pictures'] = cursor.fetchone()['count']
    
    # Total tokens earned
    cursor.execute('''
        SELECT SUM(intimacy_tokens) as total FROM affection 
        WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)
    ''', (user_id,))
    result = cursor.fetchone()
    stats['total_tokens_earned'] = result['total'] if result['total'] else 0
    
    # Current tokens (sum across all sessions)
    cursor.execute('''
        SELECT SUM(intimacy_tokens) as current FROM affection 
        WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)
    ''', (user_id,))
    result = cursor.fetchone()
    stats['current_tokens'] = result['current'] if result['current'] else 0
    
    # Tokens spent (earned - current)
    stats['tokens_spent'] = stats['total_tokens_earned'] - stats['current_tokens']
    
    # Number of girlfriends
    cursor.execute('''
        SELECT COUNT(*) as count FROM girlfriends 
        WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)
    ''', (user_id,))
    stats['girlfriend_count'] = cursor.fetchone()['count']
    
    return stats

def cleanup_old_sessions(days=30):
    """Delete sessions inactive for specified days"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM sessions
        WHERE last_active < datetime('now', '-' || ? || ' days')
    ''', (days,))
    
    deleted = cursor.rowcount
    conn.commit()
    
    return deleted


def test_connection():
    """Test database connection and return status"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sessions")
        session_count = cursor.fetchone()[0]
        
        return {
            'connected': True,
            'db_path': str(DB_PATH),
            'db_exists': DB_PATH.exists(),
            'user_count': user_count,
            'session_count': session_count
        }
    except Exception as e:
        return {
            'connected': False,
            'error': str(e),
            'db_path': str(DB_PATH),
            'db_exists': DB_PATH.exists()
        }


# Initialize database on module import
init_database()
