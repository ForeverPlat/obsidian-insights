import sqlite3

conn = sqlite3.connect("notes.db")
conn.execute("PRAGMA foreign_keys = ON")
assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1

cursor = conn.cursor()

from . import notes
from . import embeddings


def init_all_schemas():
    notes.init_schema()
    embeddings.init_schema()


# init_all_schemas()
