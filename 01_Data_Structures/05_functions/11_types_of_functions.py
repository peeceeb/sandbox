#Pure function nothing altered globally
def pure_chai(cups):
    return cups * 10

total_chai=0

#not recommended impure function
def impure_chai(cups):
    global total_chai
    total_chai+=cups

#Recursive function
def pour_chai(n):
    print(n)
    if n==0:
        return "All cups poured"
    return pour_chai(n-1)

print(pour_chai(3))

#Lambdas 
chai_types =["light","kadak","ginger","kadak"]

strong_chai=list(filter(lambda chai:chai=="kadak", chai_types))

print(strong_chai)

strong_chai=list(filter(lambda chai:chai!="kadak", chai_types))
                              #iter:iter=="whatever", list
print(strong_chai)
