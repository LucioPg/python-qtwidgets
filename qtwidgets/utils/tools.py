from os.path import join, dirname

def parent_dir(path):
    return join(dirname(dirname(path)))