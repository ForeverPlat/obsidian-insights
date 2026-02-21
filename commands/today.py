import os
from datetime import datetime, time

from database.notes import get_note_id_by_path, get_note_title_by_id, get_similar_notes
from pipeline.index_vault import VAULT_DIR
from utils.display import display_today


def _get_files(vault_path):
    results = []

    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                results.append(os.path.join(root, file))
    return results


# this might not be needed
def _get_most_accessed_today(vault_path):

    today_start = datetime.combine(datetime.today(), time.min).timestamp()

    files = _get_files(vault_path)

    accessed_today = []

    for file in files:
        if os.stat(file).st_atime >= today_start:
            accessed_today.append({"file": file, "atime": os.stat(file).st_atime})

    accessed_today.sort(key=lambda x: x["atime"], reverse=True)

    if accessed_today:
        return accessed_today[0]
    else:
        return None


def run_today(args):
    if not args:
        pass

    # get the file that was looked at the most today
    todays_note = _get_most_accessed_today(VAULT_DIR)

    if not todays_note:
        print("No notes accessed today.")
        return

    print(todays_note)

    # get the id for that note
    note_id = get_note_id_by_path(todays_note["file"])
    note_id = "0cc7894a371285621fa0564a610d3c1f47bdc3179991a4ad50d3a62964ae664e"  # <== ONLY FOR TESTING REMOVE
    print(note_id)

    # based on that find other notes in matrix that are similar
    similar_notes = get_similar_notes(note_id)
    similar_notes = similar_notes[:3]

    display_today(note_id, similar_notes)

    # return the similar notes who access time has been more than a # of time
