essential_spices={"cardamom","ginger","cinnamon"}
print(f"essential_spices:{essential_spices}")

optional_spices={"cloves","ginger","black pepper"}
print(f"optional_spices:{optional_spices}")

all_spices=essential_spices|optional_spices
print(f"All Spices:, {all_spices}")

common_spices=essential_spices & optional_spices
print(f"Common Spices:, {common_spices}")

Spices_Only_in_A=essential_spices-optional_spices
print(f"Spices only in A: {Spices_Only_in_A}")
    
print(f"Is clove in optional spices,{'cloves' in optional_spices}")