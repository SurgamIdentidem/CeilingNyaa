from os import path

def get_path(x):
    if path.isabs(x):
        return x
    else:
        return get_relative_path(x)

def get_relative_path(x):
    return path.normpath(path.join(path.abspath(path.dirname(__file__)), x))
