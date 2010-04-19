import os
from shutil import rmtree
import threading

from django.db.models import signals
from django.conf import settings
from django.dispatch import dispatcher

from appman.utils.unzip import unzip
from appman.models import Application
from datetime import datetime
from appman.utils import log_file

def get_app_dir(app):
    """ Returns the folder where an app is supposed to live """
    return os.path.join(settings.WALL_APP_DIR,str(app.id))

def remove_dir(path):
    """ Removes a certain directory and all things related to that application """
    if os.path.isdir(str(path)):
        try:
            rmtree(str(path), ignore_errors=True)
        except:
            pass
        
def remove_file(file):
    """ Deletes a file held by a FileField from the filesystem. """
    try:
        file.delete(save=True)
    except:
        pass

class UncompressThread(threading.Thread):
    """ Thread that uncompresses a certain zip file."""
    def __init__(self, model, instance, path):
        self.model = model
        self.instance = instance
        self.path = str(path)
        threading.Thread.__init__(self)

    def run(self):
        try:
            un = unzip()
            un.extract( str(self.instance.zipfile.path) , self.path)
            message = '[' + str(datetime.today()) + '] Application deployed: ' + self.instance.name + ' | Owner: ' + self.instance.owner.email + '\n'
            log_file.log(message)
            # Save in Database
            self.model.objects.filter(id=self.instance.id).update(extraction_path=self.path)
        except:
            # Todo email user.
            pass
        
    
# Signals    

def uncompress(sender, instance, signal, *args, **kwargs):
    """ Deletes the previous version and starts the uncompressing of the file """
    path = get_app_dir(instance)
    remove_dir(path)
    if instance.zipfile:
        UncompressThread(sender,instance, path).start()
    
def remove_app(sender, instance, signal, *args, **kwargs):
    """ Deletes the uncompressed folder """    
    if str(instance.extraction_path) != "":
        remove_dir(instance.extraction_path)
        remove_file(instance.zipfile)
        remove_file(instance.icon)
        message = '[' + str(datetime.today()) + '] Application folders and files deleted: ' + instance.name + ' | Owner: ' + instance.owner.email +'\n'
        log_file.log(message)

signals.post_save.connect(uncompress, sender=Application)
signals.post_delete.connect(remove_app, sender=Application)