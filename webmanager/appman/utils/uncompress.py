import os
import threading

from django.conf import settings

from appman.utils.unzip import unzip
from appman.signals import extracted_email_signal

class UncompressThread(threading.Thread):
    """ Thread that uncompresses a certain zip file."""
    def __init__(self, model, instance, path):
        self.model = model
        self.instance = instance
        self.path = str(path)
        threading.Thread.__init__(self)

    def run(self):
        
        if not os.path.isdir(settings.WALL_APP_DIR):
            os.mkdir(settings.WALL_APP_DIR)
        
        try:
            un = unzip()
            un.extract( str(self.instance.zipfile.path) , self.path)
            extracted = os.path.exists(os.path.join(self.path, 'boot.bat'))
        except IOError:
            extracted = False
    
        if extracted:
            extracted_email_signal.send(sender=self, application=self.instance)
            try:
                self.model.objects.filter(id=self.instance.id).update(is_extracted=True)
            except:
                # TODO: Remove: SQLite3 related
                pass
        else:
            extracted_email_signal.send(sender=self, application=self.instance, success=False)