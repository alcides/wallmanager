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
    message = '[' + str(datetime.today()) + '] Application ' + event_type + ': ' + application.name + ' | Owner: ' + application.owner.email +'\n'
    log(message)
