# Database Integration Guide

## Overview

Migration from in-memory dictionaries to SQLite database for persistent storage.

---

## Database Schema

### Tables:

1. **sessions** - Core session tracking
2. **girlfriends** - Girlfriend configuration
3. **affection** - Affection points and tokens
4. **pictures** - Picture unlock tracking
5. **gallery_settings** - Gallery size limits
6. **conversations** - Chat history

---

## Migration Steps

### 1. Import Database Module

```python
# At top of app.py
import database as db
```

### 2. Replace In-Memory Dictionaries

**OLD (In-Memory):**
```python
affection_levels = {}  # {session_id: int}
intimacy_tokens = {}   # {session_id: int}
unlocked_intimacy = {} # {session_id: set()}
girlfriend_names = {}  # {session_id: str}
conversations = {}     # {session_id: list}
unlocked_pictures = {} # {session_id: set()}
gallery_limits = {}    # {session_id: int}
```

**NEW (Database):**
```python
# No global dictionaries needed!
# All data accessed through db module
```

---

## Code Examples

### Affection Management

**OLD:**
```python
# Get affection
current_affection = affection_levels.get(session_id, 0)

# Add affection
affection_levels[session_id] = affection_levels.get(session_id, 0) + points

# Get tokens
current_tokens = intimacy_tokens.get(session_id, 0)
```

**NEW:**
```python
# Get affection
affection_data = db.get_affection(session_id)
current_affection = affection_data['affection_points']

# Add affection
new_affection = db.add_affection_points(session_id, points)

# Get tokens
affection_data = db.get_affection(session_id)
current_tokens = affection_data['intimacy_tokens']
```

---

### Girlfriend Management

**OLD:**
```python
# Save girlfriend
girlfriend_names[session_id] = name
# Save to JSON file...

# Get girlfriend
name = girlfriend_names.get(session_id, 'Luna')
```

**NEW:**
```python
# Save girlfriend
db.save_girlfriend(
    session_id=session_id,
    name=name,
    preset=preset,
    personality=personality,
    appearance=appearance,
    reference_image=reference_image
)

# Get girlfriend
gf_data = db.get_girlfriend(session_id)
name = gf_data['name'] if gf_data else 'Luna'
```

---

### Picture Management

**OLD:**
```python
# Check if unlocked
if session_id not in unlocked_pictures:
    unlocked_pictures[session_id] = set()
is_unlocked = picture_id in unlocked_pictures[session_id]

# Unlock picture
unlocked_pictures[session_id].add(picture_id)
```

**NEW:**
```python
# Check if unlocked
is_unlocked = db.is_picture_unlocked(session_id, picture_id)

# Unlock picture
db.unlock_picture(session_id, picture_id)

# Get all unlocked
unlocked_list = db.get_unlocked_pictures(session_id)
```

---

### Conversation Management

**OLD:**
```python
# Initialize conversation
if session_id not in conversations:
    conversations[session_id] = []

# Add message
conversations[session_id].append({
    'role': 'user',
    'content': message
})

# Get conversation
messages = conversations.get(session_id, [])
```

**NEW:**
```python
# Add message
db.save_message(session_id, 'user', message)
db.save_message(session_id, 'assistant', response)

# Get conversation
messages = db.get_conversation(session_id)

# Clear conversation
db.clear_conversation(session_id)
```

---

### Gallery Management

**OLD:**
```python
# Get gallery limit
limit = gallery_limits.get(session_id, 6)

# Expand gallery
gallery_limits[session_id] = limit + slots
```

**NEW:**
```python
# Get gallery limit
limit = db.get_gallery_limit(session_id)

# Expand gallery
db.update_gallery_limit(session_id, limit + slots)
```

---

## Complete Example: Chat Endpoint

**OLD:**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    user_message = data.get('message')
    
    # Get affection
    current_affection = affection_levels.get(session_id, 0)
    
    # Add affection
    affection_gain = calculate_affection_gain(user_message)
    affection_levels[session_id] = current_affection + affection_gain
    
    # Get conversation
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add message
    conversations[session_id].append({
        'role': 'user',
        'content': user_message
    })
    
    # ... AI response logic ...
    
    return jsonify({
        'response': ai_response,
        'affection': affection_levels[session_id]
    })
```

**NEW:**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    user_message = data.get('message')
    
    # Update session activity
    db.update_session_activity(session_id)
    
    # Get affection
    affection_data = db.get_affection(session_id)
    current_affection = affection_data['affection_points']
    
    # Add affection
    affection_gain = calculate_affection_gain(user_message)
    new_affection = db.add_affection_points(session_id, affection_gain)
    
    # Save user message
    db.save_message(session_id, 'user', user_message)
    
    # Get conversation history
    conversation = db.get_conversation(session_id)
    
    # ... AI response logic ...
    
    # Save AI response
    db.save_message(session_id, 'assistant', ai_response)
    
    return jsonify({
        'response': ai_response,
        'affection': new_affection
    })
```

---

## Complete Example: Unlock Picture

