import os,shutil

from django.conf import settings

def relative(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

def fullpath(filepath):
    return "%s%s/%s" % (settings.MEDIA_ROOT, settings.ZIP_FOLDER, filepath)

def temp_path(filepath):
    return "%s%s/%s" % (settings.MEDIA_ROOT, settings.ZIP_TEMP_FOLDER, filepath)
    
def path_exists(filepath):
    return os.path.exists(filepath)
    
def delete_path(filepath):
    try:
        os.remove(filepath)
    except:
        pass
        
def move_file(src,dst):
    try:
        shutil.move(src,dst)
    except:
        pass
    
def get_unique_path(path):
    """
    If a path to a file is already taken, generate a new file path,
    by adding underscores to the file name
    """
    while path_exists(fullpath(path)):
        parts = path.split(".")
        if len(parts) > 1:
            parts[-2] += "_"
        path = ".".join( parts )
    return path
    
def get_id_path(path,id):
    parts = path.split(".")
    if len(parts) > 1:
        parts[-2] = "user_"+str(id)
    path = ".".join( parts )
    return path
    