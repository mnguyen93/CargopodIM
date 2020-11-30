import time as tm
import simpylc as sp


class AutoPilot:
    def __init__(self):
        
        self.compass_angle = 0

        while True:
            self.input()
            self.sweep()
            self.output()
            tm.sleep(0.02)

    def input(self):  # Input from simulator
        self.compass_angle = sp.world.physics.courseAngle

    # function that turns the Cargopod toward the angle you pass it.
    # a positive target_angle makes a right turn, a negative target_angle makes a left turn.
    def turn(self, target_angle):
        if abs(self.compass_angle + 0) >= abs(target_angle):
            self.targetVelocity = 0
            self.steeringAngle = 0
        else:
            self.steeringAngle = 5 if target_angle < 0 else -5
            self.targetVelocity = 1

    def sweep(self):  # Control algorithm to be tested
        self.turn(-360)

    def output(self):  # Output to simulator
        sp.world.physics.steeringAngle.set(self.steeringAngle)
        sp.world.physics.targetVelocity.set(self.targetVelocity)
