from os import wait
from database.notes import *
from utils.ids import get_segment_id

# segment_id (hash of note_id + position)
# note_id
# heading (nullable)
# content (raw text)
# position (order in note)

# good for segments
# test_note_id = "20250904150047"

# testing for no headers
# test_note_id = "20250520192001"

# testing for bolds
# test_note_id = "20251225082000"


# print(lines)

FOUND_HEADER = False
FOUND_BOLD = False


def process_line_into_segments(curr_segment, segments, is_delimeter, line):
    if is_delimeter:

        if curr_segment["heading"] or curr_segment["text"]:
            segments.append(curr_segment)  # add prev segment

        curr_segment = {"heading": line, "text": ""}

        # print("-------------")
        # print(curr_segment)
    else:
        curr_segment["text"] += line + "\n"
        # print(line)

    return curr_segment


def is_header(line):
    if not line.startswith("#"):
        return False

    hash_count = 0

    for c in line:
        if c == "#":
            hash_count += 1

            if hash_count > 6:
                return False
        else:
            break

    if not (1 <= hash_count <= 6):
        return False

    if line[hash_count : hash_count + 1] != " ":
        return False

    FOUND_HEADER = True
    return True


def build_segments_with_headers(lines):
    segments = []
    segment = {"heading": "", "text": ""}

    for line in lines:

        is_delimeter = is_header(line)

        segment = process_line_into_segments(segment, segments, is_delimeter, line)

    if segment["heading"] or segment["text"]:
        segments.append(segment)

    return segments


# build_segments_with_headers()


def is_bold(line):
    # update to check if entire line is bold maybe?
    pass


def build_segments_with_bolds(lines):
    segments = []
    segment = {"heading": "", "text": ""}

    for line in lines:
        bold = line[:2] == "**"
        bold_italic = line[:3] == "***"

        is_delimeter = bold or bold_italic

        if is_delimeter:
            FOUND_BOLD = True

        segment = process_line_into_segments(segment, segments, is_delimeter, line)

    if segment["heading"] or segment["text"]:
        segments.append(segment)

    return segments


def build_segments(note_id):

    # maybe send in raw text?
    raw_text = get_raw_text_by_id(note_id)
    lines = raw_text.split("\n")

    segments = build_segments_with_headers(lines)

    if len(segments) <= 1:
        segments = build_segments_with_bolds(lines)

    if len(segments) <= 1:
        segments = [{"heading": "", "text": raw_text}]

    for position, segment in enumerate(segments, start=1):

        segment_id = get_segment_id(note_id, segment["heading"], position)

        # i do not think the position is working
        insert_segment(
            segment_id=segment_id,
            note_id=note_id,
            heading=segment["heading"],
            content=segment["text"],
            position=position,
        )

    return segments


def test():
    test_note_id = get_note_id_by_path(
        "/Users/luqmanajani/documents/Notes/Obsidian-Vault/Chapter 1 — The Purpose and Use of Financial Statements.md"
    )

    # print(build_segments(test_note_id))


# print(get_raw_text_by_id(test_id))

# test_note_id = "20250904150047"

# segment_id (hash of note_id + position)
# note_id
# heading (nullable)
# content (raw text)
# position (order in note)
