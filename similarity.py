from database import init_all_schemas
from database.embeddings import get_embeddings
from database.notes import (
    get_note_id_by_segment_id,
    get_segment_content,
    note_link_exist,
    get_note_title_by_segment_id,
)
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# init_all_schemas()

model_name = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.7


def compute_similarity(model_name):

    segment_ids, embedding_vectors = get_embeddings(model_name)

    embedding_matrix = np.vstack(embedding_vectors)
    similarity_matrix = cosine_similarity(embedding_matrix)

    if not embedding_vectors:
        return [], np.array([])

    # segment_ids are kind of like the
    # the rows and columns label for the matrix
    return segment_ids, similarity_matrix


def extract_similar_edges(segment_ids, similarity_matrix):

    similar_edges = {}

    for i, seg_a in enumerate(segment_ids):
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

            edge_key = tuple(sorted((note_a, note_b)))

            # for visual rep
            edge = {
                "source": seg_a,
                "target": seg_b,
                "score": score,
                "source_name": get_note_title_by_segment_id(seg_a),
                "target_name": get_note_title_by_segment_id(seg_b),
                "source_content": get_segment_content(seg_a),
                "target_content": get_segment_content(seg_b),
            }

            if edge_key not in similar_edges:
                similar_edges[edge_key] = edge
            else:
                if score > similar_edges[edge_key]["score"]:
                    similar_edges[edge_key] = edge

    sorted_edges = sorted(
        similar_edges.values(),
        key=lambda e: e["score"],
        reverse=True,
    )

    return sorted_edges


def find_missing_connections(similar_edges, top_k=5):

    connections = []

    for edge in similar_edges:

        source_note = get_note_id_by_segment_id(edge["source"])
        target_note = get_note_id_by_segment_id(edge["target"])

        if source_note == target_note:
            continue

        if note_link_exist(source_note, target_note):
            continue  # already linked

            # for visual rep
        connections.append(
            {
                "source_name": edge["source_name"],
                "target_name": edge["target_name"],
                "score": edge["score"],
                "source_content": edge["source_content"],
                "target_content": edge["target_content"],
            }
        )

    return connections[:top_k]


# segment_ids, similarity_matrix = compute_similarity(model_name)
# similar_edges = extract_similar_edges(segment_ids, similarity_matrix)
# missing_connections = find_missing_connections(similar_edges)
#
# # print(missing_connections)
#
# for con in missing_connections:
#     print(con)
#     print("")
