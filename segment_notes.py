from os import wait
import re
from database.notes import *
from utils.ids import build_segment_id

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

# remove the properties
_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
# remove code blocks
_CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)

MIN_CHARS = 100
MIN_WORDS = 20


def strip_frontmatter(text: str) -> str:
    return re.sub(_FRONTMATTER_RE, "", text)


def strip_code_fences(text: str) -> str:
    return re.sub(_CODE_FENCE_RE, "", text)


def is_meaningful_segment(text: str) -> bool:
    if not text:
        return False

    cleaned = text.strip()
    if not cleaned:
        return False

    cleaned = strip_frontmatter(cleaned)
    cleaned = strip_code_fences(cleaned).strip()

    if not cleaned:
        return False

    # drop segments that are basically only embeds / links
    # still allows some links, but not link-only chunks
    just_links = re.sub(r"\[\[.*?\]\]", "", cleaned)
    just_links = re.sub(r"!\[\[.*?\]\]", "", just_links).strip()

    # count real words (letters+numbers)
    words = re.findall(r"[A-Za-z0-9]+", cleaned)

    if len(cleaned) < MIN_CHARS:
        return False
    if len(words) < MIN_WORDS:
        return False
    if len(just_links) < 20:  # mostly links/embeds
        return False

    return True


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

    return True


def build_segments_with_headers(lines):
    segments = []
    segment = {"heading": "", "text": ""}

    for line in lines:

        segment = process_line_into_segments(segment, segments, is_header(line), line)

    if segment["heading"] or segment["text"]:
        segments.append(segment)

    return segments


def build_segments_with_bolds(lines):
    segments = []
    segment = {"heading": "", "text": ""}

    for line in lines:
        bold = line[:2] == "**"
        bold_italic = line[:3] == "***"

        is_delimeter = bold or bold_italic

        segment = process_line_into_segments(segment, segments, is_delimeter, line)

    if segment["heading"] or segment["text"]:
        segments.append(segment)

    return segments


def build_segments(note_id):

    # maybe send in raw text?
    raw_text = get_raw_text_by_id(note_id)

    if raw_text is None:
        return []

    raw_text = strip_frontmatter(raw_text)

    lines = raw_text.split("\n")

    segments = build_segments_with_headers(lines)

    if len(segments) <= 1:
        segments = build_segments_with_bolds(lines)

    if len(segments) <= 1:
        segments = [{"heading": "", "text": raw_text}]

    position = 1
    kept = []

    for segment in segments:
        content = segment["text"].strip()

        if not is_meaningful_segment(content):
            continue

        segment_id = build_segment_id(note_id, segment["heading"], position)

        # i do not think the position is working
        insert_segment(
            segment_id=segment_id,
            note_id=note_id,
            heading=segment["heading"],
            content=content,
            position=position,
        )

        kept.append(segment)
        position += 1

    return kept


# def test():
#     test_note_id = get_note_id_by_path(
#         "/Users/luqmanajani/documents/Notes/Obsidian-Vault/Chapter 1 — The Purpose and Use of Financial Statements.md"
#     )

# print(build_segments(test_note_id))


# print(get_raw_text_by_id(test_id))

# test_note_id = "20250904150047"

# segment_id (hash of note_id + position)
# note_id
# heading (nullable)
# content (raw text)
# position (order in note)
