"""
Sweep cycles through velocity, steer_angle.
Velocity and steer_angle are determined by step_index.
When target is reached (amount of wheel-rotations or driven meters?) -> go to next step_index and repeat.

Velocities and steer_angles are stored in lists. These determine the route.
"""

import time as tm
import simpylc as sp
import pid_controller as pd
import timer as tr

class Route:
    def __init__(self):
        self.step_index = 0
        self.velocities = [0.5, 1, 0.5, 1, 0, -1, -0.5, -1, -0.5, 0]
        self.steer_angles = [3, 0, -3, 0, 0, 0, -3, 0, 3, 0]
        self.drive_distances = [5, 10, 5, 10, 2, 10, 5, 10, 5, 0]
        self.pause = 0.02
        self.steeringPidController = pd.PidController(1.065, 0.0, -0.035)
        self.velocityPidController = pd.PidController(1.25, 0.0, 0.00065)

        while True:
            self.sweep()
            self.output()
            tm.sleep(self.pause)

    def sweep(self):
        self.pause = 0.02
        if self.step_index < len(self.drive_distances):
            self.velocityStep = self.velocities[self.step_index]
            self.targetVelocity = self.velocityPidController.getY(0.01, self.velocityStep, 0)
            self.steeringAngleStep = self.steer_angles[self.step_index]
            self.steeringAngle = self.steeringPidController.getY(0.01, self.steeringAngleStep, 0)

            # Handles standing still, stays still for drive_distances in seconds, this step.
            if(self.velocities[self.step_index]) == 0:
                self.pause = self.drive_distances[self.step_index]
                sp.world.physics.drivenMeters.set(0)
                self.step_index += 1

            # Goes to next step when we reach the target distance for this step.
            elif sp.world.physics.drivenMeters + 0 >= self.drive_distances[self.step_index]:
                sp.world.physics.drivenMeters.set(0)
                self.step_index += 1
        else:
            self.targetVelocity = 0.0
            self.steeringAngle = 0.0
            #self.targetVelocity = self.velocityPidController.getY(self.timer.deltaTime, 0, 0)
            #self.steeringAngle = self.steeringPidController.getY(self.timer.deltaTime, 0, 0)

    def output(self):  # Output to simulator
        sp.world.physics.steeringAngle.set(self.steeringAngle)
        sp.world.physics.targetVelocity.set(self.targetVelocity)
