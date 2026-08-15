##A local cafe wants a program that suggests a snack
##if the customer asks for cookies or samosa, it confirms the order
##Otherwise it says order not available
while(True):
    Order=input(f"Would you like to order anything?").lower()
    if Order=="y" or Order=="yes":
        while(True):
            snack=input("Enter your preferred snack:").lower()
            print(f"User input is {snack}")
            if snack=="cookies" or snack=="samosa":
                print(f"{snack} will be ordered")
                break
            else:
                print(f"{snack} is not available")
    elif Order=="n" or Order=="no":
        print("Thank you for choosing Myers! Have a Nice day!")
        break
    else:
        print("Invalid Input! Please try again!")
