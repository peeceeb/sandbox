masala_spices=("cardamom","cloves","cinnamon")

spice1,spice2,spice3=masala_spices
print(f"Main masala spices: {spice1}, {spice2}, {spice3}")
print(type(spice1))

(spice1,spice2,spice3)=masala_spices
print(f"Main masala spices: {spice1}, {spice2}, {spice3}")
print(type(spice1))


ginger_ratio, cardamon_ratio=2,1
print(f"ginger_ratio,{ginger_ratio}")
cardamon_ratio,ginger_ratio=ginger_ratio,cardamon_ratio
print(f"cardamom_ratio,{cardamon_ratio}")

#membership
print(f"Is ginger in Masala spices? {'ginger' in masala_spices}")
print(f"Is cardamom in Masala spices? {'cardamom' in masala_spices}")