**OLD:**
```python
@app.route('/api/unlock-picture', methods=['POST'])
def unlock_picture():
    data = request.json
    session_id = data.get('session_id')
    picture_id = data.get('picture_id')
    
    # Check tokens
    current_tokens = intimacy_tokens.get(session_id, 0)
    cost = 10
    
    if current_tokens < cost:
        return jsonify({'error': 'Not enough tokens'}), 400
    
    # Deduct tokens
    intimacy_tokens[session_id] -= cost
    
    # Unlock picture
    if session_id not in unlocked_pictures:
        unlocked_pictures[session_id] = set()
    unlocked_pictures[session_id].add(picture_id)
    
    return jsonify({
        'status': 'success',
        'tokens_remaining': intimacy_tokens[session_id]
    })
```

**NEW:**
```python
@app.route('/api/unlock-picture', methods=['POST'])
def unlock_picture():
    data = request.json
    session_id = data.get('session_id')
    picture_id = data.get('picture_id')
    
    # Check tokens
    affection_data = db.get_affection(session_id)
    current_tokens = affection_data['intimacy_tokens']
    cost = 10
    
    if current_tokens < cost:
        return jsonify({'error': 'Not enough tokens'}), 400
    
    # Deduct tokens
    new_tokens = current_tokens - cost
    db.update_affection(session_id, intimacy_tokens=new_tokens)
    
    # Unlock picture
    db.unlock_picture(session_id, picture_id)
    
    return jsonify({
        'status': 'success',
        'tokens_remaining': new_tokens
    })
```

---

## Benefits of Database

### 1. Persistence
- ✅ Data survives server restarts
- ✅ No data loss on crashes
- ✅ Automatic backups possible

### 2. Performance
- ✅ Indexed queries
- ✅ Efficient lookups
- ✅ Handles large datasets

### 3. Scalability
- ✅ Can migrate to PostgreSQL/MySQL later
- ✅ Supports concurrent access
- ✅ Thread-safe operations

### 4. Features
- ✅ Timestamps on all data
- ✅ CASCADE deletes
- ✅ Foreign key constraints
- ✅ Transaction support

### 5. Maintenance
- ✅ Easy to backup (single file)
- ✅ Can query with SQL
- ✅ Cleanup old sessions
- ✅ Statistics and analytics

---

## Migration Process

### Step 1: Run Migration Script
```bash
python migrate_to_database.py
```

This will:
- Create database tables
- Import existing JSON files
- Verify data integrity

### Step 2: Update app.py
Replace all in-memory operations with database calls.

### Step 3: Test
- Test all endpoints
- Verify data persistence
- Check performance

### Step 4: Deploy
- Backup database file
- Deploy updated code
- Monitor for issues

---

## Database File

**Location:** `sweetgf.db`

**Backup:**
```bash
# Simple copy
cp sweetgf.db sweetgf.db.backup

# With timestamp
cp sweetgf.db "sweetgf_$(date +%Y%m%d_%H%M%S).db"
```

**Restore:**
```bash
cp sweetgf.db.backup sweetgf.db
```

---

## Utility Functions

### Get Session Statistics
```python
stats = db.get_session_stats(session_id)
# Returns:
# {
#     'message_count': 150,
#     'total_pictures': 20,
#     'unlocked_pictures': 8,
#     'affection_points': 250,
#     'intimacy_tokens': 75
# }
```

### Cleanup Old Sessions
```python
# Delete sessions inactive for 30+ days
deleted = db.cleanup_old_sessions(days=30)
print(f"Deleted {deleted} old sessions")
```

### Delete Session
```python
# Delete all data for a session
db.delete_session(session_id)
```

---

## Thread Safety

Database module uses thread-local connections:

```python
# Each thread gets its own connection
def get_db():
    if not hasattr(_thread_local, 'connection'):
        _thread_local.connection = sqlite3.connect(DB_PATH)
    return _thread_local.connection
```

Safe for Flask's threaded mode.

---

## Error Handling

```python
try:
    db.save_girlfriend(session_id, name, preset)
except sqlite3.IntegrityError as e:
    print(f"Database integrity error: {e}")
except Exception as e:
    print(f"Database error: {e}")
```

---

## Performance Tips

### 1. Batch Operations
```python
# Instead of multiple saves
for msg in messages:
    db.save_message(session_id, msg['role'], msg['content'])

# Use transaction
conn = db.get_db()
cursor = conn.cursor()
cursor.executemany('''
    INSERT INTO conversations (session_id, role, content)
    VALUES (?, ?, ?)
''', [(session_id, msg['role'], msg['content']) for msg in messages])
conn.commit()
```

### 2. Limit Queries
```python
# Get last 50 messages only
messages = db.get_conversation(session_id, limit=50)
```

### 3. Use Indexes
Already created on:
- `pictures.session_id`
- `pictures.is_unlocked`
- `conversations.session_id`
- `conversations.timestamp`

---

## Summary

**Complete database system:**
- ✅ SQLite database with 6 tables
- ✅ Full CRUD operations
- ✅ Thread-safe connections
- ✅ Automatic timestamps
- ✅ CASCADE deletes
- ✅ Migration script
- ✅ Utility functions
- ✅ Statistics and cleanup
- ✅ Complete documentation

**Replace all in-memory dictionaries with database calls for persistent, scalable storage!** 💾✨
