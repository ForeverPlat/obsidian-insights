import os
from datetime import datetime, time

from pipeline.index_vault import VAULT_DIR


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

    # based on that find other notes in matrix that are similar

    # return the similar notes who access time has been more than a # of time
