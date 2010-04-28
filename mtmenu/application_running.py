"""
This module keeps the running application object and provides an interface to kill it.
"""

from subprocess import Popen

__all__ = ['getAppRunning', 'setAppRunning', 'removeAppRunning', 'isAppRunning', 'killAppRunning']

app_running = None

def getAppRunning():
    ''' Returns the running application object '''
    global app_running
    return app_running

def setAppRunning(app):
    ''' Sets the running application object '''
    global app_running
    app_running = app
    
def removeAppRunning():
    ''' Sets the running application to be None'''
    global app_running
    app_running = None
    
def isAppRunning():
    ''' Verifies if is there an application running '''
    global app_running
    return app_running != None

def killAppRunning():
    ''' Kills the running application process '''
    if app_running:
        pid = app_running.pid
        
        import platform
        if platform.system()[:3].lower() == "win":
            Popen("taskkill /F /T /PID %i" % pid, shell=True)
        else:
            app_running.kill()
