def chai_flavor(flavor="masala"):
    """Return the flavor of the chai"""
    return

print(chai_flavor.__doc__)
print(chai_flavor.__name__)

def generate_bill(chai=0,samosa=0):
    """
    Calculate total bill for Samosa and Chai
    Chai-20
    Samosa-30
    return total amont and thank you message
    """
    total=chai*20 + samosa*30

    return total, "Thank you for visiting chai.com"

print(generate_bill(chai=2,samosa=4))

    