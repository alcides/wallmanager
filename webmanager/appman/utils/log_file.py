import logging
import threading

from datetime import datetime

from django.conf import settings

file_lock = threading.Lock()

class Logger(object):
    """ Logger of application-wide events. """
    def __init__(self, filename):
        self.fname = filename
        logging.basicConfig(filename=self.fname, level=logging.INFO)
    
    def log(self, message):
        file_lock.acquire()
        logging.info(message)
        file_lock.release()
        
    def log_app_event(self, application, event_type):
        message = '[%s] Application %s: %s | Owner: %s\n' % (datetime.today(), event_type, application.name, application.owner.email)
        self.log(message)

    def retrieve_contents(self):
        file_lock.acquire()
        file = open(self.fname, 'r')
        contents = file.read()
        file.close()
        file_lock.release()
        return contents


logger = Logger(settings.LOG_FILENAME)