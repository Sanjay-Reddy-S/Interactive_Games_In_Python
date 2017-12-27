# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using 
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self._tiles=[]
        self._height=height
        self._width=width
        for i in range(width):
            for j in range(height):
                pos=Position(i,j)
                self._tiles.append([pos,False,0])
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x_co=math.floor(pos.getX())
        y_co=math.floor(pos.getY())
        for tile in self._tiles:
            if tile[0].getX()==x_co and tile[0].getY()==y_co:
                tile[1]=True
                tile[2]+=5
                

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        for tile in self._tiles:
            if tile[0].getX()==math.floor(m) and tile[0].getY()==math.floor(n):
                return tile[1]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self._tiles)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        num=0
        for tile in self._tiles:
            if self.isTileCleaned(tile[0].getX(),tile[0].getY()):
                num+=1
        return num        

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        num1=random.random()
        num4=random.random()
        num2=random.randrange(0,self._width)
        num3=random.randrange(0,self._height)
        tile=Position(num1+num2,num4+num3)
        return tile

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x_co=pos.getX()
        y_co=pos.getY()
        if x_co>=self._width or y_co>=self._height or x_co<0 or y_co<0:
            return False
        return True

    def four_neighbors(self, pos):
        """
        Returns horiz/vert neighbors of cell (row, col)
        """
        ans = []
        row=(pos.getX())
        col=(pos.getY())
        if row > 1:
            ans.append((row - 1, col,270))#left
        if row < self._width-1:
            ans.append((row + 1, col,90))#right
        if col > 1:
            ans.append((row, col - 1,180))#down
        if col < self._height-1:
            ans.append((row, col + 1,0))#up
        return ans

    def cost_Tile(self,m,n):
        for tile in self._tiles:
            if tile[0].getX()==math.floor(m) and tile[0].getY()==math.floor(n):
                return tile[2]
            

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self._speed=speed
        self._pos=room.getRandomPosition()
        self._room=room
        self._dir=random.randrange(0,360)
        room.cleanTileAtPosition(self._pos)
                
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self._pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """       
        return self._dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self._pos=Position(position.getX(),position.getY())
        self._room.cleanTileAtPosition(self._pos)

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self._dir=direction

    def getRobotSpeed(self):
        return self._speed

    def getRoom(self):
        return self._room

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 2
class UniformRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos=Position.getNewPosition(Robot.getRobotPosition(self),Robot.getRobotDirection(self),Robot.getRobotSpeed(self))
        room=Robot.getRoom(self)
        ans=room.four_neighbors(pos)
        answ=[]
        for i in ans:
            answ.append([room.cost_Tile(i[0],i[1]),i[2]])  
        min_cost=answ[0]
        for i in answ:
            if i[0]<min_cost[0]:
                min_cost=i 
        if room.isPositionInRoom(pos):
            Robot.setRobotPosition(self,pos)
            Robot.setRobotDirection(self,min_cost[1])
        else:
            Robot.setRobotDirection(self,min_cost[1])
# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(UniformRobot, RectangularRoom)

class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos=Position.getNewPosition(Robot.getRobotPosition(self),Robot.getRobotDirection(self),Robot.getRobotSpeed(self))
        room=Robot.getRoom(self)
        if room.isPositionInRoom(pos):
            Robot.setRobotPosition(self,pos)
        else:
            Robot.setRobotDirection(self,random.randrange(0,360))
# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    def done(min_coverage,room):
        fraction=float(room.getNumCleanedTiles())/room.getNumTiles()
        if fraction>=min_coverage:
            return True
        return False

    mean=0.0
    for i in range(num_trials):
        num=0
        room=RectangularRoom(width,height)
        r1=StandardRobot(room,speed)
        while (not done(min_coverage,room)):
            r1.updatePositionAndClean()
            num+=1
        mean+=num
    mean/=num_trials    
    return mean

    
# Uncomment this line to see how much your simulation takes on average
#print  runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)



# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos=Position.getNewPosition(Robot.getRobotPosition(self),Robot.getRobotDirection(self),Robot.getRobotSpeed(self))
        Rroom=Robot.getRoom(self)
        if Rroom.isPositionInRoom(pos):
            Robot.setRobotPosition(self,pos)
            Robot.setRobotDirection(self,random.randrange(0,360))
        else:
            Robot.setRobotDirection(self,random.randrange(0,360))
# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(RandomWalkRobot, RectangularRoom)


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#showPlot1("Sanjay","Reddy","S")

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
