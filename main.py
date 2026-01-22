import os
import hashlib
import pathlib
from datetime import datetime

# import re

VAULT_DIR = "/Users/luqmanajani/documents/Notes/Obsidian-Vault"
# note_path = f"{vault_dir}/Intro to Databases.md"


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


def hash_filename(filename):
    # SHA-256

    # encode string to bits
    encoded_string = filename.encode("utf-8")

    # create a sha-256 hash object
    hash_object = hashlib.sha256(encoded_string)

    # get the hexadecimal representation of the hash
    hex_digest = hash_object.hexdigest()

    return hex_digest


def get_file_times(file_path):
    # file_path = pathlib.Path(file_path)

    file_stats = file_path.stat()

    modified_at = datetime.fromtimestamp(file_stats.st_mtime)
    created_at = datetime.fromtimestamp(file_stats.st_ctime)

    return {modified_at, created_at}


def get_text(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except:
        print(f"{file_path} does not exsist")


def get_links(file_path):
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

                    link = line[start + 2 : end]
                    links.append(link)
                    line = line[end + 2 :]
    except:
        print(f"{note_path} does not exsist")

    return links


def search_connections(link):
    pass


note = "Obsidian Test"
note_path = f"{VAULT_DIR}/{note}.md"
# l = get_links("Basics Of Technical Analysis FNCE")
# print(l)
# print(l[4])
# print(get_links(l[4]))

# print(get_links("Intro to Databases"))
# print(get_links("Basics Of Technical Analysis FNCE"))
# print(get_links("Obsidian Test"))
