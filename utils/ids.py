import hashlib
from pathlib import Path


def get_note_id(file_path: str):

    normalized = file_path.lower().replace("\\", "/")

    # encode string to bits
    encoded_string = normalized.encode("utf-8")

    # create a sha-256 hash object
    hash_object = hashlib.sha256(encoded_string)

    # get the hexadecimal representation of the hash
    hex_digest = hash_object.hexdigest()

    return hex_digest


def get_segment_id(note_id: str, heading: str, position: int):
    heading_part = heading.lower().strip() if heading else ""
    raw = f"{note_id}:{position}:{heading_part}"

    encoded_string = raw.encode("utf-8")

    hash_object = hashlib.sha256(encoded_string)

    hex_digest = hash_object.hexdigest()

    return hex_digest
