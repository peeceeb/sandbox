def serve_chai():
    chai_type="Masala"
    print(f"Inside function: {chai_type}")

chai_type = "Lemon"
serve_chai()
print(f"Outside funtion: {chai_type}")

def chai_counter():
    chai_order="lemon" #Enclosing scope

    def print_order():
        chai_order="Ginger"
        print("Inner:", chai_order)
    print_order()
    print("Outer: ", chai_order)