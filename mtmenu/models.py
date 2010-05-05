import sys
from os import environ, path
from subprocess import Popen, PIPE
from mtmenu.settings import *
from cStringIO import StringIO
from threading import Thread
from mtmenu.proxy import proxy
from mtmenu.application_running import set_app_running, remove_app_running, get_app_running
from copy import deepcopy


# Go back one directory and adds it to sys.path
sys.path.append('..')
sys.path.append('../webmanager')

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
            
            
        #hide scatter    
        from mtmenu.ui import cover_window
        cover_window.show()
        
        app_boot_file = self.get_boot_file()
        success = False
        
        if app_boot_file:
            
            try:
                
                self.start_run()
                
                command = self.build_command(app_boot_file)
                
                # Starts application process and waits for it to terminate
                process = Popen(command, stdout = PIPE, stderr = PIPE, cwd = self.get_extraction_fullpath())
                
                # defines the application that is running
                set_app_running(process)

                get_app_running()
                # Concatenate output
                output = StringIO()
                for line in process.communicate():
                    output.write(line)


                remove_app_running()
                cover_window.resume(self)
                
                        
                self.end_run()                
                
                # Save output to database
                self.add_log_entry(output.getvalue())    
                    
                success = True
            except:
                raise
            
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
        
class UserProxy(User, WallModelsProxy):
    """Extension from User class used by webmanager.
    
    It allows the representation of an user through django models abling it to
    be extended with other locally-used functions"""
    pass


