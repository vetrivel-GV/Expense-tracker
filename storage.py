class FakeStorage:
    """
    Simple in-memory storage.

    Data remains available while the program is running.
    It is not permanent storage.
    """

    def __init__(self):
        self.stuff = {
            "expenses": {},
            "budgets": {}
        }

    def load_data(self, key):
        """Loads data."""
        return self.stuff.get(key, {})

    def save_data(self, data, key):
        """Saves data."""
        self.stuff[key] = data
