from time import sleep

from threading import Timer
from models import ScreensaverControlProxy, ProjectorControlProxy
from datetime import datetime
from webmanager.appman.utils import projectors_power

from models import *
from window_manager import *
from settings import MAX_ATTEMPTS, SLEEP_SECONDS_BETWEEN_ATTEMPTS, NATIVE_APP_NAMES
from mtmenu.application_running import is_app_running

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
    
    w._handle = hwnd
    w.set_foreground()


########## SCREENSAVER & PROJECTOR

def last_activity_checker():    
    last_activity_timer = Timer(30, last_activity_checker)
       
    if last_activity == None:
        last_activity_timer.start()
        print "entrei aqui"
        return

    diff_min = get_minutes(datetime.now() - last_activity)
    screensaver_inactivity_time = get_minutes(ScreensaverControlProxy.objects.all()[0].inactivity_time)
    projector_inactivity_time = get_minutes(ProjectorControlProxy.objects.all()[0].inactivity_time)
    application = ScreensaverControlProxy.objects.all()[0].application
    
    
    if diff_min > screensaver_inactivity_time and not is_app_running():
        if applications:
            application.execute(True)
        
    elif diff_min > projector_inactivity_time and projector_on:
        projectors_power(1)
        projector_on = 0
    
    last_activity_timer.start()
    

def get_minutes(time):
    return (24*60*60*time.days + time.seconds + time.microseconds/1000000.0) / 60