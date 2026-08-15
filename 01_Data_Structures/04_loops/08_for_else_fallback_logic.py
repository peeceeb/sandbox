#Use this if you want to execute something that is not found in the loop

staff = [("Amit",16),("Zara",19),("Raj",15)]

for name, age in staff:
    if age<=19:
        print(f"{name} is eligible to manage the staff")
        break
else:
    print(f"No one is eligible to manage the staff")