from database.similar_edges import get_similar_edges
from utils.display import display_merge_candidates

model_name = "all-MiniLM-L6-v2"


def run_merge(args, top_k=1):
    if not args:
        pass

    edges = get_similar_edges()

    merges = []

    for edge in edges:
        if edge["num_similar_segments"] >= 3:
            merges.append(edge)

    if not merges:
        print("No merge candidates found.")
        return

    merges = merges[:top_k]

    display_merge_candidates(merges)
