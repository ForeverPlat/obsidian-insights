from database.embeddings import get_embeddings
from database.notes import (
    get_note_id_by_segment_id,
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
                continue

            seg_b = segment_ids[other_index]

            note_a = get_note_id_by_segment_id(seg_a)
            note_b = get_note_id_by_segment_id(seg_b)

            if note_a == note_b:
                continue

            score = similarity_scores[other_index]

            if score < SIMILARITY_THRESHOLD:
                break

            if note_a < note_b:
                note_low, note_high = note_a, note_b
                seg_low, seg_high = seg_a, seg_b
            else:
                note_low, note_high = note_b, note_a
                seg_low, seg_high = seg_b, seg_a

            edge_key = (note_low, note_high)

            if not edge_key in similar_edges:
                similar_edges[edge_key] = {
                    "note_a_id": note_low,
                    "note_b_id": note_high,
                    "best_score": float(score),
                    "num_similar_segments": 1,
                    "rep_seg_a_id": seg_low,
                    "rep_seg_b_id": seg_high,
                }
            else:
                edge = similar_edges[edge_key]

                edge["num_similar_segments"] += 1

                if score > edge["best_score"]:
                    edge["best_score"] = float(score)
                    edge["rep_seg_a_id"] = seg_low
                    edge["rep_seg_b_id"] = seg_high

    sorted_edges = sorted(
        similar_edges.values(),
        key=lambda e: e["best_score"],
        reverse=True,
    )

    return sorted_edges


# def classify_relationship(edge):
#     if edge["num_similar_segments"] >= 3:
#         return "merge_candidate"
#     return "missing_connection"
#
#
# def find_relationships(similar_edges, top_k=5):
#
#     connections = []
#     merges = []
#
#     for edge in similar_edges:
#
#         source_note = get_note_id_by_segment_id(edge["source"])
#         target_note = get_note_id_by_segment_id(edge["target"])
#
#         if source_note == target_note:
#             continue
#
#         relation_type = classify_relationship(edge)
#
#         payload = {
#             "source_name": edge["source_name"],
#             "target_name": edge["target_name"],
#             "score": edge["score"],
#             "source_content": edge["source_content"],
#             "target_content": edge["target_content"],
#         }
#
#         if relation_type == "merge_candidate":
#             merges.append(payload)
#             continue
#
#         if note_link_exist(source_note, target_note):
#             continue  # already linked
#
#             # for visual rep
#         connections.append(payload)
#
#     return {
#         "missing_connections": connections[:top_k],
#         "merge_candidates": merges[:top_k],
#     }


# segment_ids, similarity_matrix = compute_similarity(model_name)
# similar_edges = extract_similar_edges(segment_ids, similarity_matrix)
# missing_connections = find_missing_connections(similar_edges)
#
# # print(missing_connections)
#
# for con in missing_connections:
#     print(con)
#     print("")
