# Select passing grades only (>= 50)
grades = [35, 67, 90, 48, 52]
passing = list(filter(lambda g: g >= 50, grades))
print(passing)