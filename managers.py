import datetime
import math

from models import Expense, ExpenseTrackerError


class ExpenseManager:
    """Manages all expense-related operations."""

    def __init__(self, storage_manager):
        self.storage = storage_manager
        self.expenses = self._load_expenses()

    def _load_expenses(self):
        """Loads expenses from storage."""
        data = self.storage.load_data("expenses")
        expenses = {}

        for exp_id, exp_data in data.items():
            try:
                expenses[exp_id] = Expense.from_dict(exp_data)
            except (ExpenseTrackerError, KeyError, TypeError):
                continue

        return expenses

    def _save_expenses(self):
        """Saves current expenses to storage."""
        data = {
            exp.expense_id: exp.to_dict()
            for exp in self.expenses.values()
        }
        self.storage.save_data(data, "expenses")

    def add_expense(self, amount, category, description=None, date=None):
        """Adds a new expense."""
        expense = Expense(amount, category, description, date)
        self.expenses[expense.expense_id] = expense
        self._save_expenses()
        return expense

    def get_expense(self, expense_id):
        """Retrieves a single expense by its ID."""
        expense = self.expenses.get(expense_id)

        if not expense:
            raise ExpenseTrackerError(
                f"Expense with ID {expense_id} not found."
            )

        return expense

    def get_all_expenses(self):
        """Returns all expenses sorted by date."""
        return sorted(
            self.expenses.values(),
            key=lambda exp: exp.date,
            reverse=True
        )

    def edit_expense(
        self,
        expense_id,
        amount=None,
        category=None,
        description=None,
        date=None,
    ):
        """Edits an existing expense."""
        expense = self.get_expense(expense_id)

        if amount is not None:
            try:
                new_amount = float(amount)
            except (ValueError, TypeError):
                raise ExpenseTrackerError(
                    "Invalid amount. Please enter a number."
                )

            if not math.isfinite(new_amount):
                raise ExpenseTrackerError("Amount must be a valid number.")

            if new_amount < 0:
                raise ExpenseTrackerError(
                    "Expense amount cannot be negative."
                )

            expense.amount = new_amount

        if category is not None:
            if not category.strip():
                raise ExpenseTrackerError("Category cannot be empty.")

            expense.category = category.strip().lower()

        if description is not None:
            description = description.strip() if description else ""
            expense.description = description if description else None

        if date is not None:
            expense.date = expense._parse_date(date)

        self._save_expenses()
        return expense

    def delete_expense(self, expense_id):
        """Deletes an expense by its ID."""
        if expense_id not in self.expenses:
            raise ExpenseTrackerError(
                f"Expense with ID {expense_id} not found."
            )

        del self.expenses[expense_id]
        self._save_expenses()

    def search(self, keyword):
        """Searches expenses by category or description."""
        if not keyword:
            return self.get_all_expenses()

        keyword = keyword.lower().strip()

        results = [
            exp
            for exp in self.expenses.values()
            if (
                keyword in exp.category
                or (
                    exp.description
                    and keyword in exp.description.lower()
                )
            )
        ]

        return sorted(
            results,
            key=lambda exp: exp.date,
            reverse=True
        )

    def total_spent(self):
        """Calculates total amount spent."""
        return sum(
            exp.amount
            for exp in self.expenses.values()
        )

    def get_by_month(self, month_key_str):
        """Retrieves expenses for a specific month."""
        try:
            datetime.datetime.strptime(month_key_str, "%Y-%m")
        except ValueError:
            raise ExpenseTrackerError(
                "Invalid month format. Use YYYY-MM."
            )

        return sorted(
            [
                exp
                for exp in self.expenses.values()
                if exp.date.strftime("%Y-%m") == month_key_str
            ],
            key=lambda exp: exp.date,
            reverse=True
        )


class BudgetManager:
    """Manages budget-related operations."""

    def __init__(self, storage_manager):
        self.storage = storage_manager
        self.budgets = self._load_budgets()

    def _load_budgets(self):
        """Loads budgets from storage."""
        return self.storage.load_data("budgets")

    def _save_budgets(self):
        """Saves current budgets to storage."""
        self.storage.save_data(self.budgets, "budgets")

    def set_budget(self, category, amount):
        """Sets a monthly budget for a category."""
        if not category or not category.strip():
            raise ExpenseTrackerError("Category cannot be empty.")

        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ExpenseTrackerError(
                "Invalid amount. Please enter a number."
            )

        if not math.isfinite(amount):
            raise ExpenseTrackerError(
                "Budget amount must be a valid number."
            )

        if amount < 0:
            raise ExpenseTrackerError(
                "Budget amount cannot be negative."
            )

        category = category.strip().lower()
        self.budgets[category] = amount
        self._save_budgets()

    def get_budget(self, category):
        """Retrieves the budget for a category."""
        return self.budgets.get(category.strip().lower(), 0.0)

    def check_status(self, expenses):
        """Checks budget status for the provided month's expenses."""
        status_report = []
        category_spent = {}

        for expense in expenses:
            category_spent[expense.category] = (
                category_spent.get(expense.category, 0.0)
                + expense.amount
            )

        for category, budget_amount in self.budgets.items():
            spent = category_spent.get(category, 0.0)
            remaining = budget_amount - spent

            status = (
                "Under budget"
                if remaining >= 0
                else "Over budget"
            )

            status_report.append({
                "category": category.title(),
                "budget": budget_amount,
                "spent": spent,
                "remaining": remaining,
                "status": status,
            })

        return status_report
