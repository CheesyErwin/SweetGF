# Privacy & Data Access Policy

## User Data Privacy

### What's Private (User-Only Access):

**Completely Private:**
- ✅ Girlfriend names
- ✅ Girlfriend appearances
- ✅ Conversation content
- ✅ Picture files
- ✅ Chat history
- ✅ Personal preferences

**Users have exclusive access to:**
- Their girlfriend configurations
- All conversation messages
- All generated pictures
- Unlock status of pictures
- Personal chat settings

---

## Admin Access (Limited)

### What Admins CAN See:

**Account Information:**
- Username
- Email
- Account status (active/inactive)
- Registration date
- Last login date
- Subscription tier
- Subscription expiration

**Usage Statistics (Counts Only):**
- Total message count (not content)
- Number of girlfriends created (not names)
- Total pictures generated (not images)
- Unlocked pictures count (not images)
- Current tokens
- Total tokens earned
- Tokens spent

**System Statistics:**
- Total users
- Active users
- New users
- System-wide totals

### What Admins CANNOT See:

❌ Girlfriend names or appearances
❌ Conversation content
❌ Picture files or images
❌ Chat history
❌ Personal messages
❌ Any private user content

---

## Privacy Implementation

### Database Level:

**Private Tables (User Access Only):**
```sql
girlfriends    - Girlfriend configurations
conversations  - Chat messages
pictures       - Picture metadata and files
```

**Admin-Accessible (Non-Private Data):**
```sql
users          - Account info (no passwords)
sessions       - Session tracking
affection      - Token/affection counts only
gallery_settings - Gallery size limits
```

### API Level:

**User-Only Endpoints:**
```
/api/chat                 - Send/receive messages
/api/get-gallery          - View pictures
/api/protected-image      - Access images
/api/girlfriend/*         - Girlfriend management
```

**Admin Endpoints (Privacy-Protected):**
```
/api/admin/users          - User list (no private data)
/api/admin/users/:id      - User stats (counts only)
/api/admin/stats          - System statistics
```

### Code Level:

**Privacy Functions:**
```python
# Returns counts only, no content
def get_user_stats_for_admin(user_id):
    stats = {
        'total_messages': count,      # Count, not content
        'girlfriend_count': count,     # Count, not names
        'total_pictures': count,       # Count, not images
        'tokens_spent': amount         # Amount, not what on
    }
    return stats
```

**User-Only Functions:**
```python
# Only accessible by owning user
def get_conversation(session_id):
    # Returns full conversation content
    # Requires user authentication
    
def get_girlfriend(session_id):
    # Returns girlfriend details
    # Requires user authentication
```

---

## Data Visibility Matrix

| Data Type | User | Admin | Public |
|-----------|------|-------|--------|
| Username | ✅ | ✅ | ❌ |
| Email | ✅ | ✅ | ❌ |
| Password | ❌ (hashed) | ❌ | ❌ |
| Subscription | ✅ | ✅ | ❌ |
| Girlfriend Name | ✅ | ❌ | ❌ |
| Girlfriend Appearance | ✅ | ❌ | ❌ |
| Conversations | ✅ | ❌ | ❌ |
| Pictures | ✅ | ❌ | ❌ |
| Message Count | ✅ | ✅ (count only) | ❌ |
| Token Balance | ✅ | ✅ | ❌ |
| Tokens Spent | ✅ | ✅ | ❌ |

---

## Admin Dashboard Privacy

### Statistics Shown:

**User Card:**
```
Username: john_doe
Email: john@example.com
Subscription: premium
Member Since: Jan 1, 2025
Last Login: Jan 15, 2025

Usage Statistics:
- Total Messages: 1,234 (count only)
- Girlfriends Created: 3 (count only)
- Total Pictures: 45 (count only)
- Unlocked Pictures: 12 (count only)

Token Statistics:
- Current Tokens: 150
- Total Tokens Earned: 500
- Tokens Spent: 350

🔒 Privacy Protected: Girlfriend names, conversations, 
and pictures are private and not visible to admins.
```

**What's NOT Shown:**
- Girlfriend names
- Conversation content
- Picture files
- Chat history
- Personal preferences

---

## Privacy Guarantees

### For Users:

✅ **Your conversations are private**
- Admins cannot read your messages
- Only you can access chat history

✅ **Your girlfriends are private**
- Names and appearances are hidden from admins
- Only you can see girlfriend details

✅ **Your pictures are private**
- Images are not accessible to admins
- Only you can view/unlock pictures

✅ **Your data is secure**
- Passwords are hashed (bcrypt)
- Sessions are encrypted
- Data is isolated per user

### For Admins:

✅ **Can manage accounts**
- Activate/deactivate users
- Update subscriptions
- View usage statistics

✅ **Can monitor system health**
- Total users and activity
- System-wide statistics
- Resource usage

❌ **Cannot access private data**
- No conversation access
- No picture access
- No girlfriend details

---

## Technical Implementation

### Database Queries (Privacy-Protected):

**Admin Query (Safe):**
```sql
-- Only counts, no content
SELECT COUNT(*) as total_messages
FROM conversations
WHERE session_id IN (
    SELECT session_id FROM sessions WHERE user_id = ?
)
```

**User Query (Full Access):**
```sql
-- Full content, user-authenticated
SELECT role, content, timestamp
FROM conversations
WHERE session_id = ?
AND user_id = ?  -- Verified ownership
```

### API Protection:

**User Endpoint:**
```python
@app.route('/api/chat')
@auth.require_auth  # User must be logged in
def chat():
    user = request.user
    # Verify session belongs to user
    if session.user_id != user.id:
        return 403  # Forbidden
    # Return full conversation
```

**Admin Endpoint:**
```python
@admin_bp.route('/users/<int:user_id>')
@auth.require_admin  # Admin only
def get_user(user_id):
    # Returns stats only, no private content
    stats = db.get_user_stats_for_admin(user_id)
    # No conversations, no pictures, no girlfriend names
```

---

## Privacy Compliance

### GDPR Compliance:

✅ **Right to Access**
- Users can view all their data
- Export functionality available

✅ **Right to Deletion**
- Users can delete their account
- CASCADE deletes all related data

✅ **Data Minimization**
- Admins only see necessary data
- Private content is isolated

✅ **Purpose Limitation**
- Data used only for service provision
- No unauthorized access

### Best Practices:

✅ Password hashing (bcrypt)
✅ Session encryption
✅ Role-based access control
✅ Data isolation per user
✅ Audit logging (optional)
✅ Regular security updates

---

## User Rights

### What You Can Do:

✅ **View Your Data**
- Access all conversations
- View all pictures
- See all girlfriend details

✅ **Export Your Data**
- Download conversations
- Export pictures
- Save girlfriend configs

✅ **Delete Your Data**
- Delete account
- Remove all data
- CASCADE deletion

✅ **Control Privacy**
- No data shared with admins
- Private by default
- Secure storage

---

## Summary

**Privacy-First Design:**
- ✅ User data is completely private
- ✅ Admins see only stats and subscription info
- ✅ No access to conversations or pictures
- ✅ Girlfriend details are user-exclusive
- ✅ Token/usage data for billing only
- ✅ GDPR-compliant
- ✅ Secure by design

**Your girlfriends, conversations, and pictures are 100% private. Admins can only see subscription status and usage statistics!** 🔒✨
