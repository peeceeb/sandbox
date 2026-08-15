names = ["Prasanna","Arya","Sanket", "Nayana"]
bills = [50,80,90,30]

for name, bill in zip(names,bills):
    print(f"Customer {name} has ${bill} bill due")
