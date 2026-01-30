from database.__init__ import init_all_schemas
from database.notes import drop_all_tables
from index_vault import index_vault
from segment_notes import *
from embed import *
from similarity import (
    compute_similarity,
    extract_similar_edges,
    find_missing_connections,
)

model_name = "all-MiniLM-L6-v2"
DB_PATH = "note.db"


def obsidian_insights():
    drop_all_tables()
    init_all_schemas()

    index_vault()
    embed_segments()

    segment_ids, similarity_matrix = compute_similarity(model_name)

    if len(segment_ids) == 0:
        print("No embeddings found, nothing to compute similarity on.")
        return

    similar_edges = extract_similar_edges(segment_ids, similarity_matrix)
    missing_connections = find_missing_connections(similar_edges)

    for con in missing_connections:
        print(con)
        print("\n")


if __name__ == "__main__":
    obsidian_insights()
