import logging
import threading

file_lock = threading.Lock()
LOG_FILENAME = 'web_log.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    
def log(message):
    file_lock.acquire()
    logging.info(message)
    file_lock.release()