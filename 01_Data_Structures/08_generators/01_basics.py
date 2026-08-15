#Define generator
def serve_chai():
    yield "Cup1: Masala Chai"
    yield "Cup2: Ginger Chai"
    yield "Cup3: Elaichi Chai"

stall=serve_chai()

for cup in stall:
    print(cup)

#Normal function
def get_chai_list():
    return ["Cup 1", "Cup 2", "Cup 3"]

print(get_chai_list())

#generator functions:
def get_chai_gen():
    yield "Cup 1"
    yield "Cup 2"
    yield "Cup 3"

chai=get_chai_gen()
print(next(chai))
print(next(chai))
print(next(chai))
# print(next(chai))

