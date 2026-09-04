###############Inheritance ("is-a" relationship)####################

#A class derives from another class, inheriting its properties and behavior.
class Animal:
    def __init__(self, name):
        self.name = name
    def eat(self):
        print(f"{self.name} is eating")

class Dog(Animal):  # Dog IS-A Animal
    def bark(self):
        print(f"{self.name} says Woof!")

Jimmy=Dog("Jimmy")
Jimmy.eat()  #Dog automatically gets eat() from Animal  
Jimmy.bark()  #Dog has its own bark() method

#Dog automatically gets eat() from Animal
#The relationship is fixed at compile time (or class definition time)
#Creates a tight coupling between parent and child — changes to the parent ripple down to every child


################Composition ("has-a" relationship)####################
#A class contains an instance of another class and delegates work to it, rather than inheriting from it.

class Engine:
    def start(self):
        print("Engine starting")

class Car:  # Car HAS-A Engine
    def __init__(self):
        self.engine = Engine() #This line is doing two things at once: creating an object and storing a reference to it.
    def start(self):
        self.engine.start()


Car1=Car()
Car1.start()
