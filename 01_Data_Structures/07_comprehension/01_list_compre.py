menu = [
    "Masala Chai",
    "Iced Lemon Tea",
    "Green Tea",
    "Iced Peach Tea",
    "Ginger Tea"
]

iced_tea= [tea for tea in menu if "Iced" in tea] 
iced_tea1= [tea1 for tea1 in menu if len(tea1)>12] 

print(iced_tea)
print(iced_tea1)