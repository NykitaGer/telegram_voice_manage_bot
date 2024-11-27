import sqlite3

connect = sqlite3.connect("db/server.db")
cursor = connect.cursor()


def create_tables() -> None:
    create_voice_table = """CREATE TABLE IF NOT EXISTS voices (
    id BIGINT,
    name TEXT
    )"""

    print(create_voice_table)
    cursor.execute(create_voice_table)
    return


def add_voice_to_db(file_id: int, file_name: str) -> None:
    insert_vioce_file = """INSERT INTO voices VALUES (?, ?)"""
    data = (file_id, file_name)

    print(data)
    cursor.execute(insert_vioce_file, data)
    return



