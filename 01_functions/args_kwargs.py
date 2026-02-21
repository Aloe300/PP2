def my_function(**myvar):
	for key, value in myvar.items():
		print(key, ":", value)


my_function(name = "Tobias", age = 30, city = "Bergen")

def average(*numbers):
	
    total = sum(numbers)
    return total / len(numbers)

print(average(10, 20, 30))

