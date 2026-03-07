class Student:
    university = "KBTU"

    def __init__(self, name):
        self.name = name

s1 = Student("Aruzhan")
s2 = Student("Dana")

print("Before:", s1.university, s2.university)

Student.university = "KBTU International"

print("After:", s1.university, s2.university)