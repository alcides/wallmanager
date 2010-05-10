import os
from appman.utils.projectors import *
import threading

class ProjectorsThread(threading.Thread):
	""" Thread that makes the conncetion to the rojectors."""
	def __init__(self,proj):
		threading.Thread.__init__(self)
		self.week_on = proj.startup_week_time
		self.week_off = proj.shutdown_week_time
		self.weekend_on = proj.startup_weekend_time
		self.weekend_off = proj.shutdown_weekend_time

	def run(self):
		if self.week_on == self.weekend_on and self.week_off == self.weekend_off: 
			set_projectors_time(self.week_on, self.week_off)
		else:
			set_projectors_time(self.week_on, self.week_off, self.weekend_on, self.weekend_off)

