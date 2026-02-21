class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")

class Dog(Animal):
    def wag_tail(self):
        print(f"{self.name} is wagging its tail.")

dog1 = Dog("Leo")

dog1.speak()

dog1.wag_tail()