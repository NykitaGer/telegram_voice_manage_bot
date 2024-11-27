import sqlite3

db = sqlite3.connect("server.db")
cursor = db.cursor()


def create_tables() -> None:
    create_voice_table = """CREATE TABLE IF NOT EXISTS voices (
    id BIGINT,
    name TEXT
    )"""

    cursor.execute(create_voice_table)

    create_video_table = """CREATE TABLE IF NOT EXISTS videos (
    id BIGINT,
    name TEXT
    )"""

    cursor.execute(create_video_table)

    db.commit()
    return

def get_voices_from_db():
    get_voices = """SELECT id, name FROM voices"""
    data = cursor.execute(get_voices).fetchall()
    print(data)
    return data

def add_voice_to_db(file_id: int, file_name: str) -> None:
    insert_vioce_file = """INSERT INTO voices VALUES (?, ?)"""
    data = (file_id, file_name)

    print(data)
    cursor.execute(insert_vioce_file, data)
    db.commit()

def delete_voice_from_db():
    pass

def get_videos_from_db():
    get_videos = """SELECT id, name FROM videos"""
    data = cursor.execute(get_videos).fetchall()
    print(data)
    return data

def add_video_to_db(file_id: int, file_name: std):
    insert_video_file = """INSERT INTO videos VALUES (?, ?)"""
    data = (file_id, file_name)

    print(data)
    cursor.execute(insert_video_file, data)
    db.commit()
