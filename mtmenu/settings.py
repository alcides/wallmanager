from os.path import join, dirname, abspath

# Returns the absolute path to this file directory joined
# with whatever directories given as arguments
def relative(*x):
    return join(abspath(dirname(__file__)), *x)


APPS_REPOSITORY_PATH = relative('apps/')
APPS_BOOT_FILENAME = 'boot.bat'


##PROXY CONFIGURATIONS
UDP_IP   = '127.0.0.1'
RECEIVING_PORT = 6000
SENDING_PORT_ONE = 6001
SENDING_PORT_TWO = 3333
MESSAGE  = "Hello, World!"
APPS_MAX_LOG_ENTRIES = 3

WALL_DEFAULT_WIDTH = 1024 * 2
WALL_DEFAULT_HEIGHT = 748

