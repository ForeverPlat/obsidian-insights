from . import conn, cursor
import numpy as np

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


def get_embeddings(model_name):

    cursor.execute(
        "SELECT segment_id, vector FROM embedding WHERE model_name = ? ORDER BY segment_id",
        (model_name,),
    )

    rows = cursor.fetchall()

    segment_ids = []
    embedding_vectors = []

    for segment_id, vector_blob in rows:
        segment_ids.append(segment_id)

        # convert BLOB → numpy array
        vector = np.frombuffer(vector_blob, dtype=np.float32)
        embedding_vectors.append(vector)

    return segment_ids, embedding_vectors


def insert_embedding(segment_id, model_name, vector):

    cursor.execute(
        "INSERT INTO embedding (segment_id, model_name, vector) VALUES (?,?,?) ",
        (segment_id, model_name, vector),
    )

    conn.commit()
