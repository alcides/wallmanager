import os
from shutil import rmtree
import threading

from django.db.models import signals
from django.conf import settings
from django.dispatch import dispatcher
from django.core.mail import send_mail

from appman.utils.unzip import unzip
from appman.models import Application

import django.dispatch

#Custom signal declarations
email_signal = django.dispatch.Signal(providing_args=["application"])
    
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
            # Save in Database
            self.model.objects.filter(id=self.instance.id).update(extraction_path=self.path)
            email_signal.send(sender=self, application=self.instance)
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
        

def send_mail_when_app_available(sender, **kwargs):
    """ Sends an e-mail message informing the user that the application is ready to be used """
    application = kwargs['application']
    application_name = application.name
    application_owner = application.owner
    email_from = 'wallmanager@dei.uc.pt'
    email_to = application_owner.email
    message = 'Your application, ' + application_name + ', has been successfully deployed.'
    send_mail('[WallManager] Application successfully deployed', message, email_from, [email_to])
            
signals.post_save.connect(uncompress, sender=Application)
signals.post_delete.connect(remove_app, sender=Application)
email_signal.connect(send_mail_when_app_available)
