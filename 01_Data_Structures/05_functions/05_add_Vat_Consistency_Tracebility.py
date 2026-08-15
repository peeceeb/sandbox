def add_vat(price, vat_rate):
    vat=price*vat_rate
    final_price=price+vat
    return final_price

print(f"Bill for Order1 is: {add_vat(1200,10)}")
print(f"Bill for Order2 is: {add_vat(2300,10)}")
print(f"Bill for Order3 is: {add_vat(3400,10)}")

Orders=[100,200,2000]

for price in Orders:
    final_amount=add_vat(price,10)
    print(f"Original: {price}, Final with VAT: {final_amount}")
    