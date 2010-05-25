
from datetime import datetime, time, timedelta
from threading import Timer

from webmanager.appman.utils import projectors
from models import ScreensaverControlProxy, ProjectorControlProxy, ApplicationProxy
from mtmenu.application_running import is_app_running
from config import PRODUCTION, INACTIVITY_POOL_INTERVAL

from datetime import datetime

def is_projectors_on():
    global projectors_on
    return projectors_on

def set_projectors_on(bool):
    global projectors_on
    projectors_on = bool
    

def get_last_activity():
    global last_activity
    return last_activity

def set_last_activity(time = None):
    global last_activity
    
    if time != None:
        last_activity = time
    else:
        last_activity = datetime.now()
        

def get_projectors_down_duration():
    global projectors_down_time
    return get_minutes( cast_time_to_timedelta( datetime.now() ) ) - get_minutes( cast_time_to_timedelta(projectors_down_time ) )

########## SCREENSAVER & PROJECTOR

def get_first_item(list):
    for item in list:
        return item
    return None

def cast_time_to_timedelta(instant):
    return timedelta( seconds = instant.hour*60*60 + instant.minute*60 + instant.second )

def last_activity_checker():
    last_activity_timer = Timer(INACTIVITY_POOL_INTERVAL, last_activity_checker)
    
    last_active = get_last_activity()
       
    if last_active == None:
        last_activity_timer.start()
        return

    diff_min = get_minutes(datetime.now() - last_active)
    screensaver_control_list = ScreensaverControlProxy.objects.all()
    screensaver_control = get_first_item(screensaver_control_list)
    
    projector_control_list = ProjectorControlProxy.objects.all()
    projector_control = get_first_item(projector_control_list)
    
    if screensaver_control:
        screensaver_inactivity_time = get_minutes( cast_time_to_timedelta( screensaver_control.inactivity_time ) )
        application = ApplicationProxy.objects.filter(id = screensaver_control.application.id)[0]        
        
        if diff_min > screensaver_inactivity_time and not is_app_running():
            print "screensaver inactivity time reached"
            if application:
                application.execute(True)
    else:
        print "screensaver time not defined"
    
    if projector_control:
        projector_inactivity_time = get_minutes( cast_time_to_timedelta( projector_control.inactivity_time ) )
        
        print "Projector inactivity time = %s\ndiff time = %s\nis_projectors_on = %s" % (projector_inactivity_time, diff_min, is_projectors_on())
        
        if diff_min > projector_inactivity_time and is_projectors_on():
            print "projector inactivity time reached"
            try:
                projectors.projectors_power(0)
                set_projectors_on(False)
                projectors_down_time = datetime.now()
                print 'projectors turned off'
            except Exception, e:
                print 'Error turning projectors off'
                print e
                if not PRODUCTION: 
                    set_projectors_on(False)
    else:
        print "projectors inactivity time not defined"
        
    last_activity_timer.start()
    

def get_minutes(time):
    return ( time.seconds + time.microseconds/1000000.0) / 60

def is_between(start, end):
    now = datetime.now()
    return (now.hour > start.hour or ( now.hour == start.hour and now.minute > start.minute )) and \
    (now.hour < end.hour or (now.hour == end.hour and now.minute < end.minute))

def in_schedule():
    from datetime import datetime, time
    now = datetime.now()
    day = now.weekday()
    projector_control = get_first_item( ProjectorControlProxy.objects.all() )
    if not projector_control:
        return False
     
    if day < 5:
        start = projector_control.startup_week_time
        end = projector_control.shutdown_week_time
    else:
        start = projector_control.startup_weekend_time
        end = projector_control.shutdown_weekend_time

    # Considering ending before start
    if start.hour > end.hour:
        tmp_end = time(23,59,59)
        tmp_start = time(0,0,0)
        
        return is_between(start, tmp_end) or is_between(tmp_start, end)
    else:
        return is_between(start, end)


#CONTROL VARIABLES
last_activity = datetime.now()
projectors_on = in_schedule()

projectors_down_time = time(0,0,0)