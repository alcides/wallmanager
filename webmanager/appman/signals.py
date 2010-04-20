import os
from shutil import rmtree

from django.db.models import signals
from django.conf import settings
from django.dispatch import dispatcher, Signal
from django.core.mail import send_mail

from appman.models import Application

#Custom signal declarations
extracted_email_signal = Signal(providing_args=["application"])
    
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
        
    
# Signals    

def uncompress(sender, instance, signal, *args, **kwargs):
    """ Deletes the previous version and starts the uncompressing of the file """
    path = get_app_dir(instance)
    remove_dir(path)
    if instance.zipfile:
        from appman.utils.uncompress import UncompressThread
        UncompressThread(sender,instance, path).start()
    
def remove_app(sender, instance, signal, *args, **kwargs):
    """ Deletes the uncompressed folder """    
    if instance.is_extracted:
        remove_dir(get_app_dir(instance))
    remove_file(instance.zipfile)
    remove_file(instance.icon)

def send_mail_when_app_available(sender, **kwargs):
    """ Sends an e-mail message informing the user that the application is ready to be used """
    application = kwargs['application']
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = application.owner.email
    message = 'Your application, ' + application.name + ', has been successfully deployed.'
    send_mail('[WallManager] Application successfully deployed', message, email_from, [email_to])
            
signals.post_save.connect(uncompress, sender=Application)
signals.post_delete.connect(remove_app, sender=Application)
extracted_email_signal.connect(send_mail_when_app_available)