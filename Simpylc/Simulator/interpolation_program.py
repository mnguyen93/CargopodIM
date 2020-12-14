'''
Requirements:

Module should accept point wise specifications of a curve.
The curve denotes relation between input and output.
It should interpolate between points and extrapolate at the extremes.

Design:

We use a function to achieve this.
The curve is a list parameter.
The input value is a float.
The output is returned as a float.

Test specification:

The program should correctly handle at least 3 curves at at least 5 test points.
Test should pay special attention to negative values.

aanroepen met interpolate.interpolate (y-waarden)
interpolate.get-y
interpolate.get-x
back-to-back testen

'''


class Interpolate:
    def __init__(self, curve):  # Init stands for initialize, so you give the start values (Default values)
        self.curve = list(curve)  # This is the Motor curve (gas_pedal_percentage, moment)
        self.inverseCurve = [(x, y) for y, x in self.curve]

    def get_other(self, curve, x):
        index = 0
        if index == len(curve) - 1:
            return curve[index][1]
        if x < (curve[index][0]) and index < len(curve):  # x < len(curve) then the search needs to stop
            return curve[index][0]
        while True:
            if index <= len(curve) and x <= curve[index][0]:
                while x < curve[0][0]:
                    return curve[0][1]
                a = (curve[index][1] - curve[index - 1][1]) / (curve[index][0] - curve[index - 1][0])
                b = curve[index][1] - (a * curve[index][0])
                y = (a * x) + b
                return y
            elif x > curve[-1][0]:
                return curve[-1][1]
            index += 1

    def find_y(self, x):
        return self.get_other(self.curve, x)

    def find_x(self, y):
        return self.get_other(self.inverseCurve, y)