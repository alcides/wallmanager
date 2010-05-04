import logging
import threading

from datetime import datetime

file_lock = threading.Lock()
LOG_FILENAME = 'web_log.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    
def log(message):
    file_lock.acquire()
    logging.info(message)
    file_lock.release()

def log_app_event(application, event_type):
    message = '[%s] Application %s: %s | Owner: %s\n' % (datetime.today(), event_type, application.name, application.owner.email)
    log(message)
    
def retrieve_contents():
    file_lock.acquire()
    file = open(LOG_FILENAME, 'r')
    contents = file.read()
    file.close()
    file_lock.release()
    return contents
