import os
from appman.utils.projectors import *
import threading

class ProjectorsThread(threading.Thread):
	""" Thread that makes the conncetion to the rojectors."""
	def __init__(self,proj):
		threading.Thread.__init__(self)
		times = map(self.to_array,[proj.startup_week_time,proj.shutdown_week_time,
				proj.startup_weekend_time,proj.shutdown_weekend_time])
		self.week_on, self.week_off, self.weekend_on, self.weekend_off = times

	def to_array(self,date):
		return [date.hour,date.minute]
		
	def run(self):
		set_projectors_time(self.week_on, self.week_off, self.weekend_on, self.weekend_off)

