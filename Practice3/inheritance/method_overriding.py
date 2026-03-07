class Animal:
    def speak(self):
        print("Animal makes a sound.")


class Cat(Animal):

    def speak(self):
        print("Cat says meow.")

class Dog(Animal):
    
    def speak(self):
        print("Dog says woof.")


a = Animal()
c = Cat()
d = Dog()

a.speak()
c.speak()
d.speak()