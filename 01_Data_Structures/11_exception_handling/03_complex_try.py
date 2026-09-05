# chai_menu={"masala":30, "ginger":40}

# print("Hello chai code")

def serve_chai(flavor):
    try:
        print(f"Preparing {flavor} chai")
        if flavor.lower()=="unknown":
            raise ValueError("We dont know that flavor")
    except ValueError as e:
        print("Error",e)
    else:
        print(f"{flavor} chai is served")
    finally:
        print(f"Next customer please!")

#serve_chai("masala")
serve_chai("UnKnown")
#serve_chai("unknown")

