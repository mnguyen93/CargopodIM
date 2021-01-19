"""
Sweep cycles through velocity, steer_angle.
Velocity and steer_angle are determined by step_index.
When target is reached (amount of wheel-rotations or driven meters?) -> go to next step_index and repeat.

Velocities and steer_angles are stored in lists. These determine the route.
"""

import time as tm
#import simpylc as sp
import pid_controller as pd
import timer as tr
import interpolation_program as int
import json

class Route:
    def __init__(self):
        #curve = ([-30, 0.33], [-29, 0.34], [-28, 0.34], [-27, 0.35], [-26, 0.36], [-25, 0.37], [-24, 0.37], [-23, 0.38],
        #         [-22, 0.39], [-21, 0.4], [-20, 0.41], [-19, 0.42], [-18, 0.43], [-17, 0.45], [-16, 0.46], [-15, 0.48],
        #         [-14, 0.49], [-13, 0.51], [-12, 0.54], [-11, 0.56], [-10, 0.59], [-9, 0.62], [-8, 0.66], [-7, 0.7],
        #         [-6, 0.76], [-5, 0.83], [-4, 0.93], [-3, 1.08], [-2, 1.32], [-1, 1.86], [0, 2], [1, 1.86], [2, 1.32],
        #         [3, 1.08], [4, 0.93], [5, 0.83], [6, 0.76], [7, 0.7], [8, 0.66], [9, 0.62], [10, 0.59], [11, 0.56],
        #         [12, 0.54], [13, 0.51], [14, 0.49], [15, 0.48], [16, 0.46], [17, 0.45], [18, 0.43], [19, 0.42],
        #         [20, 0.41], [21, 0.4], [22, 0.39], [23, 0.38], [24, 0.37], [25, 0.37], [26, 0.36], [27, 0.35], [28, 0.34],
        #         [29, 0.34], [30, 0.33])
        #self.inter = int.Interpolate(curve)
        self.step_index = 0
        self.loop = True
        self.drive_distances = []
        self.steer_angles = []
        self.seconds = []
        self.velocity = 0
        self.pause = 0.02
        self.setDistToZero = False
        #self.steeringPidController = pd.PidController(0.93, 0, 0.1)
        #self.velocityPidController = pd.PidController(0.6, 0.01, 0.002)
        self.timer = tr.Timer()
        self.travelLeft = kit.motor3.throttle = 0.0
        self.travelRight = kit.motor4.throttle = 0.0
        self.rotations = 0.0
        self.angle = 0.0

        with open('route.json', 'r') as route:
            route_json = json.load(route)

        for route in route_json.get('route'):
            self.drive_distances.append(route["distance"])
            self.steer_angles.append(route["angle"])
            self.seconds.append(route["seconds"])

        while self.loop:
            tm.sleep(self.pause)
            self.timer.tick()
            self.sweep()
            self.output()

    def sweep(self):
        # After the last step we want to stop the car and stop the loop
        if self.step_index > len(self.seconds) -1:
            self.targetVelocity = 0
            #self.steeringAngle = 0
            self.loop = False
        else:
            self.pause = 0.02

            if self.setDistToZero:
                kit.motor3.thorttle = 0.0
                kit.motor4.throttle = 0.0
                self.setDistToZero = False

            #self.steeringAngle = self.steeringPidController.getY(self.timer.deltaTime, self.steer_angles[self.step_index], 0)

            # Handles standing still, if drive_distance this step is 0, it stands still for 5 seconds.
            if self.seconds[self.step_index] == 0:
                #self.steeringAngle = 0
                self.targetVelocity = 0
                self.pause = 5
                self.setDistToZero = True
                self.step_index += 1

            else:
                self.velocity = 1.0
                #self.velocity = self.velocityPidController.getY(self.timer.deltaTime, self.inter.find_y(self.steer_angles[self.step_index]), 0)
                self.targetVelocity = -self.velocity if self.seconds[self.step_index] < 0 else self.velocity
        
            # Goes to next step when we reach the target distance for this step.
            timeout = tm.time() + self.seconds[]
            if timeout + 0  >= abs(self.seconds[self.step_index]):
                self.setDistToZero = True
                self.step_index += 1

    def output(self):  # Output to simulator
        print('Het voertuig rijdt naar voren of naar achteren')
        #kit.motor3.throttle = self.targetVelocity
        #kit.motor4.throttle = self.targetVelocity
