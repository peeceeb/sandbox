##A local cafe wants a program that suggests a snack
##if the customer asks for cookies or samosa, it confirms the order
##Otherwise it says order not available
while(True):
    Order=input(f"Would you like to order anything?(Y/N)\n").lower()
    if Order.lower() in ("y","yes"):
        while(True):
            snack=input("Enter your preferred snack:(Samosa or Cookies)\n").lower()
            print(f"User input is {snack}")
            if snack=="cookies" or snack=="samosa":
                    quantity=int(input(f"How many {snack} would you like to order?\n"))
                    if snack=="cookies" and quantity>0:
                        total=20*quantity
                        print(f"{snack} will be ordered\n")
                        print(f"Your total is {total}\n")
                        break

                    elif snack=="samosa" and quantity>0:
                        total=15*quantity 
                        print(f"{snack} will be ordered\n")
                        print(f"Your total is {total}\n")
                        break

                    else:
                        print(f'Invalid Quantity')
                        break
            else:
                print(f"{snack} is not available")
                
    elif Order.lower() in ("n","no"):
        print("Thank you for choosing Myers! Have a Nice day!\n")
        break
    else:
        print("Invalid Input! Please try again!\n")

