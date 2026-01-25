from database import init_all_schemas
from database.embeddings import get_embeddings
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

            score = similarity_scores[other_index]

            if score < SIMILARITY_THRESHOLD:
                break  # since it is ordered other remaining scores will be lower

            seg_b = segment_ids[other_index]

            similar_edges.append({"source": seg_a, "target": seg_b, "score": score})

            edges_found += 1
            if edges_found >= top_k:
                break

    return similar_edges


def find_missing_connections():
    # check if edge already exist (link)
    pass


segment_ids, similarity_matrix = compute_similarity(model_name)
edges = extract_similar_edges(segment_ids, similarity_matrix)

print(edges)
