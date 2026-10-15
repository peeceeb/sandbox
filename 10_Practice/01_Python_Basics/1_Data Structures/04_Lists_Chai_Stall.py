"""You are building an automated system for a high-tech chai stall. 
You need to manage inventory, tweak recipes on the fly, organize your spice rack, and analyze customer ratings using Python lists.
Here is your starter code skeleton. Your mission is to fill in the missing code based on the instructions below!"""

# TODO: Complete the tasks below!
"""
1: Restock & Expand (append & extend):
Add "Honey" to the end of inventory using .append().
Add all items from secret_spices into inventory using .extend(). Print the updated inventory.

2: Quality Control (pop & remove):
Oh no! We ran out of "Water" in the inventory list. Remove it using .remove().
A quality inspector taste-tested the last spice added to the inventory and removed it from the list using .pop(). 
Print what was popped and the updated inventory.

3: Organization (sort & reverse):
Alphabetize the remaining items in your inventory list using .sort().
Suddenly, a rebellious chef wants to brew the chai in reverse order! Reverse the sorted inventory list using .reverse(). 
Print the final quirky brewing order.

4: Analytics (max & min):
Find and print the highest and lowest customer ratings from the customer_ratings list using max() and min().
Give it a try and share your solution, or let me know if you'd like to see the breakdown of how to solve it!
"""

# --- STARTER CODE ---
inventory = ["Water", "Milk", "Black Tea"]
secret_spices = ["Cinnamon", "Star Anise", "Cloves"]
customer_ratings = [4.5, 4.8, 3.2, 5.0, 4.9]

#1
inventory.append("Honey")
print(inventory)
inventory.extend(secret_spices)
print(inventory)

#2
inventory.remove("Water")
print(inventory)
inventory.pop()
print(inventory)


#3
inventory.sort()
print(inventory)

#4
max_rating=max(customer_ratings)
print(max_rating)
min_rating=min(customer_ratings)
print(min_rating)