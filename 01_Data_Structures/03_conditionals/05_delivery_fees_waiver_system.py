order_amount=int(input("Enter the order amount"))

delivery_fee=0 if order_amount>200 else 30
print(f"Delivery fees is: {delivery_fee}")


