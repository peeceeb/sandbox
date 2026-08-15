#1 Nothing return
def print_something():
    pass

print(print_something())

#2 Single return
def sold_cups():
    return 120

total = sold_cups()
print(total)

#Early from a function
def chai_status(cups_left):
    if cups_left==0:
        return "Sorry, No cups left"
    return "Chai is ready"
    print("Chai nothing")

print(chai_status(5))
print(chai_status(0))

#Multiple return
def chai_report():
    return 100, 20, 10 #sold , none, remaining

sold, _ ,Not_paid=chai_report()
print("Sold",sold)
print("Not_Paid",Not_paid)     