import sys

x=10
print(x)
print(id(x))  # Prints the memory address of x
print(hex(id(x)))  # Prints the memory address in hexadecimal format

x+=1
print(x)
print(id(x))  # Prints the memory address of x
print(hex(id(x)))  # Prints the memory address in hexadecimal format


items=[1,2,3]
items.append(4)
print(items)
print(id(items))  # Prints the memory address of items
print(hex(id(items)))  # Prints the memory address in hexadecimal format
items.append(5)
print(items)
print(id(items))  # Prints the memory address of items
print(hex(id(items)))  # Prints the memory address in hexadecimal format

print(f"Reference count of x: {sys.getrefcount(x)}")  # Prints the reference count of x
print(f"Reference count of items: {sys.getrefcount(items)}")  # Prints the reference count of items

