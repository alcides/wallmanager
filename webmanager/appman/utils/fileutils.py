import os
import shutil

from django.conf import settings

def relative(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

def fullpath(filepath, media_subfolder=None):
    """ Given an application file, returns the absolute path."""
    if not media_subfolder:
        media_subfolder = settings.ZIP_FOLDER
    return "%s%s/%s" % (settings.MEDIA_ROOT, media_subfolder, filepath)
    
def delete_path(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        
def move_file(src,dst):
    shutil.move(src,dst)
    
def get_unique_path(path):
    """
    If a path to a file is already taken, generate a new file path,
    by adding underscores to the file name
    """
    while os.path.exists(fullpath(path)):
        parts = path.split(".")
        if len(parts) > 1:
            parts[-2] += "_"
        path = ".".join( parts )
    return path
    
def get_filename_for_id(id):
    " Returns a filename unique for each user"
    return "user_%s.zip" % id     