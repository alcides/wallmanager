import os

__all__ = ['APPS_REPOSITORY_PATH', 'APPS_BOOT_FILENAME']

# Returns the absolute path to this file directory joined
# with whatever directories given as arguments
def relative(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


APPS_REPOSITORY_PATH = 'c:\\apps\\'
APPS_BOOT_FILENAME = 'boot.bat'