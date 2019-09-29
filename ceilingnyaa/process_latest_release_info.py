import bitmath, os, subprocess, sys
from pushbullet import Pushbullet, InvalidKeyError

from config_parser import get_config_key
from log import log_error, log_info, log_success

def download_and_or_notify(latest_release_info):
    items_acted_on = {}

    automatically_download_on_new_release = get_config_key("AutomaticallyDownloadOnNewRelease", default = True, isBoolean = True)
    notify_on_new_release = get_config_key("NotifyOnNewRelease", default = False, isBoolean = True)

    for row in latest_release_info:
        if row["filename"] != row["last_known_filename"]:
            log_success("A new file is available for " + row["title"] + ": " + row["filename"])

            if automatically_download_on_new_release:
                if is_within_maximum_file_size(row["filesize_in_bytes"]):
                    open_magnet_link(row["magnet_link"])
                else:
                    log_info("AutomaticallyDownloadOnNewRelease is True but MaximumFileSizeInMB was exceeded")

            if notify_on_new_release:
                create_pushbullet_notification(row["title"], row["filename"])

            items_acted_on[row["title"]] = row["filename"]

    return items_acted_on

def create_pushbullet_notification(title, filename):
    api_token = get_config_key("APIToken")

    try:
        pb = Pushbullet(api_token)
        note = "A new file is available for " + title + ": " + filename

        log_info("Sending Pushbullet notification...")
        pb.push_note("CeilingNyaa", note)

        log_success("Pushbullet notification sent for " + title + ": " + filename)

    except InvalidKeyError as e:
        log_error("Error creating Pushbullet notification: " + str(e))

    except:
        log_error("Error creating Pushbullet notification: " + str(sys.exc_info()[0]))

def is_within_maximum_file_size(file_size_in_bytes):
    maximum_file_size_in_mb = float(get_config_key("MaximumFileSizeInMB", 0))

    if maximum_file_size_in_mb == 0:
        return True

    maximum_file_size_in_bytes = float(bitmath.MiB(maximum_file_size_in_mb).to_Byte())

    return maximum_file_size_in_bytes >= file_size_in_bytes

def open_magnet_link(magnet_link):
    try:
        if sys.platform.startswith("darwin"):
            subprocess.Popen(("open", magnet_link))
        elif os.name == "posix":
            subprocess.Popen(("xdg-open", magnet_link))
        else: #os.name == "nt":
            os.startfile(magnet_link)

        log_success("Magnet link opened: " + str(magnet_link))

    except:
        log_error("Error opening magnet link: " + str(sys.exc_info()[0]))
