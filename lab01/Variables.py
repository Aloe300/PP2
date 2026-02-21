x = 1       # x is of type int
x = "kbtu" # x is now of type str
print(x)

languages = ["python", "c++", "c#"]
x, y, z = languages
print(x)
print(y)
print(z)

x = "a "
y = "b "
z = "c"
print(x + y + z)


x = "Alim"

def myfunc():
  global x
  x = "Dimash"

myfunc()

print("My name is " + x)


x = "Alim"

def myfunc():
  print("Pythmy name is " + x)

myfunc()

