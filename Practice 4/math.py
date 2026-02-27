import math

deg = float(input("Input degree: "))
rad = deg * math.pi / 180
print("Output radian:", rad)

#######################################################

h = float(input("Height: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))

area = (a + b) / 2 * h
print("Expected Output:", area)

#######################################################

import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s * s) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", area)

#######################################################

b = float(input("Length of base: "))
h = float(input("Height of parallelogram: "))

print("Expected Output:", b * h)