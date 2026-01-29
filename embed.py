from sentence_transformers import SentenceTransformer
from database import init_all_schemas
from database.notes import get_segments
from database.embeddings import insert_embedding, get_embeddings  # type: ignore

# put in main later
init_all_schemas()


def embed_segments():

    model = SentenceTransformer("all-MiniLM-L6-v2")

    segments = get_segments()

    if not segments:
        print("No segments found in database")
        exit()

    # vectors = []

    # later update this to batch embeddings for faster time
    for segment in segments:
        if len(segment["content"]) < 30:
            continue

        text_to_embed = (
            (segment["heading"] + "\n") if segment["heading"] else ""
        ) + segment["content"]

        vector = model.encode(text_to_embed)

        insert_embedding(
            segment_id=segment["segment_id"],
            model_name="all-MiniLM-L6-v2",
            vector=vector.tobytes(),
        )

        # vectors.append(vector)


embed_segments()

# all_embeddings = get_embeddings()
# print(f"Successfully inserted {len(all_embeddings)} embeddings")
