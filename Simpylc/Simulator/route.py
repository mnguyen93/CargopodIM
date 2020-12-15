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
import interpolation_program as int

class Route:
    def __init__(self):
        self.step_index = 0
        self.velocity = 0
        self.steer_angles = [0, 3, 0, -3, 0, 0, 0, -3, 0, 3, 0]
        self.drive_distances = [0, 5, 10, 5, 10, 2, 10, 5, 10, 5, 0]
        self.pause = 0.02
        self.steeringPidController = pd.PidController(1.065, 0.0, -0.035)
        self.velocityPidController = pd.PidController(1.25, 0.0, 0.00065)

        while True:
            self.sweep()
            self.output()
            tm.sleep(self.pause)

    def next_step(self):
        sp.world.physics.drivenMeters.set(0)
        self.step_index += 1

        # Use interpolator here to determine the velocity this step.
        inter = int.Interpolate(curve)
        self.velocity = inter.find_y(self.steer_angles)

    def sweep(self):
        self.pause = 0.02
        if self.step_index < len(self.drive_distances):
            self.targetVelocity = self.velocity
            self.steeringAngle = self.steer_angles[self.step_index]

            # Handles standing still, stays still for 2 seconds, this step.
            if(self.drive_distances[self.step_index]) == 0:
                self.pause = 2
                self.next_step()

            # Goes to next step when we reach the target distance for this step.
            elif sp.world.physics.drivenMeters + 0 >= self.drive_distances[self.step_index]:
                self.next_step()
        else:
            self.targetVelocity = 0.0
            self.steeringAngle = 0.0
            #self.targetVelocity = self.velocityPidController.getY(self.timer.deltaTime, 0, 0)
            #self.steeringAngle = self.steeringPidController.getY(self.timer.deltaTime, 0, 0)

    def output(self):  # Output to simulator
        sp.world.physics.steeringAngle.set(self.steeringAngle)
        sp.world.physics.targetVelocity.set(self.targetVelocity)
