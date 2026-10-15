# --- STARTER CODE ---
# 1. Create a customer order using the dict() constructor
current_order = dict(chai_name="Adrak Chai", cup_size="Medium", milk_type="Oat")

# 2. Base recipe dictionary
current_recipe = {"base": "black tea", "water": "1 cup", "milk": "1/2 cup"}
# --------------------

"""
Safety Checks (in & .get()):
1. Check if the key "sweetness" is in current_order using the in operator and print the boolean result.
2. Use .get() to look up "syrup" in current_order. If it's missing, provide a default fallback message like "None". Print the result.
Recipe Customization (update & del):
3. The customer wants extra flavor! Create a dictionary called add_ons = {"ginger": "grated", "cardamom": "crushed"} and merge it into current_recipe using .update().
Oh wait, the kitchen is completely out of "water" for this special brew! Remove the "water" key from current_recipe using del. Print the updated recipe.
4. Kitchen Display System (.keys(), .values(), .items()):
5. Print all the keys of current_recipe.
6. Print all the values of current_recipe.
7. Print all the key-value items of current_recipe so the chef can see everything clearly.
"""

#1
sweetness_check =  "sweetness" in current_order
print(sweetness_check)

#2
print(current_order.get("syrup", "None"))
print(current_order)

#3
add_ons = {"ginger": "grated", "cardamom": "crushed"}
current_recipe.update(add_ons)
print(current_recipe)
current_recipe.pop("water")
print(current_recipe)

#4
for key in current_recipe.keys():
    print("Key",key)

for val in current_recipe.values():
    print("values",val)

for item in current_recipe.items():
    print("items", item)
