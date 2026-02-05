from database import init_all_schemas
from database.notes import drop_all_tables
from database.similar_edges import store_similar_edges
from pipeline.embed import embed_segments
from pipeline.index_vault import index_vault
from pipeline.similarity import compute_similarity
from pipeline.similarity import extract_similar_edges

model_name = "all-MiniLM-L6-v2"


def run_build(args):
    if not args:
        pass

    drop_all_tables()
    init_all_schemas()

    index_vault()
    embed_segments()

    segment_ids, similarity_matrix = compute_similarity(model_name)

    if len(segment_ids) == 0:
        print("No embeddings found, nothing to compute similarity on.")
        return

    similar_edges = extract_similar_edges(segment_ids, similarity_matrix)
    store_similar_edges(similar_edges)
