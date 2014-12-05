#Author: s0831408
from __future__ import division
from Robot import *
from Group import *
#from Auctioneer import *
from Vent import *
from random import randint

import math
import random
import matplotlib.pyplot as mp

""" This is the main class which sets up the environment, drops the robots,
	and begins the interactions of objects to obtain a final position."""

#-----------Initialise Variables------------------
numGroups = 3		#Number of groups of robots
numRobots = 12		#Number of robots
numVents = 3		#Number of vents
seabedSize = 1 		#Size of oceanbed in miles
radius = 0.25		#The distance from centre each robot should be
maxMove = 0.001		#This is the max a robot can move per turn

numRobotsPerGroup = int(numRobots / numGroups)

#Lists to hold the objects of the environment
groupList = []
robotList = []
ventList = []

#==============================PLOT ENVIRONMENT=================================
def plotEnv():
	groupColours = ['Green','Red','Blue']
	mp.axis([0,1,0,1])

	#Plot vents in black (crosses)
	for vent in ventList:
		mp.scatter(vent.getX(), vent.getY(), s=100, marker='x', color='black')

	#Plot each team of robots in a different colour (plot triangles for centroids)
	for i in xrange(numGroups):
		mp.scatter(groupList[i].getX(), groupList[i].getY(), s=60, marker='^',
			color = groupColours[i])
		
		#Plot the formation circle of each group
		circle = mp.Circle((groupList[i].getX(), groupList[i].getY()), 
			radius, color = groupColours[i], fill=False)
		fig = mp.gcf()
		fig.gca().add_artist(circle)

		robots = groupList[i].getGroupRobotIDs()

		for j in xrange(numRobotsPerGroup):
			#Plot robots
			mp.scatter(robotList[robots[j]].getX(), robotList[robots[j]].getY(), 
				s=60, marker='o', color = groupColours[i])
			
			#Plot robot's post
			post = getPost(groupList[i].getX(), groupList[i].getY(),
				robotList[robots[j]].getQuarter())
			mp.scatter(post[0],post[1],s=50, marker ='*',color = groupColours[i])

	mp.show()

#=================================GET POST======================================
def getPost(x, y, seg):
	""" This gets the point the robot should be positioned at, given the quarter
		it is assigned, the radius, and the current centre of the group"""
	#Use trig to get the x and y move size
	post = [0,0]
	xyMove = radius * math.sin(0.785398)

	if seg == 0:
		post[0] = x - xyMove
		post[1] = y + xyMove
	elif seg == 1:
		post[0] = x + xyMove
		post[1] = y + xyMove
	elif seg == 2:
		post[0] = x + xyMove
		post[1] = y - xyMove
	else:
		post[0] = x - xyMove
		post[1] = y - xyMove

	return post

#===============================================================================
def moveToPost(group, robot):
	""" Moves the specified robot within group formation. Returns True if the 
		robot needed to be moved"""
	moved = False
	errorVar = [0.0025, 0.000625]	#The sd of error in x and y movement
	current = [0,0]					#Hold current x and y
	move = [0,0]					#Holds move amount in x and y
	distFromPost = [0,0]			#Holds the x and y distances from R to P
	
	current[0] = robot.getX()
	current[1] = robot.getY()
	
	#Get the point the robot should be at from centre of group & quarter
	post = getPost(group.getX(),group.getY(),robot.getQuarter())
	distFromPost[0] = post[0] - current[0]
	distFromPost[1] = post[1] - current[1]

	#If further away than the error variance, move (up to max amount)
	for i in xrange(2):
		if abs(distFromPost[i]) > 0.001:	#errorVar[i]
			moved = True
			
			#Get movement amount
			if abs(distFromPost[i]) > maxMove:
				#Make sure we have correct sign
				if distFromPost[i] < 0:
					move[i] = -maxMove
				else:
					move[i] = maxMove
			else:
				move[i] = distFromPost[i] 
			
			#Update robot position to new position + error 
			if i == 0:
				error = random.gauss(0, math.sqrt(errorVar[i]))
				robot.setX(current[i] + move[i] + error)
			else:
				error = random.gauss(0, math.sqrt(errorVar[i]))
				robot.setY(current[i] + move[i] + error)

	return moved
#===============================================================================

#-----------------------------Build Environment---------------------------------
#Uniformaly distribute using circles (6 columns, 4 rows - +1 to get away from edges)
colStep = 1/7
rowStep = 1/5


