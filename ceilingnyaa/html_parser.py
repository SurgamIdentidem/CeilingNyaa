import bitmath, sys
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from log import log_error, log_info

HTML_PARSER = "lxml"

def get_latest_release_info(watchlist):
    latest_release_info = []

    for watchlist_item in watchlist:
        try:
            req = request.Request(watchlist_item.get("full_url"))
            req.add_header("User-Agent", "Mozilla/5.0")

            log_info("Checking: " + req.get_full_url())

            page = BeautifulSoup(urlopen(req), HTML_PARSER)

            try:
                row = page.find("table", class_="torrent-list").find("tbody").find("tr")
            except AttributeError:
                row = None

            if row is None:
                log_info("No results found for " + req.get_full_url())

            else:
                cells = row.select("td")

                if cells is not None and len(cells) >= 2:
                    latest_release_info.append({
                        "title": watchlist_item.get("title"),
                        "last_known_filename": watchlist_item.get("last_known_filename"),
                        "filename": get_title_from_cell(cells[1]),
                        "magnet_link": get_magnet_link_from_cell(cells[2]),
                        "filesize_in_bytes": get_filesize_in_bytes_from_cell(cells[3])
                    })

        except KeyboardInterrupt as e:
            raise e
        except HTTPError as e:
            log_error('Error retrieving data: ' + str(e))
        except URLError as e:
            log_error('Error retrieving data: ' + str(e))
        except:
            log_error('Error retrieving data:' + str(sys.exc_info()[0]))

    return latest_release_info

def get_title_from_cell(cell):
    tags = cell.find_all('a')
    for tag in tags:
        if not "comments" in tag.get("class", []):
            return tag.get("title")

    return None

def get_magnet_link_from_cell(cell):
    return cell.select("a")[1]['href']

def get_filesize_in_bytes_from_cell(cell):
    filesize = cell.text.replace("Bytes", "Byte")

    return float(bitmath.parse_string(filesize).to_Byte())
