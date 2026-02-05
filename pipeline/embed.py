import re
from sentence_transformers import SentenceTransformer
from database import init_all_schemas
from database.notes import get_segments
from database.embeddings import insert_embedding, get_embeddings  # type: ignore

# put in main later
init_all_schemas()

_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
_CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


def clean_for_embedding(text):
    text = re.sub(_FRONTMATTER_RE, "", text)
    text = re.sub(_CODE_FENCE_RE, "", text)
    return text.strip()


def embed_segments():

    model = SentenceTransformer("all-MiniLM-L6-v2")

    segments = get_segments()

    if not segments:
        print("No segments found in database")
        return

    # vectors = []

    # later update this to batch embeddings for faster time
    for segment in segments:
        content = clean_for_embedding(segment["content"] or "")
        heading = (segment["heading"] or "").strip()

        if len(content) < 80:
            continue

        text_to_embed = (heading + "\n" if heading else "") + content

        vector = model.encode(text_to_embed, convert_to_numpy=True)

        insert_embedding(
            segment_id=segment["segment_id"],
            model_name="all-MiniLM-L6-v2",
            vector=vector.tobytes(),
        )
        # vectors.append(vector)


if __name__ == "__main__":
    embed_segments()

# all_embeddings = get_embeddings()
# print(f"Successfully inserted {len(all_embeddings)} embeddings")
