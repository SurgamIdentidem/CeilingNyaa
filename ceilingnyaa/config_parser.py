from ast import literal_eval
import configparser

from log import log_error, log_info, log_success
from utils import get_path

INI_FILENAME = "config.ini"

def get_config_section(section, Config = None):
    obj = {}
    if Config is None:
        Config = read_ini()

    if Config.has_section(section):
        options = Config.options(section)

        for option in options:
            try:
                obj[option] = Config.get(section, option)
            except:
                obj[option] = None
                log_error("Error getting option " + str(option) + " from ini: " + str(sys.exc_info()[0]))

    return obj

def get_config_key(key, default = None, section = None, isBoolean = False):
    Config = read_ini()
    key = str(key).lower()

    sections = Config.sections()
    if section is not None:
        sections = [section]

    for section in sections:
        section_data = get_config_section(section, Config)

        key_data = section_data.get(key, None)

        if key_data is not None:
            if isBoolean:
                return get_boolean_from_key_data(key_data, default)

            else:
                return key_data

    return default

def read_ini():
    Config = configparser.ConfigParser()
    Config.read(get_path("../" + INI_FILENAME))

    return Config

def get_boolean_from_key_data(x, default = False):
    try:
        return bool(literal_eval(x))
    except:
        return default
