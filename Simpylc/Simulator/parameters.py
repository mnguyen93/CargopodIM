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
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
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

import simpylc as sp

# all variable values are divided by 5:
# 0.1 = 0.5 meter
# 0.2 = 1 meter
# 0.3 = 1.5 meter
# etc.

wheelDiameter = 0.06
wheelRadius = wheelDiameter / 2
displacementPerWheelAngle = sp.radiansPerDegree * wheelRadius

bodyLength = 0.3
bodyHeight = 0.1
bodyWidth = 0.1


leftRightWheelDistance = bodyWidth / 2
wheelBase = bodyLength - 0.1
wheelShift = wheelBase / 2
