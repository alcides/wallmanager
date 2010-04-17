from os.path import join, dirname, abspath

# Returns the absolute path to this file directory joined
# with whatever directories given as arguments
def relative(*x):
    return join(abspath(dirname(__file__)), *x)


APPS_REPOSITORY_PATH = relative('apps/')
APPS_BOOT_FILENAME = 'boot.bat'
APPS_MAX_LOG_ENTRIES = 3

WALL_DEFAULT_WIDTH = 1024 * 2
WALL_DEFAULT_HEIGHT = 748

