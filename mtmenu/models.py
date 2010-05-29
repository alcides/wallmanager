import sys
from os import environ, path
from subprocess import Popen, PIPE
from config import APPS_REPOSITORY_PATH, APPS_BOOT_FILENAME, PRODUCTION
from cStringIO import StringIO
from threading import Thread
from mtmenu.application_running import set_app_running, remove_app_running, get_app_running, is_app_running, get_app_mutex
# Go back one directory and adds it to sys.path
sys.path.append('..')
sys.path.append('../webmanager')

# Set needed environment variable
if PRODUCTION:
    environ['DJANGO_SETTINGS_MODULE'] = 'webmanager.settings-prod'
else:
    environ['DJANGO_SETTINGS_MODULE'] = 'webmanager.settings'

# webmanager models can now be imported
from webmanager.appman import models
from django.contrib.auth.models import User

class WallModelsProxy ():
    """This is an abstraction to be used by all models extended from appman"""
    class Meta:
        proxy = True
        app_label = 'appman'


class ApplicationProxy(models.Application, WallModelsProxy):    
    """Extension for Application class used by webmanager.
    
    It allows the representation of an application through django models abling it to
    be extended with other locally-used functions like execute()"""
    
    def execute (self, is_screensaver=False):
        """Executes within a thread"""
        app_mutex = get_app_mutex()
        if app_mutex.testandset():
            t = Thread( target=self._execute, args=( is_screensaver, ) )
            t.start()
        else:
            print "some application is already running"
        
    def _execute(self, is_screensaver):
        """Tries to execute application's batch file.
        
        While is executing all process output (stdout/stderr) is catched 
        and handled later on when the application is terminated. 
        
        This method blocks until the application exits. Use run() instead.

        Returns:
            True if application is successfuly executed. If no boot file
            is available False is returned
            
        Raises:
            An Exception is raised in case something goes wrong during
            process execution"""
            
            
        #hide scatter
        
        print 'i am in %s' % self.name
        
        if (is_app_running()):
            get_app_mutex().unlock()
            return False
        
        set_app_running(True)
          
        from mtmenu import cover_window
        cover_window.show()
        
        app_boot_file = self.get_boot_file()
        success = False
        
        if app_boot_file:
            
            try:
                
                self.start_run()
                
                command = self.build_command(app_boot_file)
                
                # Starts application process and waits for it to terminate
                process = Popen(command, stdout = PIPE, stderr = PIPE, cwd = self.get_extraction_fullpath(), shell = False)
                
                # defines the application that is running
                set_app_running(process)
                
                print "Running application: %s" % self.name
                
                from utils import bring_window_to_front
                bring_window_to_front(True)
                
                # Concatenate output
                output = StringIO()
                for line in process.communicate():
                    output.write(line)


                remove_app_running()
                
                cover_window.resume(self, is_screensaver)
                        
                self.end_run()                
                
                # Save output to database
                self.add_log_entry(output.getvalue())    
                    
                success = True
                print "Application terminated"
            except Exception, e: #Pokemon
                print "EXCEPTION RUNNING APPLICATION"
                print e
        else:
            print "Could not run app because no boot file"
        print 'i am unlocking %s' % self.name
        get_app_mutex().unlock()
        
        return success
        
        
    def get_extraction_fullpath(self):
        """Full path to application repository.
        
        It considers the folder name as being the application's ID. The main path
        is setted on config.py

        Returns:
            Full path to application repository if exists otherwise
            returns empty string"""
        full_path = path.join(APPS_REPOSITORY_PATH, str(self.id))
        
        if path.exists(full_path): 
            return full_path
        else:
            return ""
        
    def build_command(self, boot_file):
        """ Returns the command to be executed on the shell """
        import platform
        if platform.system()[:3].lower() == "win":
            return [boot_file]
        else:
            return ["bash", boot_file]    
        
    def get_boot_file(self):
        """Full path to application boot file.
        
        Returns:
            Full path to application boot file if exists otherwise
            returns nothing"""
        boot_file = path.join(self.get_extraction_fullpath(), APPS_BOOT_FILENAME)
        
        if path.exists(boot_file): 
            return boot_file
    
    def add_log_entry(self, app_log_text = '(none)'):

        """Adds an application's log entry.
        
        Always use this method to add new log entries to
        keep all logic at the same place.
        
        Parameters:
            - app_log_text: Debug text to be added"""
            
        # Adds entry to database
        log = ApplicationLogProxy.objects.create(application = self, error_description = app_log_text)
        
    def vote(self, like):
        if like:
            self.likes = self.likes + 1
        else:
            self.dislikes = self.dislikes + 1
        self.save()
            
    def start_run(self):
        self.is_running = True
        self.save(False, True)
        
    def end_run(self):
        self.is_running = False
        self.add_run()
        self.save(False, True)
        
    def add_run(self):
        self.runs = self.runs + 1

            
class CategoryProxy(models.Category, WallModelsProxy):
    """Extension from Category class used by webmanager.
    
    It allows the representation of a category through django models enabling it to
    be extended with other locally-used functions"""
    pass


class ApplicationLogProxy(models.ApplicationLog, WallModelsProxy):
    """Extension from ApplicationLog class used by webmanager.
    
    It allows the representation of an application log through django models abling it to
    be extended with other locally-used functions"""
    pass


# Connect post_save signal to web-side signals
from django.db.models import signals
from webmanager.appman.signals import remove_extra_logs
signals.post_save.connect(remove_extra_logs, sender=ApplicationLogProxy)


class UserProxy(User, WallModelsProxy):
    """Extension from User class used by webmanager.
    
    It allows the representation of an user through django models abling it to
    be extended with other locally-used functions"""
    pass


class ScreensaverControlProxy (models.ScreensaverControl, WallModelsProxy):
    """Extension from ScreensaverControl class used by webmanager.
    
    It allows the representation of an user through django models abling it to
    be extended with other locally-used functions"""
    pass


class ProjectorControlProxy (models.ProjectorControl, WallModelsProxy):
    """Extension from ProjectorControl class used by webmanager.
    
    It allows the representation of an user through django models abling it to
    be extended with other locally-used functions"""
    pass


def _execute(name):
      
    print 'i am in %s' % name

    from time import sleep
    sleep(5)
    print 'i am unlocking %s' % name
    
    app_mutex.unlock()
    
    


if __name__ == "__main__":
    
    t = Thread(target=app_mutex.lock, args=(_execute, ("1",) ) )
    t.start()
    
    t2 = Thread(target=app_mutex.lock, args=(_execute,("2",)))
    t2.start()
    