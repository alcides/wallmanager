'''
Created on 2010/04/16

@author: disbeat
'''
from threading import Thread
from proxy import proxy
from ui import scatter


app_running = None

def setAppRunning(app):
    global app_running
    app_running = app
    
def getAppRunning():
    global app_running
    return app_running

def removeAppRunning():
    global app_running
    app_running = None
    
    

#class AppRunner(Thread):
#    
#    This thread receives and runs an application
#    
#
#    def run(self):
#        try:
#            proxy.APP_RUNNING = True
#            scatter.hide()            
#            
#            log = self.app.execute()
#            
#            # TODO: vote popup here
#            
#            # TODO: save log here 
#            for str in log:
#                print "OUTPUT:\n %s" % str # TO-DO
#            
#            scatter.show()    
#            proxy.APP_RUNNING = False
#        except:
#            raise
#
#    def __init__(self, application):
#         Receives an application instance and the TUIOproxy
#        
#        self.app = application
#        Thread.__init__(self)
