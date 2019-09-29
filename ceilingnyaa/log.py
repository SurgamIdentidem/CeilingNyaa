import os
from datetime import datetime

import config_parser
from utils import get_path

try:
    import termcolor

    try:
        if os.name == 'nt': # are we on Windows?
            import colorama
            colorama.init()

    except ImportError:
        print('"pip install colorama" for colored console messages on Windows"')
        pass

except ImportError:
    print('"pip install termcolor" for colored console messages"')
    pass

LOG_FOLDER_NAME = 'logs'

def log_error(message, forceNoFileLog = False):
    return log_message(message, 1, forceNoFileLog)

def log_success(message, forceNoFileLog = False):
    return log_message(message, 2, forceNoFileLog)

def log_info(message, forceNoFileLog = False):
    return log_message(message, 3, forceNoFileLog)

def log_message(message, level = 3, forceNoFileLog = False): #level 1 = error, 2 = success, 3 = info
    original_message = message
    message = str(message)
    log_type = "[INFO]   "
    if level == 1:
        log_type = "[ERROR]  "
    elif level == 2:
        log_type = "[SUCCESS]"

    message = "[" + get_current_datetime() + "]" + log_type + " " + str(message)
    console_log_level = int(config_parser.get_config_key("ConsoleLogLevel", 3))
    file_log_level = int(config_parser.get_config_key("FileLogLevel", 2))

    if level <= console_log_level:
        if termcolor:
            color = "white"
            if level == 1:
                color = "red"
            elif level == 2:
                color = "green"

            termcolor.cprint(termcolor.colored(message, color))

        else:
            print(message)

    if level <= file_log_level and not forceNoFileLog:
        if create_log_directory_if_needed():
            file_name = '../' + LOG_FOLDER_NAME + '/' + get_current_date() + '.txt'
            file_path = get_path(file_name)

            try:
                f = open(file_path, 'a')
                f.write(message + '\n')
                f.close()

            except:
                log_error('Error creating or appending to log file.', forceNoFileLog = True)

    return original_message


def create_log_directory_if_needed():
    path = get_path('../' + LOG_FOLDER_NAME)

    if not os.path.exists(path) or not os.path.isdir(path):
        try:
            os.makedirs(path)

            return True

        except:
            log_error('Error creating logs directory.', forceNoFileLog = True)
            
            return False

    else:
        return True

def get_current_datetime():
    return str(datetime.now().strftime("%Y%m%d %H:%M:%S"))

def get_current_date():
    return str(datetime.now().strftime("%Y%m%d"))
