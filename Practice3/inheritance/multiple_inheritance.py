class Flyer:
    def fly(self):
        print("Can fly.")


class Swimmer:
    def swim(self):
        print("Can swim.")


class Duck(Flyer, Swimmer):
    def quack(self):
        print("Duck says quack.")


duck = Duck()

duck.fly()
duck.swim()
duck.quack()