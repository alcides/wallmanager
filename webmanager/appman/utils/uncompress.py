import os
import shutil
import threading

from django.conf import settings

import appman.utils.unzip as unzip
from appman.utils.log_file import logger

class UncompressThread(threading.Thread):
    """ Thread that uncompresses a certain zip file."""
    def __init__(self, model, instance, path, signal):
        self.model = model
        self.instance = instance
        self.path = str(path)
        self.signal = signal
        threading.Thread.__init__(self)

    def post_signal(self, success=True ):
        if self.signal:
            self.signal.send(sender=self, application=self.instance, success=success)
            
    def prepare_folder(self):
        if not os.path.isdir(settings.WALL_APP_DIR):
            os.mkdir(settings.WALL_APP_DIR)
            
    def extract_file(self):
        try:
            un = unzip.unzip()
            un.extract(str(self.instance.zipfile.path) , self.path)
            return os.path.exists(os.path.join(self.path, 'boot.bat'))
        except unzip.zipfile.BadZipfile, e:
            logger.log_app_event(self.instance, "BadZipfile:" + str(e))
            return False
        except IOError, e:
            logger.log_app_event(self.instance, "IO:" + str(e))
            return False
            
    def safe_call(self, fun):
        try:
            return fun()
        except Exception, e:
            if settings.DATABASE_ENGINE == 'sqlite3':
                if settings.DEBUG:
                    print "Concurrent Exception (SQLite-related)", e
                return False
            else:
                # Raise exception normally
                raise e
            
    def run(self):
        self.prepare_folder()
        extracted = self.extract_file()
        
        if extracted:
            self.post_signal()
            
            def update_extracted():
                self.model.objects.filter(id=self.instance.id).update(is_extracted=True)
            self.safe_call(update_extracted)
        else:
            shutil.rmtree(self.path)
            
            def delete_extracted():
                self.model.objects.filter(id=self.instance.id)
            self.safe_call(delete_extracted)
            
            self.post_signal(False)