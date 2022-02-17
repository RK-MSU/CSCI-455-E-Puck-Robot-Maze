'''
River Kelly
Kyler Gappa
CSCI-455: Embedded Systems (Robotics)
Assignment 01 - Webots E-Puck Robot Maze
Spring 2022
'''

from controller import Robot
from enum import Enum
import math

TIME_STEP = 64
MAX_SPEED = 6.28

# --------------------------------------------------------------------

# Direction Class
class Direction(Enum):
    North = 'North'
    South = 'South'
    East = 'East'
    West = 'West'
    Left = 'Left'
    Right = 'Right'

# RobotState Class
class RobotState(Enum):
    FindWall = 'Find Wall'
    MountWall = 'Mount Wall'
    FollowWall = 'Follow Wall - Right-Hand Rule'
    TurnCorner = 'Turn Corner'
    CorrectTurn = 'CorrectTurn'

# --------------------------------------------------------------------

# EPuck (Robot) Class
class EPuck:

    # properties
    robot = None
    ps = []
    leftMotor = None
    rightMotor = None
    leftMotorSensor = None
    rightMotorSensor = None
    compass = None
    touchSensor = None

    # constructor
    def __init__(self, robot):
        self.robot = robot
        # get and enable ultrasound sensors
        for i in range(8):
            sensorName = "ps{!s}".format(i)
            sensor = self.robot.getDevice(sensorName)
            sensor.enable(TIME_STEP)
            self.ps.append(sensor)
        # Setup left and right motors
        self.leftMotor = self.robot.getDevice('left wheel motor')
        self.rightMotor = self.robot.getDevice('right wheel motor')
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        # wheel sensors
        self.leftMotorSensor = self.robot.getDevice('left wheel sensor')
        self.rightMotorSensor = self.robot.getDevice('left wheel sensor')
        self.leftMotorSensor.enable(TIME_STEP)
        self.rightMotorSensor.enable(TIME_STEP)
        # compass
        self.compass = self.robot.getDevice('compass')
        self.compass.enable(TIME_STEP)
        # touch sensor
        self.touchSensor = self.robot.getDevice('touch sensor')
        self.touchSensor.enable(TIME_STEP)

    # step()
    # ----------------------------------------------------------------
    # TODO: add description
    def step(self):
        if self.robot.step(TIME_STEP) != -1:
            return True
        return False

    # bearing (property)
    # ----------------------------------------------------------------
    # Returns the degree (0-360) which the robot is facing
    @property
    def bearing(self):
        dir = self.compass.getValues()
        if math.isnan(dir[0]):
            return None
        rad = math.atan2(dir[0], dir[1])
        bearing = (rad - 1.5708) / math.pi * 180.0
        if bearing < 0.0:
            bearing = bearing + 360.0
        return bearing

    # direction (property)
    # ----------------------------------------------------------------
    # returns the compass pole (North, South, East, or West) which the
    # robot is currently facing basesd on the bearing
    @property
    def direction(self):
        bearing = self.bearing
        if bearing is None:
            return None
        if 45 < bearing <= 135:
            return Direction.West
        elif 135 < bearing <= 225:
            return Direction.South
        elif 225 < bearing <= 315:
            return Direction.East
        else:
            return Direction.North

    # setSpeed()
    # ----------------------------------------------------------------
    # Set the robots wheel speed based on a percentage of the
    # MAX_SPEED.
    #
    # Example: self.setSpeed(50)
    # sets wheel velocity to 50% of the MAX_SPEED
    # ----------------------------------------------------------------
    def setSpeed(self, speed):
        speed = MAX_SPEED * (speed / 100)
        self.leftMotor.setVelocity(speed)
        self.rightMotor.setVelocity(speed)

    # setLeftWheelSpeed()
    def setLeftWheelSpeed(self, speed):
        speed = MAX_SPEED * (speed / 100)
        self.leftMotor.setVelocity(speed)

    # setRightWheelSpeed()
    def setRightWheelSpeed(self, speed):
        speed = MAX_SPEED * (speed / 100)
        self.rightMotor.setVelocity(speed)

    # travel()
    # ----------------------------------------------------------------
    # TODO: add description
    def travel(self):
        pass

# END EPuck Class

print("Starting")
robot = EPuck(Robot())
while robot.step():
    robot.travel()
print("GAME OVER")

# END
