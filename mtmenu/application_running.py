"""
This module keeps the running application object and provides an interface to kill it.
"""

from subprocess import Popen

__all__ = ['get_app_running', 'set_app_running', 'remove_app_running', 'is_app_running', 'kill_app_running']

app_running = None

def get_app_running():
    ''' Returns the running application object '''
    global app_running
    return app_running

def set_app_running(app):
    ''' Sets the running application object '''
    global app_running
    app_running = app
    
def remove_app_running():
    ''' Sets the running application to None'''
    global app_running
    app_running = None
    
def is_app_running():
    ''' Verifies if is there an application running '''
    global app_running
    return app_running != None

def kill_app_running():
    ''' Kills the running application process '''
    if app_running:
        pid = app_running.pid
        
        import platform
        if platform.system()[:3].lower() == "win":
            Popen("taskkill /F /T /PID %i" % pid, shell=True)
        else:
            app_running.kill()