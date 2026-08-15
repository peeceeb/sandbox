
favorite_chai={
    "Ginger Tea",
    "Masala Chai",
    "Green Tea",
    "Masala Chai",
    "Lemon Tea",
    "Green Tea",
    "Elaichi Chai"
}

#How many unique chai using set

unique_chai={Chai for Chai in favorite_chai}

print(unique_chai)

recipes={
    "Masala Chai":["ginger","cardamom","clove"],
    "Elaichi Chai":["cardamom","milk"],
    "Spicy Chai":["ginger","black pepper"],
}

unique_spices={spice for ingredient in recipes.values() for spice in ingredient} 
print(unique_spices)