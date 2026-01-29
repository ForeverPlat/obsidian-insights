from . import conn, cursor

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
            note_a_id TEXT,
            note_b_id  TEXT,

            FOREIGN KEY (note_a_id) REFERENCES note(id),
            FOREIGN KEY (note_b_id) REFERENCES note(id)
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS segment (
            segment_id TEXT PRIMARY KEY,
            note_id TEXT,
            heading TEXT,
            content TEXT,
            position INTEGER,

            FOREIGN KEY (note_id) REFERENCES note(id)
        )
   """)

    conn.commit()


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


def get_note_id_by_path(file_path):
    cursor.execute("SELECT id FROM note WHERE path = ?", (file_path,))
    row = cursor.fetchone()
    return row[0] if row else ""


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


def insert_note_link(seg_a_id, seg_b_id):

    note_id_1 = get_note_id_by_segment_id(seg_a_id)
    note_id_2 = get_note_id_by_segment_id(seg_b_id)

    note_low_id = min(note_id_1, note_id_2)
    note_high_id = max(note_id_1, note_id_2)

    cursor.execute(
        "INSERT INTO link (note_a_id, note_b_id) VALUES (?,?)",
        (note_low_id, note_high_id),
    )

    conn.commit()


def note_link_exist(seg_a_id, seg_b_id):

    note_id_1 = get_note_id_by_segment_id(seg_a_id)
    note_id_2 = get_note_id_by_segment_id(seg_b_id)

    note_low_id = min(note_id_1, note_id_2)
    note_high_id = max(note_id_1, note_id_2)

    cursor.execute(
        "SELECT 1 FROM link WHERE note_a_id = ? AND note_b_id = ?",
        (note_low_id, note_high_id),
    )

    return cursor.fetchone() is not None


def get_links_from(note_id):
    pass


def get_links_to(note_id):
    pass


# [ SEGMENT OPERATIONS ]


def get_segments():
    cursor.execute(
        "SELECT segment_id, note_id, heading, content, position FROM segment"
    )
    rows = cursor.fetchall()
    # return rows
    # Convert to dictionaries for easier use
    return [
        {
            "segment_id": row[0],
            "note_id": row[1],
            "heading": row[2],
            "content": row[3],
            "position": row[4],
        }
        for row in rows
    ]


def get_note_id_by_segment_id(segment_id):
    cursor.execute("SELECT note_id FROM segment WHERE segment_id = ?", (segment_id,))
    row = cursor.fetchone()
    return row[0] if row else ""


def get_note_title_by_segment_id(segment_id):
    note_id = get_note_id_by_segment_id(segment_id)

    cursor.execute("SELECT title FROM note WHERE id = ?", (note_id,))

    title = cursor.fetchone()
    return title


def insert_segment(segment_id, note_id, heading, content, position):

    # check if note exists
    cursor.execute("SELECT 1 FROM note WHERE id = ?", (note_id,))

    if cursor.fetchone() is None:
        raise ValueError(f"Note with id {note_id} does not exist")

    cursor.execute(
        "INSERT INTO segment (segment_id, note_id, heading, content, position) VALUES (?,?,?,?,?)",
        (segment_id, note_id, heading, content, position),
    )

    conn.commit()
