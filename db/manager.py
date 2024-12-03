import sqlite3
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "server.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        """Create necessary tables if they do not already exist."""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            username TEXT,
            is_admin BOOLEAN
        )"""

        create_voice_table = """
        CREATE TABLE IF NOT EXISTS voices (
            id BIGINT PRIMARY KEY,
            name TEXT
        )"""

        create_video_table = """
        CREATE TABLE IF NOT EXISTS videos (
            id BIGINT PRIMARY KEY,
            name TEXT
        )"""

        create_chats_table = """
        CREATE TABLE IF NOT EXISTS chats (
            id BIGINT PRIMARY KEY,
            voice_pending BOOLEAN,
            video_pending BOOLEAN
        )"""

        self.cursor.execute(create_users_table)
        self.cursor.execute(create_voice_table)
        self.cursor.execute(create_video_table)
        self.cursor.execute(create_chats_table)
        self.db.commit()

    # User Management
    def get_users(self) -> List[Tuple[int, str, bool]]:
        query = "SELECT id, username, is_admin FROM users"
        return self.cursor.execute(query).fetchall()

    def add_user(self, user_id: int, username: str, is_admin: bool) -> bool:
        if any(user[0] == user_id for user in self.get_users()):
            return False
        query = "INSERT INTO users (id, username, is_admin) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user_id, username, is_admin))
        self.db.commit()
        return True

    def is_user_admin(self, user_id: int) -> bool:
        query = "SELECT is_admin FROM users WHERE id = ?"
        result = self.cursor.execute(query, (user_id,)).fetchone()
        return result[0] if result else False

    def change_user_permission(self, user_id: int, is_admin: bool) -> None:
        query = "UPDATE users SET is_admin = ? WHERE id = ?"
        self.cursor.execute(query, (is_admin, user_id))
        self.db.commit()

    # Voice Management
    def get_voices(self) -> List[Tuple[int, str]]:
        query = "SELECT id, name FROM voices"
        return self.cursor.execute(query).fetchall()

    def add_voice(self, voice_id: int, voice_name: str) -> bool:
        if any(voice[0] == voice_id for voice in self.get_voices()):
            return False
        query = "INSERT INTO voices (id, name) VALUES (?, ?)"
        self.cursor.execute(query, (voice_id, voice_name))
        self.db.commit()
        return True

    def update_voice(self, old_name: str, new_name: str) -> None:
        query = "UPDATE voices SET name = ? WHERE name = ?"
        self.cursor.execute(query, (new_name, old_name))
        self.db.commit()

    def delete_voice(self, voice_name: str) -> None:
        query = "DELETE FROM voices WHERE name = ?"
        self.cursor.execute(query, (voice_name,))
        self.db.commit()

    # Video Management
    def get_videos(self) -> List[Tuple[int, str]]:
        query = "SELECT id, name FROM videos"
        return self.cursor.execute(query).fetchall()

    def add_video(self, video_id: int, video_name: str) -> None:
        query = "INSERT INTO videos (id, name) VALUES (?, ?)"
        self.cursor.execute(query, (video_id, video_name))
        self.db.commit()

    # Chat Management
    def add_chat(self, chat_id: int) -> None:
        query = "INSERT INTO chats (id, voice_pending, video_pending) VALUES (?, ?, ?)"
        self.cursor.execute(query, (chat_id, False, False))
        self.db.commit()

    def set_voice_pending(self, chat_id: int, is_pending: bool) -> None:
        query = "UPDATE chats SET voice_pending = ? WHERE id = ?"
        self.cursor.execute(query, (is_pending, chat_id))
        self.db.commit()

    def is_voice_pending(self, chat_id: int) -> bool:
        query = "SELECT voice_pending FROM chats WHERE id = ?"
        result = self.cursor.execute(query, (chat_id,)).fetchone()
        return result[0] if result else False

    # General
    def close(self) -> None:
        """Close the database connection."""
        self.db.close()
