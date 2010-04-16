import os


# Returns the absolute path to this file directory joined
# with whatever directories given as arguments
def relative(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


APPS_REPOSITORY_PATH = relative('apps/')
APPS_BOOT_FILENAME = 'boot.bat'


##PROXY CONFIGURATIONS
UDP_IP   = '127.0.0.1'
RECEIVING_PORT = 6000
SENDING_PORT_ONE = 6001
SENDING_PORT_TWO = 3333
MESSAGE  = "Hello, World!"

