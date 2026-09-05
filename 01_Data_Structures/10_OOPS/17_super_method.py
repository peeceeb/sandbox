class Chai:
    def __init__(self, tea_type):
        self.tea_type = tea_type
        print(f"Base chai created: {self.tea_type}")

    def prepare(self):
        print(f"Preparing {self.tea_type} chai with milk and tea leaves.")


class MasalaChai(Chai):
    def __init__(self, tea_type, spice_level):
        # super() calls the parent class constructor and initializes tea_type.
        super().__init__(tea_type)
        self.spice_level = spice_level

    def prepare(self):
        # Reuse the parent's preparation steps before adding child-specific work.
        super().prepare()
        print(f"Adding spices at {self.spice_level} level.")


masala_chai = MasalaChai("Masala", "medium")
masala_chai.prepare()

# Without super(), MasalaChai would need to repeat Chai's initialization and prepare logic.