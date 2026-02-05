from . import conn, cursor


def init_schema():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS similar_edge (
            note_a_id TEXT,
            note_b_id TEXT,

            best_score REAL,
            num_similar_segments INTEGER,

            rep_seg_a_id TEXT,
            rep_seg_b_id TEXT,

            PRIMARY KEY (note_a_id, note_b_id),

            FOREIGN KEY (note_a_id) REFERENCES note(id),
            FOREIGN KEY (note_b_id) REFERENCES note(id),
            FOREIGN KEY (rep_seg_a_id) REFERENCES segment(segment_id),
            FOREIGN KEY (rep_seg_b_id) REFERENCES segment(segment_id)            )
        """)

    conn.commit()


def insert_similar_edge(edge):
    cursor.execute(
        """
        INSERT INTO similar_edge (
            note_a_id,
            note_b_id,
            best_score,
            num_similar_segments,
            rep_seg_a_id,
            rep_seg_b_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            edge["note_a_id"],
            edge["note_b_id"],
            edge["best_score"],
            edge["num_similar_segments"],
            edge["rep_seg_a_id"],
            edge["rep_seg_b_id"],
        ),
    )

    conn.commit()


def store_similar_edges(edges):
    # there might be away to just batch insert
    for edge in edges:
        insert_similar_edge(edge)


def get_similar_edges(order_by="best_score DESC"):
    cursor.execute(f"""
        SELECT
            note_a_id,
            note_b_id,
            best_score,
            num_similar_segments,
            rep_seg_a_id,
            rep_seg_b_id
        FROM similar_edge
        ORDER BY {order_by}
    """)
    rows = cursor.fetchall()

    return [
        {
            "note_a_id": row[0],
            "note_b_id": row[1],
            "best_score": row[2],
            "num_similar_segments": row[3],
            "rep_seg_a_id": row[4],
            "rep_seg_b_id": row[5],
        }
        for row in rows
    ]
