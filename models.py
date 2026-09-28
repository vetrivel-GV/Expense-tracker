import uuid
import datetime
import math


class ExpenseTrackerError(Exception):
    """Custom exception for expense tracker errors."""
    pass


class Expense:
    """Represents a single expense entry."""

    def __init__(self, amount, category, description, date, expense_id=None):
        self.expense_id = expense_id or str(uuid.uuid4())

        try:
            self.amount = float(amount)
        except (ValueError, TypeError):
            raise ExpenseTrackerError("Invalid amount. Please enter a number.")

        if not math.isfinite(self.amount):
            raise ExpenseTrackerError("Amount must be a valid number.")

        if self.amount < 0:
            raise ExpenseTrackerError("Expense amount cannot be negative.")

        if not category or not category.strip():
            raise ExpenseTrackerError("Category cannot be empty.")

        self.category = category.strip().lower()

        description = description.strip() if description else ""
        self.description = description if description else None

        self.date = self._parse_date(date)

    def _parse_date(self, date_str):
        """Parses a date string into a date object."""
        if not date_str:
            return datetime.date.today()

        try:
            return datetime.datetime.strptime(
                date_str, "%Y-%m-%d"
            ).date()
        except ValueError:
            raise ExpenseTrackerError(
                f"Invalid date format: {date_str}. Use YYYY-MM-DD."
            )

    def to_dict(self):
        """Converts the expense object to a dictionary."""
        return {
            "id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.strftime("%Y-%m-%d"),
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an Expense object from a dictionary."""
        return cls(
            data["amount"],
            data["category"],
            data.get("description"),
            data["date"],
            expense_id=data["id"],
        )

    def __str__(self):
        """String representation of the expense."""
        desc = f" ({self.description})" if self.description else ""

        return (
            f"ID: {self.expense_id[:8]}... | "
            f"Date: {self.date} | "
            f"Category: {self.category.title()} | "
            f"Amount: ${self.amount:.2f}{desc}"
        )
