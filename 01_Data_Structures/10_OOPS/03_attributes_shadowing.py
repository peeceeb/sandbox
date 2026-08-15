class Chai:
    temperature = "hot"
    strength ="Strong"

cutting = Chai()
print(cutting.temperature)

cutting.temperature="Mild"
cutting.cup="Small"
print("After Changing",cutting.temperature)
print("Cup Size",cutting.cup)
print("Direct look into the class",Chai.temperature)

del cutting.temperature
print(cutting.temperature)

#Suppose you create some attibutes in a class and later you delete them from an object, the shadow 
#will fall but the attribute stay. This is nothing but object shadowing.

