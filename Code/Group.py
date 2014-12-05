#Author: s0831408

class Group(object):
	""" This hold the IDs of the robots in the group and the centroid postion of the
	group. """

	def __init__(self, i):
		self._groupNo = i
		self._x = 0
		self._y = 0
		self._groupRobotList = []

	def getGroupNo(self):
		return self._groupNo

	def getGroupRobotIDs(self):
		return self._groupRobotList

	def getMemberID(self, i):
		return self._groupRobotList[i]

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def setX(self, x):
		self._x = x

	def setY(self, y):
		self._y = y

	def addRobot(self, id):
		self._groupRobotList.append(id)

