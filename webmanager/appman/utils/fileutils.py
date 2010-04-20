import os

from django.conf import settings

def relative(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

def fullpath(filepath):
    return "%s%s/%s" % (settings.MEDIA_ROOT, settings.ZIP_FOLDER, filepath)

def get_unique_path(path):
    """
    If a path to a file is already taken, generate a new file path,
    by adding underscores to the file name
    """
    while os.path.exists( fullpath(path) ):
        parts = path.split(".")
        if len(parts) > 1:
            parts[-2] += "_"
        path = ".".join( parts )
    return path