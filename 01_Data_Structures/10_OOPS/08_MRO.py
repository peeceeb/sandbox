class A:
    label = "A: Base Class"

class B(A):
    label = "B: Masala Blend"

class C(A):
    label = "C: Herbal Blend"

class D(C,B):#order of inheritance matters
    pass

cup=D()
print(cup.label)
print(D.__mro__)
print(C.__mro__)