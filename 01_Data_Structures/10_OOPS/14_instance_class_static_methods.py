class ChaiOrder:
    shop_name = "Chai Corner"  # Class attribute: shared by every order.

    def __init__(self, tea_type, cups):
        self.tea_type = tea_type  # Instance attribute: belongs to one order.
        self.cups = cups

    # INSTANCE METHOD: receives self, so it can use this order's data.
    def describe(self):
        return f"{self.cups} cup(s) of {self.tea_type} chai"

    # CLASS METHOD: receives cls, so it can use class-level data or create objects.
    @classmethod
    def from_string(cls, order_text):
        tea_type, cups = order_text.split(",")
        return cls(tea_type, int(cups))

    @classmethod
    def change_shop_name(cls, new_name):
        cls.shop_name = new_name  # Changes the shared class attribute.

    # STATIC METHOD: receives neither self nor cls; it is a related utility function.
    @staticmethod
    def is_valid_cup_count(cups):
        return cups > 0


order = ChaiOrder("Masala", 2)
print(order.describe())  # Instance method uses this order's tea_type and cups.

online_order = ChaiOrder.from_string("Ginger,3")
print(online_order.describe())  # Class method creates a new ChaiOrder instance.

ChaiOrder.change_shop_name("Evening Chai")
print(ChaiOrder.shop_name)  # Class method changed data shared by all orders.

print(ChaiOrder.is_valid_cup_count(4))  # Static method checks data without object state.
print(ChaiOrder.is_valid_cup_count(0))

"""
Use an **instance method** when the action needs data from one specific object.

Example: An order needs its own items, customer, and total.

```python
order.calculate_total()
order.cancel()
```

Use a **class method** when the action concerns the whole class or creates objects in an alternative way.

Example: Create an order from API data, change a shared tax rate, or track the number of orders.

```python
Order.from_api_response(data)
Order.set_tax_rate(0.18)
```

Use a **static method** for a helper related to the class but needing neither object data nor class data.

Example: Validate an email, coupon code, or password before creating a customer.

```python
Customer.is_valid_email("asha@example.com")
Coupon.is_valid_code("SAVE10")
```

Quick rule:
- Needs one object’s state: instance method (`self`)
- Needs shared class state or constructs objects: class method (`cls`)
- Needs neither, but belongs conceptually with the class: static method
"""