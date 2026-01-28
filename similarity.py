from database import init_all_schemas
from database.embeddings import get_embeddings
from database.notes import (
    get_note_id_by_segment_id,
    is_link,
    get_note_title_by_segment_id,
)
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

init_all_schemas()

model_name = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.7


def compute_similarity(model_name):

    segment_ids, embedding_vectors = get_embeddings(model_name)

    embedding_matrix = np.vstack(embedding_vectors)
    similarity_matrix = cosine_similarity(embedding_matrix)

    # segment_ids are kind of like the
    # the rows and columns label for the matrix
    return segment_ids, similarity_matrix


def extract_similar_edges(segment_ids, similarity_matrix, top_k=5):

    similar_edges = []

    for i, seg_a in enumerate(segment_ids):
        # for max five per
        edges_found = 0

        similarity_scores = similarity_matrix[i]
        sorted_indices = sorted(
            range(len(similarity_scores)),
            key=lambda j: similarity_scores[j],
            reverse=True,
        )

        for other_index in sorted_indices:

            if i == other_index:
                # skip itslef
                continue

            seg_b = segment_ids[other_index]
            note_a = get_note_id_by_segment_id(seg_a)
            note_b = get_note_id_by_segment_id(seg_b)

            if note_a == note_b:
                # skip if in same note
                continue

            score = similarity_scores[other_index]

            if score < SIMILARITY_THRESHOLD:
                break  # since it is ordered other remaining scores will be lower

            soure_name = get_note_title_by_segment_id(seg_a)
            target_name = get_note_title_by_segment_id(seg_b)

            seen_edges = set()
            edge_key = tuple(sorted((seg_a, seg_b)))

            # hehehehe O(1)
            # okay bud its not that special
            if edge_key in seen_edges:
                # skip if missing connection has been found
                continue

            # for visual rep
            similar_edges.append(
                {
                    "source": seg_a,
                    "target": seg_b,
                    "score": score,
                    "source_name": soure_name,
                    "target_name": target_name,
                }
            )

            # for regular
            # similar_edges.append({"source": seg_a, "target": seg_b, "score": score})

            seen_edges.add(edge_key)

            edges_found += 1
            if edges_found >= top_k:
                break

    return similar_edges


def find_missing_connections(similar_edges):

    connections = []

    for edge in similar_edges:

        is_missing = not is_link(edge["source"], edge["target"])

        if is_missing:
            # for regular
            # connections.append(edge)

            # for visual rep
            connections.append(
                f"{edge['source_name']} -> {edge['target_name']}, score: {edge['score']}"
            )

    # check if edge already exist (link)
    return connections


segment_ids, similarity_matrix = compute_similarity(model_name)
similar_edges = extract_similar_edges(segment_ids, similarity_matrix)
missing_connections = find_missing_connections(similar_edges)

# print(missing_connections)

for con in missing_connections:
    print(con)
    print("")
