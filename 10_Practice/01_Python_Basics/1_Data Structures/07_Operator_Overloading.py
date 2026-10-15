base_ingredients = ["water", "milk"]
spices = ["ginger", "cardamom"]
sugar = 2
extra_sugar = 3

"""
Write a program to:
1. Use + to combine base_ingredients and spices into one list.
2. Use + to calculate the total sugar.
3. Use * to repeat the spices list twice.
4. Print all three results using f-strings.
"""
combined_ingredients = base_ingredients + spices
total_sugar = sugar + extra_sugar
repeated_spices = spices * 2

print(f"Combined Ingredients: {combined_ingredients}")
print(f"Total Sugar: {total_sugar}")
print(f"Repeated Spices: {repeated_spices}")