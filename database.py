import sqlite3

# [ DATABASE SETUP ]
# - DB_PATH
# - connection
# - cursor

conn = sqlite3.connect("note.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# [ SCHEMA ]
# - init_schema()
#   - creates note table
#   - creates link table


def init_schema():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id TEXT PRIMARY KEY,
            path TEXT UNIQUE,
            title TEXT,
            raw_text TEXT,
            created_at DATETIME,
            modified_at DATETIME
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS link (
            source_note_id TEXT,
            target_note_id TEXT,

            FOREIGN KEY (source_note_id) REFERENCES note(id),
            FOREIGN KEY (target_note_id) REFERENCES note(id)
        )
        """)

    conn.commit()


init_schema()

# [ NOTE OPERATIONS ]
# - insert_note
# - update_note
# - get_note_by_id
# - etc.


def insert_note(id, path, title, raw_text, created_at, modified_at):

    cursor.execute(
        "INSERT INTO note (id, path, title, raw_text, created_at, modified_at) VALUES (?,?,?,?,?,?) ",
        (id, path, title, raw_text, created_at, modified_at),
    )

    conn.commit()


def get_notes():
    cursor.execute("SELECT * FROM note")
    return cursor.fetchall()


def get_raw_text_by_id(note_id):

    cursor.execute("SELECT raw_text FROM note WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    return row[0] if row else ""


# [ LINK OPERATIONS ]
# - insert_link
# - get_links_from
# - get_links_to
# - etc.


def insert_link(source_note_id, target_note_id):

    cursor.execute(
        "INSERT INTO link (source_note_id, target_note_id) VALUES (?,?)",
        (source_note_id, target_note_id),
    )

    conn.commit()


def get_links_from(note_id):
    pass


def get_links_to(note_id):
    pass
