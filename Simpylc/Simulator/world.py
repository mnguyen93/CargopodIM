#! /usr/bin/python

# ====== Legal notices
#
# Copyright (C) 2013  - 2020 GEATEC engineering
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

import timing as tm
import visualisation as vs
import physics as ps
import lidar_pilot_sp as ls
import lidar_pilot as lp
import keyboard_pilot as kp
import control as ct
import simpylc as sp
import os
import sys as ss
import route as r

# If you want to store your simulations somewhere else, put SimPyLC in your PYTHONPATH environment variable
ss.path.append(os.path.abspath('../../..'))

sp.World (
    ps.Physics,
    vs.Visualisation,
    r.Route,
)
