chai_order=dict(type="Masala_Chai",
                size="Large",
                sugar=2)

print(f"Chai_Order:,{chai_order}")

chai_recipe={}
chai_recipe["base"]="black tea"
chai_recipe["liquid"]="milk"

print(f"Recipe_Base: {chai_recipe['base']}")
del chai_recipe["liquid"]
print(f"chai_recipe: {chai_recipe}")
print(f"is Sugar in Chai order? {'sugar'in chai_order}")

# print(f"Order details Keys {chai_order.keys()}")
# print(f"Order details Values {chai_order.values()}")
# print(f"Order details Items {chai_order.items()}")

print(f"chai recipe: {chai_recipe}")
extra_spices={"cardamom":"crushed", "ginger":"sliced"}
chai_recipe.update(extra_spices)
print(f"Updated Chai recipe: {chai_recipe}")

customer_note=chai_order.get("size","No note")
print(f"Customer_Note is: {customer_note}"s)