"""
Create first admin user
Run this script once to create an admin account
"""

import database as db
import auth

def create_admin():
    """Create admin user"""
    print("=" * 60)
    print("Create Admin User for SweetGF")
    print("=" * 60)
    print()
    
    # Get admin credentials
    username = input("Enter admin username: ").strip()
    email = input("Enter admin email: ").strip()
    password = input("Enter admin password: ").strip()
    password_confirm = input("Confirm password: ").strip()
    
    # Validate
    if not username or not email or not password:
        print("\n❌ Error: All fields are required")
        return
    
    if password != password_confirm:
        print("\n❌ Error: Passwords do not match")
        return
    
    # Validate password
    valid, error = auth.validate_password(password)
    if not valid:
        print(f"\n❌ Error: {error}")
        return
    
    # Check if username exists
    if db.get_user_by_username(username):
        print(f"\n❌ Error: Username '{username}' already exists")
        return
    
    # Check if email exists
    if db.get_user_by_email(email):
        print(f"\n❌ Error: Email '{email}' already exists")
        return
    
    # Hash password
    password_hash = auth.hash_password(password)
    
    # Create admin user
    user_id = db.create_user(username, email, password_hash, is_admin=True)
    
    if user_id:
        print(f"\n✅ Success! Admin user created:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   User ID: {user_id}")
        print()
        print("You can now login at: http://localhost:5000/login.html")
        print("After login, access admin panel at: http://localhost:5000/admin.html")
    else:
        print("\n❌ Error: Failed to create admin user")

if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
