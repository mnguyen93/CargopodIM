# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

'''

      z
      |
      o -- y
     /
    x

'''

import random as rd

import simpylc as sp

import parameters as pm
import json
import math 


normalFloorColor = (0, 0.003, 0)
collisionFloorColor = (1, 0, 0.3)
nrOfObstacles = 64


class Lidar:
    # 0, ...,  halfApertureAngle - 1, -halfApertureAngle, ..., -1

    def __init__(self, apertureAngle, obstacles):
        self.apertureAngle = apertureAngle
        self.halfApertureAngle = self.apertureAngle // 2
        self.obstacles = obstacles
        self.distances = [sp.finity for angle in range(self.apertureAngle)]

    def scan(self, mountPosition, mountAngle):
        self.distances = [sp.finity for angle in range(self.apertureAngle)]
        all = [(sp.finity, angle) for angle in range(-180, 180)]

        for obstacle in self.obstacles:
            relativePosition = sp.tSub(obstacle.center, mountPosition)
            distance = sp.tNor(relativePosition)
            absoluteAngle = sp.atan2(relativePosition[1], relativePosition[0])
            relativeAngle = (
                round(absoluteAngle - mountAngle) + 180) % 360 - 180

            if distance < all[relativeAngle][0]:
                # In case of coincidence, favor nearby obstacle
                all[relativeAngle] = (distance, relativeAngle)

            if -self.halfApertureAngle <= relativeAngle < self.halfApertureAngle - 1:
                # In case of coincidence, favor nearby obstacle
                self.distances[relativeAngle] = min(
                    distance, self.distances[relativeAngle])

        # print (all)


class Line (sp.Cylinder):
    def __init__(self, **arguments):
        super() .__init__(size=(1, 0.1, 0), axis=(
            1, 0, 0), angle=0, color=(0, 1, 1), **arguments)


class BodyPart (sp.Beam):
    def __init__(self, **arguments):
        super() .__init__(color=(1, 0, 0), **arguments)


class Wheel:
    def __init__(self, **arguments):
        self.suspension = sp.Cylinder(size=(0.01, 0.01, 0.001), axis=(
            1, 0, 0), angle=0, pivot=(0, 1, 1), **arguments)
        self.rim = sp.Beam(size=(0.08, 0.06, 0.02),
                           pivot=(0, 1, 0), color=(0, 0, 0))
        self.tire = sp.Cylinder(size=(pm.wheelDiameter, pm.wheelDiameter, 0.04), axis=(
            1, 0, 0), angle=0, color=(1, 1, 0))
        self.line = Line()

        self.circumference = (math.pi * pm.wheelDiameter) #should be 0.1256 with diameter 0.04
        #revolutions = distance / circumference
        self.wheelRotations = 0

    def wheelRotations(self):
        wheelRotations = self.wheelRotations
        if self.line.angle == 360:
            wheelRotations = wheelRotations + 1
        else:
            wheelRotations = wheelRotations + 0

    def __call__(self, wheelAngle, slipping, steeringAngle=0):
        return self.suspension(rotation=steeringAngle, parts=lambda:
                               self.rim(rotation=wheelAngle, parts=lambda:
                                        self.tire(color=(rd.random(), rd.random(), rd.random()) if slipping else (1, 1, 0)) +
                                        self.line()
                                        ))


class Window (sp.Beam):
    def __init__(self, **arguments):
        super() .__init__(axis=(0, 1, 0), color=(0, 0, 1), **arguments)


class Floor (sp.Beam):
    trackLength = 114
    trackWidth = 13
    spacing = 0.2
    lengthHalfSteps = round(0.5 * trackLength / spacing)
    widthHalfSteps = round(0.5 * trackWidth / spacing)

    class Stripe (sp.Beam):
        def __init__(self, length, **arguments):
            super() .__init__(size=(0.01, length, 0.001), **arguments)

    def __init__(self, **arguments):
        super() .__init__(size=(self.trackLength, self.trackWidth, 0.0005), color=normalFloorColor)
        self.xStripes = [self.Stripe(
            self.trackLength,
            center=(0, nr * self.spacing, 0.0001),
            angle=90,
            color=(1, 1, 1)
        ) for nr in range(-self.widthHalfSteps, self.widthHalfSteps)]
        self.yStripes = [self.Stripe(
            self.trackWidth,
            center=(nr * self.spacing, 0, 0),
            color=(0, 0, 0)
        ) for nr in range(-self.lengthHalfSteps, self.lengthHalfSteps)]

    def __call__(self, parts):
        return super() .__call__(color=collisionFloorColor if self.scene.collided else normalFloorColor, parts=lambda:
                                 parts() +
                                 sum(xStripe() for xStripe in self.xStripes) +
                                 sum(yStripe() for yStripe in self.yStripes)
                                 )


