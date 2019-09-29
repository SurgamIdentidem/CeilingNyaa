from time import sleep
from sys import exc_info, exit
from config_parser import get_config_key
from csv_parser import get_watchlist, update_last_known_filenames
from process_latest_release_info import download_and_or_notify
from html_parser import get_latest_release_info
from log import log_error, log_info, log_success

log_success("CeilingNyaa is starting...")

try:
    while True:
        log_info("Main loop starting")

        try:
            watchlist = get_watchlist()
        except IOError as e:
            raise IOError(log_error("Error getting watchlist info: " + str(e)))

        try:
            update_last_known_filenames(download_and_or_notify(get_latest_release_info(watchlist)))
        except KeyboardInterrupt as e:
            raise e
        except IOError as e:
            raise IOError(log_error("Error saving watchlist info: " + str(e)))

        log_info("Main loop done")

        run_once = get_config_key("RunOnce", default = False, isBoolean = True)
        if run_once:
            log_info("run_once is True, breaking out of main loop")
            break

        minutes_to_sleep = int(get_config_key("CheckIntervalInMinutes", default = False))
        log_info("Next run will be in " + str(minutes_to_sleep) + " minutes")
        sleep(minutes_to_sleep * 60)

except KeyboardInterrupt:
    log_info("KeyboardInterrupt received")

except IOError:
    log_error("CeilingNyaa is exiting...")
    exit(1)

except:
    log_error("Unexpected error: " + str(exc_info()[0]))
    log_error("CeilingNyaa is exiting...")
    exit(2)

log_success("CeilingNyaa is exiting...")
exit(0)
