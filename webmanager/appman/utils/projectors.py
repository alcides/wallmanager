import urllib
import urllib2

class ProjectorsManager():

	def __init__(self,projector):
		self.days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
		if projector == 1:
			self.url = lambda day : 'http://192.168.1.254/admin/%s.html' % (day)
		else: #projector == 2
			self.url = lambda day : 'http://192.168.1.253/admin/%s.html' % (day)
	
	#returns true if successfully authenticated
	def login(self):
		url = 'http://192.168.1.254/index.html'
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
