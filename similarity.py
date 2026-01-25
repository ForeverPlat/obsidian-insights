from database.embeddings import get_embeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model_name = "all-MiniLM-L6-v2"


def compute_similarity(model_name):

    segment_ids, embedding_vectors = get_embeddings(model_name)

    embedding_matrix = np.vstack(embedding_vectors)
    similarity_matrix = cosine_similarity(embedding_matrix)

    # segment_ids are kind of like the
    # the rows and columns label for the matrix
    return segment_ids, similarity_matrix
