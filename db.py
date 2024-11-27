import sqlite3

db = sqlite3.connect("server.db")
cursor = db.cursor()


def create_tables() -> None:
    create_voice_table = """CREATE TABLE IF NOT EXISTS voices (
    id BIGINT,
    name TEXT
    )"""

    cursor.execute(create_voice_table)
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
    return


def delete_voice_from_db():
    pass
