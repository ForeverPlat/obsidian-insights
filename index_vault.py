import os
from pathlib import Path
from datetime import datetime

from numpy import full
from database.notes import *
from segment_notes import build_segments
from utils.ids import *

# import re
# init_all_schemas()

VAULT_DIR = "/Users/luqmanajani/documents/Notes/Obsidian-Vault"
# note_path = f"{vault_dir}/Intro to Databases.md"

# NOTE
# note_id TEXT
# path TEXT
# title/name TEXT
# raw_text TEXT
# created_at DATETIME
# modified_at DATETIME

# NOTE_LINKS
# note_id TEXT
# target TEXT
# link_text TEXT


def get_files():

    files = []
    for filename in os.listdir(VAULT_DIR):
        if filename[-2:] != "md":
            continue

        full_path = os.path.join(VAULT_DIR, filename)
        if os.path.isfile(full_path):
            # print(filename)
            # print(full_path)
            files.append(filename)

    print(files)
    print(len(files))


# get_files()


def get_file_times(file_path):
    file_path = Path(file_path)
    file_stats = file_path.stat()

    modified_at = datetime.fromtimestamp(file_stats.st_mtime)

    if hasattr(file_stats, "st_birthtime"):
        created_at = datetime.fromtimestamp(file_stats.st_ctime)
    else:
        created_at = modified_at

    return {"modified_at": modified_at, "created_at": created_at}


def get_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def normalize_link_target(raw: str) -> str:
    """
    Takes contents inside [[...]] and returns a vault filename like 'Note.md'
    Handles:
      [[Note]]
      [[Note|alias]]
      [[Note#Heading]]
      [[Note#Heading|alias]]
    """
    target = raw.split("|", 1)[0]  # drop alias
    target = target.split("#", 1)[0]  # drop heading anchor
    target = target.strip()

    if not target:
        return ""

    # If [[Note.md]] keep it, else add .md
    if not target.lower().endswith(".md"):
        target += ".md"

    return target


def get_links(note_id_a, file_path):
    try:
        with open(file_path, "r") as file:

            for line in file:
                # every thing under can be done with this as well (regex)
                # links += re.findall(r"\[\[(.*?)\]\]", line)

                while "[[" in line:
                    start = line.find("[[")
                    end = line.find("]]")

                    if end == -1:
                        break

                    inner = line[start + 2 : end]
                    target_filename = normalize_link_target(inner)

                    if target_filename:
                        target_path = os.path.join(VAULT_DIR, target_filename)

                        if os.path.isfile(target_path):
                            note_id_b = build_note_id(target_path)

                            if note_exists(note_id_b):
                                insert_note_link(note_id_a, note_id_b)

                    line = line[end + 2 :]

    except FileNotFoundError:
        print(f"{file_path} does not exist")
    except Exception as e:
        print(f"Error parsing links for {file_path}: {e}")


def index_vault():
    note_files = []

    for filename in os.listdir(VAULT_DIR):
        if not filename.lower().endswith(".md"):
            continue

        full_path = os.path.join(VAULT_DIR, filename)

        if not os.path.isfile(full_path):
            continue

        note_id = build_note_id(full_path)

        raw_text = get_text(full_path)
        times = get_file_times(full_path)

        insert_note(
            note_id,
            full_path,
            filename,
            raw_text,
            times["created_at"],
            times["modified_at"],
        )

        # segment here
        build_segments(note_id)

        note_files.append((note_id, full_path))

    for note_id, full_path in note_files:
        get_links(note_id, full_path)


if __name__ == "__main__":
    index_vault()


# index_vault()
# print(get_notes())
# note = "Obsidian Test"
# note_path = f"{VAULT_DIR}/{note}.md"
# l = get_links("Basics Of Technical Analysis FNCE")
# print(l)
# print(l[4])
# print(get_links(l[4]))

# print(get_links("Intro to Databases"))
# print(get_links("Basics Of Technical Analysis FNCE"))
# print(get_links("Obsidian Test"))
