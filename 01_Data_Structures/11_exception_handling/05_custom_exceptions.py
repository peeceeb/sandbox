def brew_chai(flavor):
    if flavor not in ["masala","ginger","elaichi"]:
        raise ValueError("Doesnot exist such chai")
    print(f"brewing {flavor} chai..")

brew_chai("masala")