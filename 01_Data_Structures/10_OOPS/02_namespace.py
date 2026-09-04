class Chai:
    origin = "India"

print(Chai.origin)

Chai.is_hot = True
print(Chai.is_hot)

#Creating object from Class chai
masala=Chai()
print(f"Masala {masala.origin}")
print(f"Masala {masala.is_hot}")

masala.is_hot=False
print("Class: ", Chai.is_hot)
print(f"Masala:  {masala.is_hot}")

#Each object is actually having its own namespace which doesn't affect other object and also does not affect the classes by default.

#You can also add more values to Masala object eg. Flavor.
#Hello