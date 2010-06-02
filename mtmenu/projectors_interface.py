
from datetime import datetime, time, timedelta
from threading import Timer

from webmanager.appman.utils import projectors
from models import ScreensaverControlProxy, ProjectorControlProxy, ApplicationProxy
from mtmenu.application_running import is_app_running
from config import PRODUCTION, INACTIVITY_POOL_INTERVAL

from datetime import datetime
from threading import Thread


class Projector_checker():

    def __init__(self):
        #CONTROL VARIABLES
        self.last_activity = datetime.now()
        self.projectors_on = in_schedule()
        self.projectors_down_time = time(0,0,0)
        
        Thread( target=self.last_activity_checker ).start()
        
        
    def is_projectors_on(self):
        if self.projectors_down_time == time(0,0,0):
            self.projectors_on = self.in_schedule()
        return self.projectors_on


    def set_projectors_status(self, status):
        if (status):
            self.projectors_down_time = time(0,0,0)
        else:
            self.projectors_down_time = datetime.now()
        self.projectors_on = status


    def set_last_activity(self, time = None): 
        if time != None:
            self.last_activity = time
        else:
            self.last_activity = datetime.now()
      
        
    def get_projectors_down_duration(self):
        return get_minutes( cast_time_to_timedelta( datetime.now() ) ) - get_minutes( cast_time_to_timedelta(self.projectors_down_time ) )
        
        
    def update_projectors_status(self):
        try:
            dic = projectors.projectors_status()
            for key, value in dic.items():
                if not value == 'ON':
                    self.set_projectors_status(0)
                    return

            self.set_projectors_status(1)                
        except Exception as e:
            print "Projectors status error: %s" % e
    
    
    def last_activity_checker(self):
        self.update_projectors_status()

        diff_min = get_minutes(datetime.now() - self.last_activity())
        screensaver_control = get_first_item(ScreensaverControlProxy.objects.all())        
        projector_control = get_first_item(ProjectorControlProxy.objects.all())
              
        if screensaver_control:
            self.manage_screensaver(screensaver_control, diff_min)
        else:
            print "screensaver time not defined"
        
        if projector_control:
            self.manage_projectors(projector_control, diff_min)           
        else:
            print "projectors inactivity time not defined"


    def manage_screensaver(self, control, minutes):
        inactivity_time = get_minutes( cast_time_to_timedelta( screensaver_control.inactivity_time ) )
        application = ApplicationProxy.objects.filter(id = screensaver_control.application.id)[0]    
        if diff_min > inactivity_time and not is_app_running() and application:
            application.execute(True)


    def manage_projector(self, control, minutes):
        projector_inactivity_time = get_minutes( cast_time_to_timedelta( projector_control.inactivity_time ) )            
        #print "Projector inactivity time = %s\ndiff time = %s\nis_projectors_on = %s" % (projector_inactivity_time, diff_min, is_projectors_on())
        
        if diff_min > projector_inactivity_time and self.is_projectors_on():
            print "projector inactivity time reached"   
            turn_projectors_power(0)     

        
    def turn_projectors_power(self, status):
        try:
            projectors.projectors_power(status)
            set_projectors_status(status)
            print 'projectors turned off'
        except Exception, e:
            print 'Error turning projectors off'
            if not PRODUCTION: 
                set_projectors_status(status)
    
    
    def in_schedule():
        day = datetime.now().weekday()
        projector_control = get_first_item( ProjectorControlProxy.objects.all() )
        if not projector_control:
            return False
         
        if day < 5:
            start = projector_control.startup_week_time
            end = projector_control.shutdown_week_time
        else:
            start = projector_control.startup_weekend_time
            end = projector_control.shutdown_weekend_time

        return is_between(start, end)




########## SCREENSAVER & PROJECTOR

def get_first_item(list):
    for item in list:
        return item
    return None

def cast_time_to_timedelta(instant):
    return timedelta( seconds = instant.hour*60*60 + instant.minute*60 + instant.second )
   

def get_minutes(time):
    return ( time.seconds + time.microseconds/1000000.0) / 60

def is_between(start, end):
    now = datetime.now()
    return (now.hour > start.hour or ( now.hour == start.hour and now.minute > start.minute )) and \
    (now.hour < end.hour or (now.hour == end.hour and now.minute < end.minute))

