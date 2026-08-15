class Chaicup:
    size=150

    def describe(self): #self is the reference to all the properties you are defining in class. 1 or many
        return f"A {self.size} ml chai cup" #you can use self. for a property or a function
    
cup=Chaicup()
print(cup.describe())
#print(Chaicup.describe())

cup2=Chaicup()
print(cup2.describe())
cup2.size=100
print(Chaicup.describe(cup2))