class Rectangle(sp.Beam):
    def __init__(self, **arguments):
        super().__init__(**arguments)


class Visualisation (sp.Scene):
    def __init__(self):
        super() .__init__()

        self.camera = sp.Camera()

        self.floor = Floor(scene=self)

        self.carBody = BodyPart(size=(pm.bodyLength, pm.bodyWidth, pm.bodyHeight), center=(
            0, 0, pm.bodyHeight), pivot=(0, 0, 1), group=0)

        self.wheelFrontLeft = Wheel(
            center=(pm.wheelShift, pm.leftRightWheelDistance, -(pm.bodyHeight / 2)))
        self.wheelFrontRight = Wheel(
            center=(pm.wheelShift, -pm.leftRightWheelDistance, -(pm.bodyHeight / 2)))

        self.wheelRearLeft = Wheel(
            center=(-pm.wheelShift, pm.leftRightWheelDistance, -(pm.bodyHeight / 2)))
        self.wheelRearRight = Wheel(
            center=(-pm.wheelShift, -pm.leftRightWheelDistance, -(pm.bodyHeight / 2)))

        self.windowFront = Window(
            size=(0.05, 0.14, 0.14), center=(0.14, 0, -0.025), angle=-60)
        self.windowRear = Window(
            size=(0.05, 0.14, 0.18), center=(-0.18, 0, -0.025), angle=72)

        # self.walls = [
        #     Wall(size=(102, 0.1, 1), center=(0, 2.05, 0), color=(1, 0.3, 0), group=1),
        #     Wall(size=(102, 0.1, 1), center=(0, -2.05, 0), color=(1, 0.3, 0), group=1)
        # ]

        # jsondata = '''[

        #         {
        #             "name": "sideWall1",
        #             "length": 102,
        #             "width": 0.1,
        #             "posX": 0,
        #             "posY": 2.05
        #         },
        #         {
        #             "name": "sideWall2",
        #             "length": 102,
        #             "width": 0.1,
        #             "posX": 0,
        #             "posY": -2.05
        #         }
        # ]'''
        with open('obstacles.json', 'r') as rectangles:
            obstacles_json = json.load(rectangles)

        self.rectangles = []

        for rectangle in obstacles_json.get('rectangles'):
            # print(obstacles_json['rectangles'][0]['length'])
            self.rectangles.append(
                Rectangle(
                    size=(rectangle["length"], rectangle["width"], 1),
                    center=(rectangle["posX"], rectangle["posY"], 0),
                    color=(1, 0, 1),
                    group=1
                )
            )

        self.init = True

        self.lidar = Lidar(120, self.rectangles)

    def display(self):
        if self.init:
            self.init = False
            # Set initial car position here
            # -50 is the start of the track, 50 is the end of the track
            # -Y is the right side of the car, +Y is the left side of the car
            sp.world.physics.positionX.set(0)
            sp.world.physics.positionY.set(0)

        self.camera(
            position=sp.tEva((sp.world.physics.positionX + 2,
                              sp.world.physics.positionY, 3)),
            focus=sp.tEva((sp.world.physics.positionX + 1,
                           sp.world.physics.positionY, 0))
        )
        '''
        self.camera (
            position = sp.tEva ((0.0000001, 0, 12)),
            focus = sp.tEva ((0, 0, 0))
        )
        '''

        self.floor(parts=lambda:
                   self.carBody(position=(sp.world.physics.positionX, sp.world.physics.positionY, 0), rotation=sp.world.physics.attitudeAngle, parts=lambda:

                                self.wheelFrontLeft(
                       wheelAngle=sp.world.physics.midWheelAngle,
                       slipping=sp.world.physics.slipping,
                       steeringAngle=sp.world.physics.steeringAngle
                   ) +
                       self.wheelFrontRight(
                       wheelAngle=sp.world.physics.midWheelAngle,
                       slipping=sp.world.physics.slipping,
                       steeringAngle=sp.world.physics.steeringAngle
                   ) +

                       self.wheelRearLeft(
                       wheelAngle=sp.world.physics.midWheelAngle,
                       slipping=sp.world.physics.slipping
                   ) +
                       self.wheelRearRight(
                       wheelAngle=sp.world.physics.midWheelAngle,
                       slipping=sp.world.physics.slipping
                   )

                   )
                   +
                   sum(rectangle() for rectangle in self.rectangles)


                   )

        try:
            self.lidar.scan(self.fuselage.position, self.fuselage.rotation)
        except Exception as exception:  # Initial check
            pass
            # print ('Visualisation.display:', exception)
