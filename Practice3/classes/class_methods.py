class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major

    def introduce(self):
        print(f"Hello! My name is {self.name} and my major is {self.major}.")

student2 = Student("Ali", "Computer Science")
student2.introduce()