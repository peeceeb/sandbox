ingredients=["Water","Milk","Black Tea"]
ingredients.append("Sugar")
print(f"ingredients:{ingredients}")
ingredients.remove("Water")
print(f"ingredients:{ingredients}")

spice_option=["ginger","cardamom"]
chai_ingredient=["Water","Milk"]

chai_ingredient.extend(spice_option)
print(f"Chai Ingredients:{chai_ingredient}")

#.pop() .reverse() .sort()

sugar_level=[1,2,3,4,5]
print(f"Maximum sugar level", max(sugar_level))