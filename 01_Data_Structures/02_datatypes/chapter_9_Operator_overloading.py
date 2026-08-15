base_liquid=["water","milk"]
extra_flavor=["ginger"]
full_liquid_mix=base_liquid+extra_flavor
#The + operator is not supposed to add two lists but it is still adding
#This functionality is called as opperator overloading
print(f"Full liquid mix: {full_liquid_mix}")

raw_spice_data=bytearray(b"CINNAMON")
raw_spice_data=raw_spice_data.replace(b"CINNA",b"CARDA")
print(f"Bytes:{raw_spice_data}")