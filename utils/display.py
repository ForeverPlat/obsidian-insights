from database.notes import get_note_title_by_id
from database.notes import get_segment_content


def _preview(text, max_lines):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return "\n".join(lines[:max_lines])


def display_connections(connections, max_lines=6):
    for edge in connections:
        divider = "━" * 60

        note_a = get_note_title_by_id(edge["note_a_id"])
        note_b = get_note_title_by_id(edge["note_b_id"])

        seg_a_text = get_segment_content(edge["rep_seg_a_id"])
        seg_b_text = get_segment_content(edge["rep_seg_b_id"])

        print(divider)
        print(" Suggested Connection")
        print(divider)
        print()
        print(f"FROM : {note_a}")
        print(f"TO   : {note_b}")
        print(f"SCORE: {edge['best_score']:.2f}")
        print()

        print(f"--- Evidence from {note_a} ---")
        print(_preview(seg_a_text, max_lines))
        print()

        print(f"--- Evidence from {note_b} ---")
        print(_preview(seg_b_text, max_lines))
        print()


def display_merge_candidates(candidates, max_lines=6):
    for edge in candidates:
        divider = "━" * 60

        note_a = get_note_title_by_id(edge["note_a_id"])
        note_b = get_note_title_by_id(edge["note_b_id"])

        seg_a_text = get_segment_content(edge["rep_seg_a_id"])
        seg_b_text = get_segment_content(edge["rep_seg_b_id"])

        print(divider)
        print("󰐱 Possible Merge / Consolidation")
        print(divider)
        print()
        print(f"NOTE A : {note_a}")
        print(f"NOTE B : {note_b}")
        print(f"SCORE  : {edge['best_score']:.2f}")
        print(f"SHARED SEGMENTS : {edge['num_similar_segments']}")
        print()

        print(f"--- Overlapping content in {note_a} ---")
        print(_preview(seg_a_text, max_lines))
        print()

        print(f"--- Overlapping content in {note_b} ---")
        print(_preview(seg_b_text, max_lines))
        print()
