import os
from shutil import rmtree
from smtplib import SMTPException

from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import dispatcher, Signal
from django.core.mail import send_mail

from appman.models import Application, ApplicationLog, WallManager
from appman.models import Application, WallManager

from appman.models import Application, ApplicationLog, WallManager
from appman.utils.unzip import unzip
from appman.utils.uncompress import UncompressThread
from appman.utils.log_file import logger
from appman.utils import get_contact_admin_email

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
        
def remove_file(file, save=True):
    """ Deletes a file held by a FileField from the filesystem. """
    try:
        file.delete(save)
    except:
        pass
        
    
# Signals    

def uncompress_file(sender, instance, signal, *args, **kwargs):
    """ Deletes the previous version and starts the uncompressing of the file """
    application_was_added = kwargs['created']
    if application_was_added:
        logger.log_app_event(instance, 'added')
    else:
        logger.log_app_event(instance, 'edited')
    
    path = get_app_dir(instance)
    remove_dir(path)
    if instance.zipfile:
        from appman.utils.uncompress import UncompressThread
        UncompressThread(sender,instance, path, extracted_email_signal).start()
    
def remove_app(sender, instance, signal, *args, **kwargs):
    """ Deletes the uncompressed folder """
    logger.log_app_event(instance, 'deleted')
    
    if instance.is_extracted and not instance.is_running:
        remove_dir(get_app_dir(instance))
    remove_file(instance.zipfile, False)
    remove_file(instance.icon, False)
    logger.log_app_event(instance, 'removed from filesystem')

def send_mail_when_app_available(sender, **kwargs):
    """ Sends an e-mail message informing the user that the application is ready to be used """
    if 'success' in kwargs:
        success = kwargs['success']
    else:
        success = True
    application = kwargs['application']
    logger.log_app_event(application, 'deployed')
    
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = application.owner.email
    if success:
        message = 'Your application, %s, has been successfully deployed.' % application.name
        subject = '[WallManager] Application successfully deployed'
    else:
        message = """Your application, %s, was not deployed. \n
        Please check if the zipfile is valid, contains a boot.bat \n
        and follows the technical guidelines.""" % application.name
        subject = '[WallManager] Error deploying application.'
    try: 
        send_mail(subject, message, email_from, [email_to])
    except SMTPException:
        application.owner.message_set.create(message = message)
        
    
def remove_extra_logs(sender, **kwargs):
    """ Removes logs after a certain limit by Application. """
    app = kwargs['instance'].application
    for log in ApplicationLog.objects.filter(application=app).order_by('-datetime')[settings.APPS_MAX_LOG_ENTRIES:]:
        log.delete()
    
def check_if_contact_admin(sender, instance, signal, *args, **kwargs):
    """ Checks if the removed user is the contact admin (and if so, sets the contact admin to null) """
    contact_admin_email = get_contact_admin_email()
    if instance.email == contact_admin_email:
        try:
            wallmanager_instance = WallManager.objects.all()[0]
            wallmanager_instance.contact = ""
            wallmanager_instance.save()
        except IndexError:
            pass
            
signals.post_save.connect(uncompress_file, sender=Application)
signals.post_save.connect(remove_extra_logs, sender=ApplicationLog)
signals.post_delete.connect(remove_app, sender=Application)
signals.post_delete.connect(check_if_contact_admin, sender=User)

extracted_email_signal.connect(send_mail_when_app_available)
