import sys
sys.path.append('..')
sys.path.append('../webmanager')

from time import sleep

from models import *
from window_manager import *
from config import MAX_ATTEMPTS, SLEEP_SECONDS_BETWEEN_ATTEMPTS, NATIVE_APP_NAMES, PRODUCTION



def get_applications(cat=None, sort_by_value=False):
    if cat: 
        return get_applications_of_category(cat, sort_by_value)
    else:
        return get_all_applications(sort_by_value)


def get_all_categories():
    return CategoryProxy.objects.all()    

    
def get_all_applications(sort_by_value=False):
    return sort_apps(ApplicationProxy.objects.all(), sort_by_value)


def get_applications_of_category(cat, sort_by_value=False):
        return sort_apps( ApplicationProxy.objects.filter(category = cat), sort_by_value )
    

def exists_category(category_name):
    return len(CategoryProxy.objects.filter(name = category_name)) > 0


def sort_apps(apps, sort_by_value):
    if sort_by_value:
        return sorted(list(apps), key = lambda app: app.value(), reverse= True)
    else:
        return apps.order_by('name')
    
def bring_window_to_front(toApp = False):
    ''' Bring the WallManager window to the front'''
    from mtmenu import self_hwnd
    
    hwnd = None
    
    w = WindowMgr()
    if toApp:
        
        for i in range(MAX_ATTEMPTS):
            # loop for the open windows on the desktop
            for handler, name in w.getWindows():
                if handler != self_hwnd and name not in NATIVE_APP_NAMES:
                    hwnd = handler
                    print 'Changing context to handler %d with name %s' % (handler, name)
                    break
            if hwnd != None:
                break
            sleep(SLEEP_SECONDS_BETWEEN_ATTEMPTS)
        
        print "Got handler", hwnd    
        if hwnd == None:
            hwnd = self_hwnd
    else:
        hwnd = self_hwnd
        for handler, name in w.getWindows():
            if handler != self_hwnd and name not in NATIVE_APP_NAMES:
                print name
                tid, pid = win32process.GetWindowThreadProcessId(handler)
                if PRODUCTION:
                    Popen("taskkill /F /T /PID %i" % pid, shell=True)
                
                print 'killing %s with PID %d' % (name, pid)
        
    w._handle = hwnd
    w.set_foreground()


