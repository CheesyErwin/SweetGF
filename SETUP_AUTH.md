# Authentication Setup Guide

## Quick Setup (3 Steps)

### Step 1: Install bcrypt
```bash
pip install bcrypt
```

### Step 2: Create Admin User
```bash
python create_admin.py
```

Follow the prompts:
- Enter admin username (e.g., `admin`)
- Enter admin email (e.g., `admin@sweetgf.com`)
- Enter password (min 8 chars, must have letters + numbers)
- Confirm password

### Step 3: Start Server
```bash
python app.py
```

---

## Access Points

### Login Page
```
http://localhost:5000/login.html
```

### Admin Dashboard
```
http://localhost:5000/admin.html
```
(Requires admin login)

### Main App
```
http://localhost:5000/
```

---

## Default Behavior

### Without Login:
- Users can still access the main app
- No authentication required for basic features
- Sessions work as before

### With Login:
- Users can register accounts
- Save progress across devices
- Access from anywhere
- Admin can manage users

---

## Making Authentication Required (Optional)

If you want to require login for the main app, add this to your chat endpoint:

```python
@app.route('/api/chat', methods=['POST'])
@auth.require_auth  # Add this decorator
def chat():
    user = request.user  # Access logged-in user
    # ... rest of code
```

---

## Testing

### 1. Create Admin:
```bash
python create_admin.py
# Username: admin
# Email: admin@test.com
# Password: admin123
```

### 2. Login:
- Go to http://localhost:5000/login.html
- Enter credentials
- Should redirect to admin dashboard

### 3. Register User:
- Click "Register" tab
- Fill in form
- Should create account and redirect to login

### 4. Admin Panel:
- View all users
- See statistics
- Activate/deactivate users
- View user stats (privacy-protected)

---

## Troubleshooting

### "Module 'bcrypt' not found"
```bash
pip install bcrypt
```

### "Module 'auth' not found"
Make sure `auth.py` is in the same directory as `app.py`

### "Module 'auth_routes' not found"
Make sure `auth_routes.py` is in the same directory as `app.py`

### Can't access admin panel
1. Make sure you created an admin user
2. Login at /login.html first
3. Then go to /admin.html

### Login page not showing
1. Make sure `static/login.html` exists
2. Check Flask is serving static files
3. Try http://localhost:5000/login.html directly

---

## File Checklist

Required files:
- ✅ `auth.py` - Authentication logic
- ✅ `auth_routes.py` - API endpoints
- ✅ `database.py` - Database functions
- ✅ `static/login.html` - Login page
- ✅ `static/admin.html` - Admin dashboard
- ✅ `create_admin.py` - Admin creation script

---

## Security Notes

### In Production:

1. **Change Secret Key:**
```python
# In auth.py or app.py
app.secret_key = os.getenv('SECRET_KEY', 'your-random-secret-key')
```

2. **Use HTTPS:**
- Never send passwords over HTTP
- Use SSL certificate

3. **Environment Variables:**
```bash
# .env file
SECRET_KEY=your-very-long-random-secret-key-here
DATABASE_URL=your-database-url
```

4. **Password Requirements:**
- Already enforced: 8+ chars, letters + numbers
- Consider adding: special characters, uppercase

5. **Rate Limiting:**
- Add rate limiting to login endpoint
- Prevent brute force attacks

---

## Summary

**Setup Complete:**
- ✅ Authentication system integrated
- ✅ Admin panel available
- ✅ Login/register pages ready
- ✅ Privacy-protected user data
- ✅ Bcrypt password hashing
- ✅ Session management

**Next Steps:**
1. Run `python create_admin.py`
2. Start server: `python app.py`
3. Login at http://localhost:5000/login.html
4. Access admin at http://localhost:5000/admin.html

**Your authentication system is ready to use!** 🔐✨
