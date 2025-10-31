# Authentication & Admin System

## Overview

Complete user authentication system with login, registration, and admin dashboard for managing users and viewing statistics.

---

## Features

### User Authentication:
- ✅ User registration with validation
- ✅ Secure password hashing (bcrypt)
- ✅ Login/logout functionality
- ✅ Session management
- ✅ Password requirements enforcement

### Admin Dashboard:
- ✅ User management (view, activate, deactivate)
- ✅ Real-time statistics
- ✅ Subscription management
- ✅ System cleanup tools
- ✅ Activity monitoring

---

## Database Schema

### Users Table:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    subscription_tier TEXT DEFAULT 'free',
    subscription_expires TIMESTAMP
)
```

### Sessions Linked to Users:
```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER,
    created_at TIMESTAMP,
    last_active TIMESTAMP,
    language TEXT DEFAULT 'en',
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

---

## API Endpoints

### Authentication:

**Register:**
```
POST /api/auth/register
Body: {username, email, password}
```

**Login:**
```
POST /api/auth/login
Body: {username, password}
```

**Logout:**
```
POST /api/auth/logout
```

**Check Auth:**
```
GET /api/auth/check
```

**Get Current User:**
```
GET /api/auth/me
Requires: Authentication
```

### Admin:

**Get All Users:**
```
GET /api/admin/users?page=1&per_page=50
Requires: Admin
```

**Get User Details:**
```
GET /api/admin/users/:id
Requires: Admin
```

**Deactivate User:**
```
POST /api/admin/users/:id/deactivate
Requires: Admin
```

**Activate User:**
```
POST /api/admin/users/:id/activate
Requires: Admin
```

**Update Subscription:**
```
PUT /api/admin/users/:id/subscription
Body: {tier, expires_at}
Requires: Admin
```

**Get Statistics:**
```
GET /api/admin/stats
Requires: Admin
```

**Cleanup Old Data:**
```
POST /api/admin/cleanup
Body: {days}
Requires: Admin
```

---

## Password Requirements

- Minimum 8 characters
- Maximum 128 characters
- At least one letter
- At least one number

---

## Usage Examples

### Register User:
```javascript
const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        username: 'john_doe',
        email: 'john@example.com',
        password: 'SecurePass123'
    })
});
```

### Login:
```javascript
const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        username: 'john_doe',
        password: 'SecurePass123'
    })
});

const data = await response.json();
// Store session token
localStorage.setItem('session_token', data.session_token);
```

### Admin - Get Users:
```javascript
const response = await fetch('/api/admin/users?page=1&per_page=20');
const data = await response.json();
// data.users, data.total, data.page, data.per_page
```

---

## Integration with app.py

### 1. Import Modules:
```python
from flask import Flask, session
import auth
from auth_routes import auth_bp, admin_bp
import database as db

app = Flask(__name__)
app.secret_key = auth.SECRET_KEY

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
```

### 2. Protect Routes:
```python
@app.route('/api/chat', methods=['POST'])
@auth.require_auth
def chat():
    user = request.user
    # ... chat logic
```

### 3. Link Sessions to Users:
```python
# When creating session
user_id = session.get('user_id')
db.create_session(session_id, user_id=user_id)
```

---

## Admin Dashboard

**URL:** `/admin.html`

**Features:**
- Real-time statistics
- User list with pagination
- Activate/deactivate users
- View user details
- Subscription management
- Auto-refresh stats

**Statistics Shown:**
- Total users
- Active users (7 days)
- New users today
- Total messages
- Total pictures
- Unlocked pictures
- Subscription breakdown

---

## Login Page

**URL:** `/login.html`

**Features:**
- Login form
- Registration form
- Tab switching
- Form validation
- Error messages
- Auto-redirect after login
- Remember session

---

## Security Features

### Password Security:
- ✅ Bcrypt hashing
- ✅ Salt per password
- ✅ No plaintext storage

### Session Security:
- ✅ Secure session tokens
- ✅ Server-side validation
- ✅ Automatic expiration

### Authorization:
- ✅ Role-based access (admin/user)
- ✅ Route protection decorators
- ✅ User activation status

### Validation:
- ✅ Username format check
- ✅ Email format check
- ✅ Password strength check
- ✅ Duplicate prevention

---

## Files Created

1. **database.py** (updated)
   - Added users table
   - User management functions
   - Session-user linking

2. **auth.py**
   - Password hashing/verification
   - User registration/login
   - Validation functions
   - Auth decorators

3. **auth_routes.py**
   - Authentication endpoints
   - Admin endpoints
   - User management
   - Statistics

4. **static/login.html**
   - Login/register UI
   - Form validation
   - Auto-redirect

5. **static/admin.html**
   - Admin dashboard
   - User management UI
   - Statistics display
   - Real-time updates

6. **AUTH_SYSTEM.md**
   - Complete documentation

---

## Creating First Admin

### Method 1: Direct Database
```python
import database as db
import auth

# Create admin user
password_hash = auth.hash_password('admin_password')
user_id = db.create_user('admin', 'admin@sweetgf.com', password_hash, is_admin=True)
print(f"Admin created with ID: {user_id}")
```

### Method 2: Registration + Update
```python
# Register normally
# Then update in database:
import database as db
conn = db.get_db()
cursor = conn.cursor()
cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
conn.commit()
```

---

## Subscription Tiers

**Default Tiers:**
- `free` - Default for all users
- `premium` - Paid subscription
- `vip` - Highest tier

**Usage:**
```python
# Update subscription
db.update_user_subscription(
    user_id=1,
    tier='premium',
    expires_at='2025-12-31'
)
```

---

## Admin Statistics

**Available Stats:**
- Total users
- Active users (last 7 days)
- New users today
- Total sessions
- Total messages
- Total pictures
- Unlocked pictures
- Subscription breakdown

**Auto-refresh:** Every 30 seconds

---

## User Management

**Admin Can:**
- ✅ View all users
- ✅ Search/filter users
- ✅ Activate/deactivate accounts
- ✅ Update subscriptions
- ✅ View user statistics
- ✅ Clean up old data

**Admin Cannot:**
- ❌ See user passwords
- ❌ Deactivate own account
- ❌ Delete users (only deactivate)

---

## Testing

### Test Registration:
1. Go to `/login.html`
2. Click "Register" tab
3. Fill in form
4. Submit
5. Should see success message

### Test Login:
1. Enter credentials
2. Click "Login"
3. Should redirect to main page
4. Admin users redirect to `/admin.html`

### Test Admin Dashboard:
1. Login as admin
2. Go to `/admin.html`
3. Should see statistics
4. Should see user list
5. Can activate/deactivate users

---

## Summary

**Complete authentication system:**
- ✅ User registration with validation
- ✅ Secure login (bcrypt)
- ✅ Session management
- ✅ Admin dashboard
- ✅ User management
- ✅ Real-time statistics
- ✅ Role-based access control
- ✅ Password requirements
- ✅ Beautiful UI
- ✅ Complete documentation

**Users can now register, login, and admins can manage the entire system through a web dashboard!** 🔐✨
