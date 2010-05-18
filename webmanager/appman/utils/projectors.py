import urllib
import urllib2

from django.conf import settings


PROJECTOR_IPS = settings.PROJECTOR_IPS or ('192.168.1.254', '192.168.1.253')

class ProjectorManager():

    WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    WEEKEND = ['saturday', 'sunday']
    DAYS = WEEKDAYS + WEEKEND
    ON = 1
    OFF = 0

    def __init__(self,projector_ip):
        self.projector = projector_ip
        self.url = lambda day: 'http://%s/admin/%s.html' % (self.projector, day)
        self.url_main = 'http://%s/main.html' % (self.projector)
    
    #returns true if successfully authenticated
    def login(self):
        url = 'http://%s/index.html' % self.projector
        values = {'DATA1' : 'Administrator',
              'DATA2' : '' }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return 'sts = "2";' in response.read()
        
    def enable(self,day):
        values = {'V1' : '1',
              'SetScheduleFlag' : '1' }
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url(day), data)
        urllib2.urlopen(req)
    
    #power is 1 when ON and 0 when OFF
    def set_time(self,day,hour,mint,power):
        values = {'V1' : '1',
                'SetScheduleFlag' : '',
                'SetScheduleHour' : str(hour),
                'SetScheduleMin' : str(mint),
                'SetScheduleCommand' : '1',
                'SetScheduleParam1' : str(power),
                'ScheduleInfo' : '' }
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url(day), data)
        urllib2.urlopen(req)

    def reset(self,day):
        values = {'V1' : '1',
            'SetScheduleFlag' : '0',
            'A1':'2',
            'V11' : '1',
            'D11' : '1',
            'V12' : '1',
            'D12' : '2' }
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url(day), data)
        urllib2.urlopen(req)
        
    def power_off(self):
        values = {'V2' : '1','D2' : '0'}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url_main, data)
        urllib2.urlopen(req)

    def power_on(self):
        values = {'V1' : '1','D1' : '1'}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url_main, data)
        urllib2.urlopen(req)

def set_projectors_time(week_on, week_off, 
        weekend_on=False, weekend_off=False, 
        klass=ProjectorManager, projector_ips=PROJECTOR_IPS):
    controllers = map(klass, projector_ips)
    weekend_on = weekend_on or week_on
    weekend_off = weekend_off or week_off
    
    for projector in controllers:
        if projector.login():
            for day in projector.DAYS:
                projector.reset(day)
                
                def set_hour(h_on, h_off):
                    projector.set_time(day, h_on[0], h_on[1], projector.ON)
                    projector.set_time(day, h_off[0], h_off[1], projector.OFF)
                    
                if day in projector.WEEKEND:
                    set_hour(weekend_on, weekend_off)
                else:
                    set_hour(week_on, week_off)
                
                projector.enable(day)

#power is 1 when ON and 0 when OFF
def projectors_power(power, klass=ProjectorManager, projector_ips=PROJECTOR_IPS):
    controllers = map(klass, projector_ips)
    for projector in controllers:
        if projector.login():
            if power:
                projector.power_on()
            else:
                projector.power_off()