class BaseChai:
    def __init__(self, type_):
        self.type=type_

    def prepare(self):
        print(f"Preparing {self.type} chai...")

class MasalaChai(BaseChai):
    def add_spices(self):
        print("Adding cardamon, ginger, cloves.")


Amit=MasalaChai("Masala")
Amit.prepare()
Amit.add_spices()

#Composition
class ChaiShop:
    chai_cls= BaseChai  #Refernce of the Basechai

    def __init__(self):
        self.chai=self.chai_cls("Regular") #Creates an object Regular of class BaseChai and passing the reference in self.chai


    def serve(self):
        print(f"Serving {self.chai.type} chai in the shop")      #Access the attribute of basechai
        self.chai.prepare() #Access the method of basechai

class FancyChaiShop(ChaiShop):
    chai_cls=MasalaChai

#shop = ChaiShop()
#fancy = FancyChaiShop()

#shop.serve()
#fancy.serve()

#fancy.chai_cls.add_spices() doesnot have context throws error
#fancy.chai.add_spices() #Has context