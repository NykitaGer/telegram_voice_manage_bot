from db.manager import DatabaseManager

def is_user_admin(db: DatabaseManager, user_id: int) -> bool:
    """Check if a user is an admin."""
    return db.is_user_admin(user_id)
