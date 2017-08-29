import csv, re
from urllib import urlencode

from config_parser import get_config_key
from log import log_error, log_info, log_success
from utils import get_path

BASE_URL = "https://nyaa.si"

def get_watchlist():
    watchlist = []

    with open_csv_file("rb") as csvfile:
        reader = csv.reader(csvfile)
        first_row = True

        for row in reader:
            if first_row and len(row) > 0 and row[0] == "#TITLE":
                pass

            elif len(row) >= 2:
                watchlist_item = {
                    "title": row[0],
                    "search": row[1],
                    "last_known_filename": row[2].strip() if len(row) > 2 and row[2] else None,
                    "categories": row[3] if len(row) > 3 and row[3] else "0_0",
                    "filters": row[4] if len(row) > 4 and row[4] else "0",
                }

                full_url = re.sub(r'[\/\\\?]*$', "", BASE_URL) #removing trailing \, /, and ? just in case

                full_url = full_url + "/?" + urlencode({
                    "f": watchlist_item.get("filters"),
                    "c": watchlist_item.get("categories"),
                    "q": watchlist_item.get("search"),
                    "s": "id",
                    "o": "desc",
                })

                watchlist_item["full_url"] = full_url

                watchlist.append(watchlist_item)

            first_row = False

    return watchlist

def update_last_known_filenames(shows = { "title_here": "latest_filename_here" }):
    if len(shows) <= 0:
        return False

    watchlist = []
    rows_to_write = []

    with open_csv_file("rb") as csvfile:
        reader = csv.reader(csvfile)
        first_row = True

        for row in reader:
            if first_row and len(row) > 0 and row[0] == "#TITLE":
                pass

            elif len(row) >= 2:
                if row[0] in shows:
                    row[2] = shows[row[0]]

            first_row = False
            rows_to_write.append(row)

    with open_csv_file("wb") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows_to_write)

    return True

def open_csv_file(mode = "rb"):
    watchlist_file_path = get_config_key("WatchListPath", default = "../watchlist.csv")
    return open(get_path(watchlist_file_path), mode)
