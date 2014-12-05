#Author: s0831408

class Robot(object):
	"""This is the robot class which creates robot objects. Each robot object has an
	ID number, an a group number (which is assigned through the auction).
	They are able to send sensor data to the central decision maker (auctioneer)
	and will move as instructed by the winner. The robots can localise in the
	grid, and using their team member's positions, update their own to stay 
	within the correct radius"""

	def __init__(self, x, y, id):
		self._x = x
		self._y = y
		self._id = id
		self._sensor = 0

		#This is the quarter it hold in the group's circle (tl=0,tr=1,br=2,bl=3)
		self._quarterPost = -1

	def getID(self):
		return self._id

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def getSensorReading(self):
		return self._sensor

	def getQuarter(self):
		return self._quarterPost

	def setX(self, x):
		self._x = x
			
	def setY(self, y):
		self._y = y

	def setSensorReading(self, i):
		self._sensor = i

	def setQuarter(self, num):
		self._quarterPost = num