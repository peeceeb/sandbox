def calculate_bill(cups, price_per_cup):
    total_bill=cups*price_per_cup
    return total_bill

print(f"Bill for Order1 is: {calculate_bill(12,25)}")
print(f"Bill for Order2 is: {calculate_bill(2,35)}")
print(f"Bill for Order3 is: {calculate_bill(3,45)}")
