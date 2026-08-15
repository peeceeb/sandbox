chai_menu={"masala":30, "ginger":40}

#chai_menu["elaichi"] ##What if this is a sensitive call

try:
    chai_menu["elaichi"]
except KeyError:
    print("The key that you are trying to access does not exist")
