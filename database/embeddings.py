from . import conn, cursor

# [ SCHEMA ]
# - init_schema()
#   - creates note table
#   - creates link table


def init_schema():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embedding (
            segment_id TEXT,
            model_name TEXT,
            vector BLOB,

            FOREIGN KEY (segment_id) REFERENCES segment(segment_id)
        )
        """)

    conn.commit()


def get_embeddings():
    cursor.execute("SELECT * FROM embedding")
    return cursor.fetchall()


def insert_embedding(segment_id, model_name, vector):

    cursor.execute(
        "INSERT INTO embedding (segment_id, model_name, vector) VALUES (?,?,?) ",
        (segment_id, model_name, vector),
    )

    conn.commit()
