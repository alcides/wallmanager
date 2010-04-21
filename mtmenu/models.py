import sys
from os import environ, path
from subprocess import Popen, PIPE
from settings import *
from cStringIO import StringIO
from threading import Thread
from proxy import proxy
from application_running import *
from ui import scatter


# Go back one directory and adds it to sys.path
add_dir = lambda x: sys.path.append(join(abspath(dirname(__file__)), *x))
add_dir(['..'])
add_dir(['..', 'webmanager'])

# Set needed environment variable
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
    
    def execute (self):
        """Executes within a thread"""
        t = Thread(target=self._execute, args=())
        t.start()
        
    def _execute(self):
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
            
        app_boot_file = self.get_boot_file()
        success = False
        
        if app_boot_file:
            
            try:
                command = self.build_command(app_boot_file)
                
                # Starts application process and waits for it to terminate
                process = Popen(command, stdout = PIPE, stderr = PIPE, cwd = self.get_extraction_fullpath())
                
                # hides the main menu and defines the application that is running
                scatter.hide()
                setAppRunning(process)

                # Concatenate output
                output = StringIO()
                for line in process.communicate():
                    output.write(line)

                scatter.show()
                removeAppRunning()
                
                # Save output to database
                self.add_log_entry(output.getvalue())    
                    
                success = True
            except:
                pass
            
        return success
        
    def get_extraction_fullpath(self):
        """Full path to application repository.
        
        It considers the folder name as being the application's ID. The main path
        is setted on settings.py

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
        ApplicationLogProxy.objects.create(application = self, error_description = app_log_text)
            
        # Get all entries associated with this application
        entries = ApplicationLogProxy.objects.filter(application = self).order_by('-datetime')

            
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
        
class UserProxy(User, WallModelsProxy):
    """Extension from User class used by webmanager.
    
    It allows the representation of an user through django models abling it to
    be extended with other locally-used functions"""
    pass


