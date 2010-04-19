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
    
def log_application_added(application):
    message = '[' + str(datetime.today()) + '] Application added: ' + application.name + ' | Owner: ' + application.owner.email +'\n'
    log(message)
    
def log_application_deleted(application):
    message = '[' + str(datetime.today()) + '] Application deleted: ' + application.name + ' | Owner: ' + application.owner.email +'\n'
    log(message)
    
def log_application_edited(application):
    message = '[' + str(datetime.today()) + '] Application edited: ' + application.name + ' | Owner: ' + application.owner.email +'\n'
    log_file.log(message)

def log_application_deployed(application):
    message = '[' + str(datetime.today()) + '] Application deployed: ' + application.name + ' | Owner: ' + application.owner.email + '\n'
    log_file.log(message)
    
def log_application_removedfs(application):
    message = '[' + str(datetime.today()) + '] Application removed from file system: ' + application.name + ' | Owner: ' + application.owner.email +'\n'
    log_file.log(message)
