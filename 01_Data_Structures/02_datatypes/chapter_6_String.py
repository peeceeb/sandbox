Customer_Name="Priya"
Chai_Type="Ginger_Tea"

print(f"Order for {Customer_Name} : {Chai_Type}")

Chai_Descritpion="Strong and less sugar"
print(f"First Word", {Chai_Descritpion[0:6:1]})
print(f"Specification ", {Chai_Descritpion[0:5:1]})
print(f"Step", {Chai_Descritpion[0:7:2]})
print(f"Last Word", {Chai_Descritpion[16:]})
print(f"Last Word", {Chai_Descritpion[::-1]})


label_txt="प्रसन्न"
print(f"label_txt{label_txt}")
encoded_label=label_txt.encode("utf-8")
print(f"Non Encoded Label: {encoded_label}")
print(f"Encoded Label: {encoded_label.decode("utf-8")}")
decoded_label=encoded_label.decode("utf-8")
print(f"Decoded Label: {decoded_label}")
