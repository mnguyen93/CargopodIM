# ====== Legal notices
#
# Copyright (C) 2013  - 2020 GEATEC engineering
#
# This program is free software./
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
A PID controller:
P = knows the speed the vehicle is reaching
I = integrated the speed difference to reach the exact speed
D = Differentiate the speed if there was a big speed increase

Inputs of the PID is the Vs (the willing speed) Vi (the current speed).
Output of the PID is the Moment or Torque

The PID controller will be an object and is located in the low level
controller together with the hardware abstraction.
The output will be implemented in the hardware abstraction (interpolator program)

In this program will be an loop which runs infinitely by collecting the old and new time.
P --> Mp = p dv
I --> Mi = i sum dv dt
D --> Md = d * dv/dt
----------------------- +
      Mt = the total moment as output
The p, i and d are constants which will be collected by tuning the program.

The output of this will be a moment by reversing the interpolator a current
will be calculated.
'''
import time


class PidController:
    def __init__(self, Kp, Ki, Kd):
        self.previousError = 0.0

        self.differential = 0.0
        self.integral = 0.0
        self.proportional = 0.0

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.output = 0.0
        self.setPoint = 0.0

    def getY(self, deltaTime, setPoint, actual):
        # The difference between the actual and the setPoint signal
        error = setPoint - actual

        deltaError = error - self.previousError

        # Proportional
        self.proportional = self.Kp * error

        # Integral
        self.integral += error * deltaTime * self.Ki

        # Differential
        self.differential = self.Kd * (deltaError / deltaTime)

        # Save old value as new value
        self.previousError = error

        self.output = self.proportional + self.integral + self.differential

        return self.output

    '''def __init__ (self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.yI = 0
        self.xErrorOld = 0

    def getY (self, deltaT, xSetpoint, xActual):
        
        # Deviation between setpoint and actual signal
        xError = xSetpoint - xActual
        
        # Proportional term
        yP = self.p * xError
        
        # Integrating term
        self.yI += self.i * xError * deltaT
        
        # Differentiating term
        yD = self.d * (xError - self.xErrorOld) / deltaT
        self.xErrorOld = xError
        
        # Summation
        return yP + self.yI + yD'''
