
def infinite_chai():
    count=1
    while True:
        yield f"Refill #{count}"
        count+=1

User1 =infinite_chai()
User2 =infinite_chai()

for __ in range(33):
    print(next(User1))

for __ in range(30):
    print(next(User2))