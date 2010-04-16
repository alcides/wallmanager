from os.path import join, exists, isdir
from os import chdir, getcwdu, listdir
from subprocess import Popen, PIPE
import threading

from OpenGL.GLUT import *

from settings import *


__all__ = ['gel_all_apps', 'Application']


def get_all_apps(proxy):
    """Loops through all APPS_REPOSITORY_PATH subdirectories. Takes in 
    consideration that each subdirectory is named after the application ID
    
    (Temporary method while there's no database access)"""
    ids = [name for name in listdir(APPS_REPOSITORY_PATH)
            if isdir(join(APPS_REPOSITORY_PATH, name))]
    
    apps = []
    for id in ids:
        apps.append(Application(id, proxy))
        
    return apps


#class Application (models.Model): TO-DO
class Application( threading.Thread ):
    """Class representing an application.
    
    Arguments:
        id -- Application's ID
    
    NOTE: This is something that should be talked about. Use django models?
    Direct connection to database? What?
    
    http://stackoverflow.com/questions/302651/use-only-some-parts-of-django
    http://jystewart.net/process/2008/02/using-the-django-orm-as-a-standalone-component/
    """
    def __init__(self, id=-1, proxy = 0):
        self.id = id;
        self.proxy = proxy
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            self.proxy.APP_RUNNING = True
            self.execute()
            self.proxy.APP_RUNNING = False
        except:
            pass
        
    def __unicode__(self):
        return u'AppName Nr%s' % self.id
    
    def execute(self):
        """Tries to execute application's batch file. While is executing all
        process output (stdout/stderr) is catched and handled later on
        when the application is terminated.
        
        Arguments:
            id -- Application's ID (obligatory)
            
        Returns:
            True if application is successfuly executed. If no boof file
            is available False is returned
            
        Raises:
            An Exception is raised in case something goes wrong during
            process execution"""
        app_path = self.path()
        app_boot_file = self.boot_file()
        
        success = False
        
        if app_boot_file:
            
            try:
                import platform
                if platform.system()[:3].lower() == "win":
                    command = [app_boot_file]
                else:
                    command = ["bash", app_boot_file]
                
                
                # Starts application process and waits for it to terminate
                process = Popen(command, stdout=PIPE, stderr=PIPE, cwd=app_path)
                
                
                # Application's output should be handle here! 
                for str in process.communicate():
                    print "OUTPUT:\n %s" % str # TO-DO
                    
                success = True
            except:
                raise
            
        return success
        
    def path(self):
        """Full path to application repository. Each application
        directory is named after its ID so 'id' argument is obligatory
        
        Arguments:
            id -- Application's ID (obligatory)
            
        Returns:
            Full path to application repository if exists otherwise
            nothing is returned"""
        full_path = join(APPS_REPOSITORY_PATH, self.id)
        
        if exists(full_path): 
            return full_path
        
    def boot_file(self):
        """Full path to application boot file. Each application
        directory is named after its ID so 'id' argument is obligatory
        
        Arguments:
            id -- Application's ID (obligatory)
            
        Returns:
            Full path to application repository if exists otherwise
            nothing is returned"""
        boot_file = join(self.path(), APPS_BOOT_FILENAME)
        
        if exists(boot_file): 
            return boot_file


    
    
    
