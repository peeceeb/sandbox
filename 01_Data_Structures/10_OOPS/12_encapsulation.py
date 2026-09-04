class ChaiWallet:
    """Stores a wallet balance and controls how it can be changed."""

    def __init__(self, owner, opening_balance=0):
        self.owner = owner  # Public attribute: intended for normal use.
        self._currency = "INR"  # Protected by convention: internal detail.
        self.__balance = opening_balance  # Private: name-mangled to avoid direct access.

    def add_money(self, amount):
        """Add a positive amount to the wallet."""
        if amount <= 0:
            raise ValueError("Amount to add must be positive.")
        self.__balance += amount

    def spend_money(self, amount):
        """Spend only a positive amount that is available in the wallet."""
        if amount <= 0:
            raise ValueError("Amount to spend must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient wallet balance.")
        self.__balance -= amount

    def get_balance(self):
        """Provide read-only access to the private balance."""
        return f"{self._currency} {self.__balance}"


wallet = ChaiWallet("Asha", 100)
wallet._currency="USD"  # This is allowed, but not recommended; it's a protected attribute.
wallet.__balance = 100000  # This creates a new attribute; it does not change the private balance.
print(f"Owner: {wallet.owner}")
print(f"Starting balance: {wallet.get_balance()}")

wallet.add_money(50)
wallet.spend_money(70)
print(f"Balance after transactions: {wallet.get_balance()}")

try:
    wallet.spend_money(200)
except ValueError as error:
    print(f"Transaction rejected: {error}")

# wallet.__balance = 100000  # This creates a new attribute; it does not change the private balance.