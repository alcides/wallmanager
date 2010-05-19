import sys
sys.path.append('..')
sys.path.append('../webmanager')

from time import sleep

from threading import Timer
from models import ScreensaverControlProxy, ProjectorControlProxy
from datetime import datetime, time, timedelta
from webmanager.appman.utils import projectors

from models import *
from window_manager import *
from config import MAX_ATTEMPTS, SLEEP_SECONDS_BETWEEN_ATTEMPTS, NATIVE_APP_NAMES
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

def get_first_item(list):
    for item in list:
        return item
    return None

def cast_time_to_timedelta(instant):
    return timedelta( seconds = instant.hour*60*60 + instant.minute*60 + instant.second )

def last_activity_checker():
    from mtmenu import last_activity, projector_on    
    last_activity_timer = Timer(30, last_activity_checker)
       
    if last_activity == None:
        last_activity_timer.start()
        return

    diff_min = get_minutes(datetime.now() - last_activity)
    screensaver_control_list = ScreensaverControlProxy.objects.all()
    screensaver_control = get_first_item(screensaver_control_list)
    
    projector_control_list = ProjectorControlProxy.objects.all()
    projector_control = get_first_item(projector_control_list)
    
    if screensaver_control:
        screensaver_inactivity_time = get_minutes( cast_time_to_timedelta( screensaver_control.inactivity_time ) )
        
        if diff_min > screensaver_inactivity_time and not is_app_running():
            print "screensaver #todo remove this print"
            if application:
                application.execute()
    
    if projector_control:
        projector_inactivity_time = get_minutes( cast_time_to_timedelta( projector_control.inactivity_time ) )
        
        if diff_min > projector_inactivity_time and projector_on:
            print "projector #todo remove this print"
            projectors.projectors_power(0)
            projector_on = 0
    
    last_activity_timer.start()
    

def get_minutes(time):
    return ( time.seconds + time.microseconds/1000000.0) / 60

def in_schedule(self):
    from datetime import datetime
    now = datetime.now()
    day = now.weekday()
    if day < 5:
        start = get_first_item( ProjectorControlProxy.objects.all() ).startup_week_time
        end = get_first_item( ProjectorControlProxy.objects.all() ).shutdown_week_time
    else:
        start = get_first_item( ProjectorControlProxy.objects.all() ).startup_weekend_time
        end = get_first_item( ProjectorControlProxy.objects.all() ).shutdown_weekend_time

    if (now.hours > start.hour or ( now.hours == start.hour and now.minutes > start.minute )) and \
    (now.hours < end.hour or (now.hours == end.hour and now.minutes < end.minute)):
        return True
    return False

