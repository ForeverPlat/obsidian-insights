import os
import hashlib
from pathlib import Path
from datetime import datetime
from database import *

# import re

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


def get_note_id(file_path):

    file_path = Path(file_path)
    file_stats = file_path.stat()

    if hasattr(file_stats, "st_birthtime"):
        created_at = datetime.fromtimestamp(file_stats.st_birthtime)
    else:
        created_at = datetime.fromtimestamp(file_stats.st_mtime)  # fallback

    note_id = created_at.strftime("%Y%m%d%H%M%S")
    return note_id


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
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except:
        print(f"{file_path} does not exsist")


def get_links(source_note_id, file_path):
    # example of link
    #     {
    #         "source_note_id": id,
    #         "target_node_id": id
    #         "target_title": "Another Note",
    #         "target_path": "/notes/another_note.md",
    #     },

    links = []

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

                    link_name = line[start + 2 : end]
                    target_path = os.path.join(VAULT_DIR, link_name)

                    if os.path.isfile(target_path):
                        target_note_id = get_note_id(target_path)

                        insert_link(source_note_id, target_note_id)

                    line = line[end + 2 :]

    except:
        print(f"{file_path} does not exsist")

    return links


def build_db():

    for filename in os.listdir(VAULT_DIR):
        if filename[-2:] != "md":
            continue

        full_path = os.path.join(VAULT_DIR, filename)
        if os.path.isfile(full_path):
            id = get_note_id(full_path)

            get_links(id, full_path)

            note = {
                "note_id": id,
                "path": full_path,
                "title": filename,
                "raw_text": get_text(full_path),
                "created_at": get_file_times(full_path)["created_at"],
                "modified_at": get_file_times(full_path)["modified_at"],
            }

            insert_note(
                note["note_id"],
                note["path"],
                note["title"],
                note["raw_text"],
                note["created_at"],
                note["modified_at"],
            )


build_db()
# print(get_notes())
note = "Obsidian Test"
note_path = f"{VAULT_DIR}/{note}.md"
# l = get_links("Basics Of Technical Analysis FNCE")
# print(l)
# print(l[4])
# print(get_links(l[4]))

# print(get_links("Intro to Databases"))
# print(get_links("Basics Of Technical Analysis FNCE"))
# print(get_links("Obsidian Test"))
