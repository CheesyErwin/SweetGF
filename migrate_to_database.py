"""
Migration script to move from in-memory storage to database
Run this once to migrate existing data
"""

import database as db
import json
from pathlib import Path

def migrate_girlfriend_files():
    """Migrate girlfriend JSON files to database"""
    girlfriends_dir = Path('girlfriends')
    
    if not girlfriends_dir.exists():
        print("[Migration] No girlfriends directory found")
        return
    
    migrated = 0
    for filepath in girlfriends_dir.glob('*.json'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            session_id = data.get('session_id')
            if not session_id:
                print(f"[Migration] Skipping {filepath.name} - no session_id")
                continue
            
            # Create session
            db.create_session(session_id, data.get('language', 'en'))
            
            # Save girlfriend data
            db.save_girlfriend(
                session_id=session_id,
                name=data.get('name', 'Luna'),
                preset=data.get('preset'),
                personality=data.get('personality'),
                appearance=data.get('appearance'),
                reference_image=data.get('reference_image')
            )
            
            # Save affection data if present
            if 'affection' in data:
                db.update_affection(
                    session_id=session_id,
                    affection_points=data.get('affection', 0),
                    intimacy_tokens=data.get('tokens', 0),
                    unlocked_intimacy=data.get('unlocked_intimacy', [])
                )
            
            # Save conversation if present
            if 'conversation' in data:
                for msg in data['conversation']:
                    db.save_message(
                        session_id=session_id,
                        role=msg.get('role', 'user'),
                        content=msg.get('content', '')
                    )
            
            migrated += 1
            print(f"[Migration] Migrated {filepath.name}")
            
        except Exception as e:
            print(f"[Migration] Error migrating {filepath.name}: {e}")
    
    print(f"[Migration] Migrated {migrated} girlfriend files")

def verify_migration():
    """Verify migration was successful"""
    print("\n[Verification] Checking database...")
    
    conn = db.get_db()
    cursor = conn.cursor()
    
    # Count sessions
    cursor.execute('SELECT COUNT(*) as count FROM sessions')
    session_count = cursor.fetchone()['count']
    print(f"  Sessions: {session_count}")
    
    # Count girlfriends
    cursor.execute('SELECT COUNT(*) as count FROM girlfriends')
    gf_count = cursor.fetchone()['count']
    print(f"  Girlfriends: {gf_count}")
    
    # Count messages
    cursor.execute('SELECT COUNT(*) as count FROM conversations')
    msg_count = cursor.fetchone()['count']
    print(f"  Messages: {msg_count}")
    
    # Count pictures
    cursor.execute('SELECT COUNT(*) as count FROM pictures')
    pic_count = cursor.fetchone()['count']
    print(f"  Pictures: {pic_count}")
    
    print("\n[Verification] Migration complete!")

if __name__ == '__main__':
    print("=" * 60)
    print("SweetGF Database Migration")
    print("=" * 60)
    print()
    
    # Run migration
    migrate_girlfriend_files()
    
    # Verify
    verify_migration()
    
    print()
    print("=" * 60)
    print("Migration finished!")
    print("You can now start using the database-backed system.")
    print("=" * 60)
