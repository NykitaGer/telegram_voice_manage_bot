import sqlite3

db = sqlite3.connect("server.db")
cursor = db.cursor()


def create_tables() -> None:
    create_users_table = """CREATE TABLE IF NOT EXISTS users (
    id BIGINT,
    username TEXT,
    is_admin BOOLEAN
    )"""

    create_voice_table = """CREATE TABLE IF NOT EXISTS voices (
    id BIGINT,
    name TEXT
    )"""

    create_video_table = """CREATE TABLE IF NOT EXISTS videos (
    id BIGINT,
    name TEXT
    )"""

    create_chats_table = """CREATE TABLE IF NOT EXISTS chats (
    id BIGINT,
    voice_pending BOOLEAN,
    video_pending BOOLEAN
    )"""

    cursor.execute(create_users_table)
    cursor.execute(create_voice_table)
    cursor.execute(create_video_table)
    cursor.execute(create_chats_table)

    db.commit()

def get_users_from_db() -> list[tuple[str]]:
    get_users = "SELECT id, username, is_admin FROM users"
    data = cursor.execute(get_users).fetchall()
    return data

def add_user(user_id: int, username: str, permission: bool) -> bool:
    users = get_users_from_db()
    for id, username, is_admin in users:
        if id == user_id:
            return False
        
    insert_user = "INSERT INTO users VALUES (?, ?, ?)"
    data = (user_id, username, permission)
    cursor.execute(insert_user, data)
    db.commit()
    return True

def is_user_admin(user_id: int) -> bool:
    users = get_users_from_db()
    for id, username, is_admin in users:
        if id == user_id and is_admin == True:
            return True
    return False

def change_user_permission(user_id: int, permission: bool) -> None:    
    change_permission = "UPDATE users SET is_admin = ? WHERE id = ?"
    data = (permission, user_id)
    cursor.execute(change_permission, data)
    db.commit()

def get_voices_from_db() -> list[tuple[str]]:
    get_voices = "SELECT id, name FROM voices"
    data = cursor.execute(get_voices).fetchall()
    return data
    
def add_voice_to_db(file_id: int, file_name: str) -> bool:
    voices = get_voices_from_db()

    for id, name in voices:
        if id == file_id:
            return False

    insert_voice_file = "INSERT INTO voices VALUES (?, ?)"
    data = (file_id, file_name)

    cursor.execute(insert_voice_file, data)
    db.commit()
    return True

def update_voice(old_file_name: str, new_file_name: str) -> None:
    update_voice_file = "UPDATE voices SET name = ? WHERE id = ?"
    data = (new_file_name, old_file_name)
    cursor.execute(update_voice_file, data)
    db.commit()


def delete_voice_from_db(name: str):
    delete_voice = "DELETE FROM voices WHERE name = ?"
    cursor.execute(delete_voice, name)
    db.commit()

def get_videos_from_db() -> list[tuple[str]]:
    get_videos = "SELECT id, name FROM videos"
    data = cursor.execute(get_videos).fetchall()
    return data

def add_video_to_db(file_id: int, file_name: str):
    insert_video_file = "INSERT INTO videos VALUES (?, ?)"
    data = (file_id, file_name)

    cursor.execute(insert_video_file, data)
    db.commit()


def add_chat_id(chat_id: int):
    add_id = "INSERT INTO chats VALUES (?, ?, ?)"

    cursor.execute(add_id, (chat_id, False, False))
    db.commit()


def change_voice_pending(chat_id: int, pending: bool):
    change_pending = "UPDATE chats SET voice_pending = ? WHERE id = ?"

    data = (pending, chat_id)

    cursor.execute(change_pending, data)
    db.commit()


def check_voice_pending(chat_id: int) -> bool:
    voice_pending = "SELECT voice_pending FROM chats WHERE id = ?"
    data = cursor.execute(voice_pending, (chat_id,)).fetchone()
    return data[0]
