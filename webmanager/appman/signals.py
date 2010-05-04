import os
from shutil import rmtree

from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import dispatcher, Signal
from django.core.mail import send_mail

from appman.models import Application, WallManager
from appman.utils.other import get_contact_admin_email

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
    
def check_if_contact_admin(sender, instance, signal, *args, **kwargs):
    """ Checks if the removed user is the contact admin (and if so, sets the contact admin to null) """
    contact_admin_email = get_contact_admin_email()
    if (instance.email == contact_admin_email):
        try:
            wallmanager_instance = WallManager.objects.all()[0]
            wallmanager_instance.contact = ""
            wallmanager_instance.save()
        except IndexError:
            pass
            
signals.post_save.connect(uncompress, sender=Application)
signals.post_delete.connect(remove_app, sender=Application)
signals.post_delete.connect(check_if_contact_admin, sender=User)
extracted_email_signal.connect(send_mail_when_app_available)