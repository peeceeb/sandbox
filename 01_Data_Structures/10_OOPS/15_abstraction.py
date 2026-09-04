from abc import ABC, abstractmethod


# An abstract class defines what every chai type must be able to do.
class Chai(ABC):
    @abstractmethod
    def prepare(self):
        """Prepare the chai. Each child class supplies its own steps."""

    def serve(self):
        # This shared method uses the abstract behavior without knowing its details.
        print("Serving the chai.")


class MasalaChai(Chai):
    def prepare(self):
        # The customer only calls prepare(); these internal steps are hidden.
        print("Boiling tea with ginger, cardamom, and cloves.")


class GreenTea(Chai):
    def prepare(self):
        print("Steeping green tea leaves in hot water.")


def make_and_serve(chai):
    """Works with any object that follows the Chai abstraction."""
    chai.prepare()
    chai.serve()


masala_chai = MasalaChai()
green_tea = GreenTea()

make_and_serve(masala_chai)
make_and_serve(green_tea)

# Chai() cannot be created because it has no implementation of prepare().