import time as tm
import simpylc as sp

class AutoPilot:
    def __init__(self):
        print('Use up arrow to start, down arrow to stop')

        self.driveEnabled = False

        while True:
            self.input()
            self.sweep()
            self.output()
            tm.sleep(0.02)

    def input(self):  # Input from simulator
        key = sp.getKey()

        if key == 'KEY_UP':
            self.driveEnabled = True
        elif key == 'KEY_DOWN':
            self.driveEnabled = False

    def sweep(self):  # Control algorithm to be tested
            self.steeringAngle = 4
            self.targetVelocity = 1 if self.driveEnabled else 0

    def output(self):  # Output to simulator
        sp.world.physics.steeringAngle.set(self.steeringAngle)
        sp.world.physics.targetVelocity.set(self.targetVelocity)