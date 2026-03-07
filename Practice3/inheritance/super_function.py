class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Student(Person):
    def __init__(self, name, age, major):
        super().__init__(name, age)
        self.major = major

    def show_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Major: {self.major}")


s1 = Student("Aruzhan", 18, "Computer Science")
s1.show_info()