#Create the robots giving unique ID
robot = Robot((1*colStep), (1*rowStep), 0)
robotList.append(robot)
robot = Robot((3*colStep), (1*rowStep), 1)
robotList.append(robot)
robot = Robot((5*colStep), (1*rowStep), 2)
robotList.append(robot)
robot = Robot((2*colStep), (2*rowStep), 3)
robotList.append(robot)
robot = Robot((4*colStep), (2*rowStep), 4)
robotList.append(robot)
robot = Robot((6*colStep), (2*rowStep), 5)
robotList.append(robot)
robot = Robot((1*colStep), (3*rowStep), 6)
robotList.append(robot)
robot = Robot((3*colStep), (3*rowStep), 7)
robotList.append(robot)
robot = Robot((5*colStep), (3*rowStep), 8)
robotList.append(robot)
robot = Robot((2*colStep), (4*rowStep), 9)
robotList.append(robot)
robot = Robot((4*colStep), (4*rowStep), 10)
robotList.append(robot)
robot = Robot((6*colStep), (4*rowStep), 11)
robotList.append(robot)


#Create the vents from the assignment
ventA = Vent(0.5, 0.75, 0.2)
ventB = Vent(0.25, 0.5, 0.3)
ventC = Vent(0.5, 0.25, 0.4)

ventList.append(ventA)
ventList.append(ventB)
ventList.append(ventC)

#Create the three groups
for i in xrange(numGroups):
	group = Group(i)
	groupList.append(group)


#------------------------------Group Robots-------------------------------------
#Using single auction, group robots
botsToAssign = [0,1,2,3,4,5,6,7,8,9,10,11]
for i in xrange(numGroups-1):
	bids = []
	groupMembers = []

	#Elect a seller for robot's to bid to join
	leaderID = randint(0,11)
	#Add to group list and remove from auction
	groupList[i].addRobot(leaderID)
	botsToAssign.remove(leaderID)
	
	#Get bids from all other bidders in auction
	for j in botsToAssign:
		#get distance to seller
		distSeller = math.sqrt((robotList[leaderID].getX()-robotList[j].getX())**2 + 
			(robotList[leaderID].getY()-robotList[j].getY())**2)
		#Append bid and bidder ID
		bids.append([distSeller,j])

	#Auctioneer assigns three lowest bidders the task (group id)
	bids.sort()
	for j in xrange(numRobotsPerGroup-1):
		groupList[i].addRobot(bids[j][1])
		botsToAssign.remove(bids[j][1])

#Assign remaining robots to final group
print botsToAssign
for botID in botsToAssign:
	groupList[(numGroups-1)].addRobot(botID)


#Set initial centroid of group
for group in groupList:
	xs = 0
	ys = 0
	roboIDs = group.getGroupRobotIDs()
	
	for j in roboIDs:
		xs += robotList[j].getX()
		ys += robotList[j].getY()

	group.setX((xs/numRobotsPerGroup))
	group.setY((ys/numRobotsPerGroup))

#Set what quarter each robot is posted to
for group in groupList:
	roboIDs = group.getGroupRobotIDs()

	count = 0
	for j in roboIDs:
		robotList[j].setQuarter(count)
		count += 1


#------------------Initially rally the groups into formation--------------------
plotEnv()
	
#Move robots to correct formation (repeats until all teams have converged)
for group in groupList:
	for i in xrange(numRobotsPerGroup):
		robot = robotList[group.getMemberID(i)]

		positionUpdated = True
		while (positionUpdated == True):
			positionUpdated = moveToPost(group, robot)

plotEnv()

#-------------------------------Begin Move Cycle--------------------------------

for i in xrange(1000):
	#For each robot, get sensor readings
	for robot in robotList:
		readingA = ventList[0].getPDF(robot.getX(),robot.getY())
		readingB = ventList[1].getPDF(robot.getX(),robot.getY())
		readingC = ventList[2].getPDF(robot.getX(),robot.getY())
		sensorReading = readingA + readingB + readingC

		robot.setSensorReading(sensorReading)


	#For each group, bid for which direction to move
	for group in groupList:
		members = group.getGroupRobotIDs()
		bids = []

		for member in members:
			bids.append([robotList[member].getSensorReading(),member])

		bids.sort()
		#Get the quarter for the winning bidder
		direction = robotList[bids[len(bids)-1][1]].getQuarter()

		#Now move the centres
		if direction == 0:
			group.setX(group.getX()-0.001)
			group.setY(group.getY()+0.001)
		elif direction == 1:
			group.setX(group.getX()+0.001)
			group.setY(group.getY()+0.001)
		elif direction == 2:
			group.setX(group.getX()+0.001)
			group.setY(group.getY()-0.001)
		else:
			group.setX(group.getX()-0.001)
			group.setY(group.getY()-0.001)

		#Move robots to correct formation (repeats until converged)
		for i in xrange(numRobotsPerGroup):
			robot = robotList[group.getMemberID(i)]

			positionUpdated = True
			while (positionUpdated == True):
				positionUpdated = moveToPost(group, robot)

print "Group 1: ("+str(groupList[0].getX()) +", "+ str(groupList[0].getY())+")"
print "Group 2: ("+str(groupList[1].getX()) +", "+ str(groupList[1].getY())+")"
print "Group 3: ("+str(groupList[2].getX()) +", "+ str(groupList[2].getY())+")"
plotEnv()