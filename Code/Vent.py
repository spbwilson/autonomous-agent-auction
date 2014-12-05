#Author: s0831408
import math

class Vent(object):
	""" This class represents one of the hydrothermal vents in the task. It has a 
	position and standard deviation. It can be used to get the reading of the
	chemical level by passing it a grid reference, it then sends back the 
	reading at this point. """


	def __init__(self, x, y, sd):
			self._mean = 0
			self._sd = sd
			self._x = x
			self._y = y

	def getMean(self):
		return self._mean

	def getSD(self):
		return self._sd

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def getPDF(self, x, y):
		"""Given a location, calculate value"""
		xSide = ((x - self.getX())**2) / 2*self.getSD()**2
		ySide = ((y - self.getY())**2) / 2*self.getSD()**2
		val = math.exp(-(xSide + ySide))
		return val