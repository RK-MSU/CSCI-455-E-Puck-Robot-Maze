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
    FollowWall = 'Follow Wall'
    TurnCorner = 'Turn Corner'
    CorrectTurn = 'CorrectTurn'
    GameOver = 'Game Over'

class HandRule(Enum):
    Left = "Left Hand Rule"
    Right = "Right Hand Rule"

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

    _state = RobotState.FindWall
    hand_rule = HandRule.Right

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

    def printSensorValues(self):
        
        front_left = self.ps[7].getValue()
        front_right = self.ps[0].getValue()
        corner_right = self.ps[1].getValue()
        corner_left = self.ps[6].getValue()
        side_right = self.ps[2].getValue()
        side_left = self.ps[5].getValue()
        back_right = self.ps[3].getValue()
        back_left = self.ps[4].getValue()

        TBL_END = "-------------------------------------------------------------------------------"
        TBL_SPACER = "|{!s:-^8}|{!s:-^8}|{!s:-^10}|{!s:-^9}|{!s:-^9}|{!s:-^10}|{!s:-^8}|{!s:-^8}|"
        TBL_HEADER = "|{!s:^8}|{!s:^8}|{!s:^10}|{!s:^9}|{!s:^9}|{!s:^10}|{!s:^8}|{!s:^8}|"
        TBL_ROW = "|{:^8.1f}|{:^8.1f}|{:^10.1f}|{:^9.1f}|{:^9.1f}|{:^10.1f}|{:^8.1f}|{:^8.1f}|"
        TABLE_STR = TBL_END + "\n" +TBL_HEADER + "\n" + TBL_SPACER + "\n" + TBL_ROW + "\n" + TBL_END + "\n"
        
        STR = TABLE_STR.format(
            "L-Back", "L-Side", "L-Corner", "L-Front", "R-Front", "R-Corner", "R-Side", "R-Back",
            '', '', '', '', '', '', '', '',
            back_left, side_left, corner_left, front_left, front_right, corner_right, side_right, back_right)
        
        print(STR)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        print("Switching RobotState:\n---------------------\n To: '{!s}' - From: '{!s}'\n".format(state.value, self.state.value))
        self._state = state


    # travel()
    # ----------------------------------------------------------------
    # TODO: add description
    def travel(self):
        front_left = self.ps[7].getValue()
        front_right = self.ps[0].getValue()
        corner_right = self.ps[1].getValue()
        corner_left = self.ps[6].getValue()
        side_right = self.ps[2].getValue()
        side_left = self.ps[5].getValue()
        back_right = self.ps[3].getValue()
        back_left = self.ps[4].getValue()

        hand_front = None
        opposite_front = None
        hand_corner = None
        hand_side = None

        if self.hand_rule == HandRule.Right:
            hand_front = front_right
            opposite_front = front_left
            hand_corner = corner_right
            hand_side = side_right
        elif self.hand_rule == HandRule.Left:
            hand_front = front_left
            opposite_front = front_right
            hand_corner = corner_left
            hand_side = side_left

        # Game Over?
        touch = self.touchSensor.getValue()
        if not math.isnan(touch) and touch > 0 and opposite_front < 80 and hand_front < 80:
            self.state = RobotState.GameOver
            return

        # print(self.state.name)
        # self.printSensorValues()

        # ------------------------------------------------------------
        # Find Wall
        # ------------------------------------------------------------
        if self.state == RobotState.FindWall:
            self.setSpeed(50)
            if opposite_front > 200 and hand_front > 200:
                self.setSpeed(0)
                self.state = RobotState.MountWall
            elif opposite_front > 150 and hand_front > 150:
                self.setSpeed(5)
            elif opposite_front > 80 and hand_front > 80:
                self.setSpeed(20)
        # ------------------------------------------------------------
        # Mount Wall
        # ------------------------------------------------------------
        elif self.state == RobotState.MountWall:
            self.setLeftWheelSpeed(-35)
            self.setRightWheelSpeed(35)
            if opposite_front > 80:
                return
            if hand_corner < 120 and hand_side > 100:
                self.setSpeed(0)
                self.state = RobotState.FollowWall
        # ------------------------------------------------------------
        # Follow Wall
        # ------------------------------------------------------------
        elif self.state == RobotState.FollowWall:
            self.setSpeed(100)
            # Facing Wall
            if opposite_front > 100 and hand_front > 100:
                self.setSpeed(0)
                self.state = RobotState.MountWall
            # Turn Corner
            elif hand_side < 80 and hand_corner < 80:
                self.setSpeed(50) # TODO: do we need this?
                self.state = RobotState.TurnCorner
            # Adjust Left (more severly)
            elif hand_side > 200 and hand_corner > 150:
                self.setLeftWheelSpeed(-10)
                self.setRightWheelSpeed(50)
            # Adjust Left (moderate)
            elif hand_side > 200 and hand_corner > 100:
                self.setLeftWheelSpeed(80)
                self.setRightWheelSpeed(100)
            # Adjust Right
            elif hand_side < 150 and hand_corner < 80:
                self.setLeftWheelSpeed(100)
                self.setRightWheelSpeed(80)
        # ------------------------------------------------------------
        # Turn Corner
        # ------------------------------------------------------------
        elif self.state == RobotState.TurnCorner:
            self.setLeftWheelSpeed(50)
            self.setRightWheelSpeed(8)
            # Facing Wall
            if opposite_front > 100 and hand_front > 100:
                self.setSpeed(0)
                self.state = RobotState.MountWall
            elif hand_corner > 80:
                self.setSpeed(5) # TODO: do we need this?
                self.state = RobotState.FollowWall
# END EPuck Class

# trans:
# rotation:

print("Starting")
robot = EPuck(Robot())
while robot.step():
    robot.travel()
    if robot.state == RobotState.GameOver:
        break
print("GAME OVER")

# END
