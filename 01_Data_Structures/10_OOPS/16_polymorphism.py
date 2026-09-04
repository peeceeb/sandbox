class MasalaChai:
    def prepare(self):
        # Same method name, but this class has its own preparation behavior.
        print("Preparing masala chai with ginger and cardamom.")


class GreenTea:
    def prepare(self):
        # The same method name has different behavior for green tea.
        print("Steeping green tea leaves without milk.")


class LemonTea:
    def prepare(self):
        print("Mixing black tea with lemon and honey.")


def serve_chai(chai):
    """Accepts any object that provides a prepare() method."""
    chai.prepare()
    print("Chai served.\n")


# POLYMORPHISM: one function sends the same message, prepare(), to many object types.
chai_menu = [MasalaChai(), GreenTea(), LemonTea()]

for chai in chai_menu:
    serve_chai(chai)