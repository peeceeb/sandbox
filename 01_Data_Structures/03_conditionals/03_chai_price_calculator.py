##
# A tea stall offers different prices for different cup sizes.
# Write a program that calculates price based on price.

#Task
#Input= "Small","Medium","Large"
#Small ->$10 Medium $15 Large->$20
#If invalid:show "Unknown cup size"

cup=input("Choose your cup size (Small/Medium/Large)").lower()
if cup == "small":
    print("Price is $10")
elif cup == "medium":
    print("Price is $15")
elif cup == "large":
    print("Price is $20")
else:
    print("Unknown Cup Size")

