# chai = "Ginger chai"

# def prepare_chai(order):
#     print("Preparing",order)

# prepare_chai(chai)

lst1=[1,2,3]

def edit_chai(lst):
    lst[1]=42

edit_chai(lst1)
print(lst1)

def make_chai(tea,milk,sugar):
    print(tea,milk,sugar)

make_chai("Darjeeling","Yes","Medium") #positional parameters
make_chai(tea="Mysore",sugar="High",milk="Yes") #keyword parameters


# *---> arguments convert aka args *ingredients into a tuple
# **---> keyvaluue argument aka kwargs **extras gets converted to dictionary
def special_chai(*ingredients,**extras):
    print("Ingredients", ingredients)
    print("Extras",extras)

special_chai("Cinnamon","Cardamom","Tea",sweetener ="Honey", foam="Yes")

# def chai_order(order=None):
#     if order is None:
#         order=[]
#         order.append("Masala")
#     print(order)

# chai_order()
# chai_order("Masala")