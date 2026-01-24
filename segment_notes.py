from os import wait
from database import *

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
test_note_id = "20251225082000"


raw_text = get_raw_text_by_id(test_note_id)
# print(raw_text)

lines = []
l = ""

for letter in raw_text:
    if letter == "\n":
        lines.append(l)
        l = ""
    else:
        l += letter

# print(lines)


def build_segments(segment, segments, is_segment, line):
    if is_segment:
        segments.append(segment)
        print("-------------")
        segment = line
        print(segment)
    else:
        segment += line + "\n"
        print(line)

    return segments, segment


def build_segments_with_headers():
    segments = []
    segment = ""

    for line in lines:

        h1 = line[:2] == "# "
        h2 = line[:3] == "## "
        h3 = line[:4] == "### "
        h4 = line[:5] == "#### "
        h5 = line[:6] == "##### "

        is_segment = h1 or h2 or h3 or h4 or h5
        segments, segment = build_segments(segment, segments, is_segment, line)

    print(segments)


# build_segments_with_headers()


def build_segments_with_bolds():
    segments = []
    segment = ""

    for line in lines:
        bold = line[:2] == "**"
        bold_italic = line[:3] == "***"

        is_segment = bold or bold_italic
        segments, segment = build_segments(segment, segments, is_segment, line)

    print(segments)
