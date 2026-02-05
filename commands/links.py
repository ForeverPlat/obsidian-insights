from database.similar_edges import get_similar_edges
from utils.display import display_connections

model_name = "all-MiniLM-L6-v2"


def run_links(args, top_k=1):
    if not args:
        pass

    edges = get_similar_edges()

    connections = []

    for edge in edges:
        if edge["num_similar_segments"] < 3:
            connections.append(edge)

    if not connections:
        print("No possible connections found.")
        return

    connections = connections[:top_k]

    display_connections(connections)
