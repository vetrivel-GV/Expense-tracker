from models import ExpenseTrackerError


def display_expenses(expense_list):
    """Displays a list of expenses."""
    if not expense_list:
        print("\nNo expenses found.")
        return

    print("\n--- Expenses ---")

    for expense in expense_list:
        print(expense)


def add_expense_interactively(expenses):
    """Adds an expense using user input."""
    amount = input("Amount: ")
    category = input("Category: ")
    description = input("Description (optional): ")
    date = input(
        "Date YYYY-MM-DD (leave blank for today): "
    )

    try:
        expense = expenses.add_expense(
            amount, category, description, date
        )
        print("\nExpense added successfully!")
        print(expense)
    except ExpenseTrackerError as err:
        print("Oops:", err)


def edit_expense_interactively(expenses):
    """Edits an existing expense."""
    expense_id = input("Enter expense ID: ").strip()

    try:
        expense = expenses.get_expense(expense_id)

        print("\nCurrent expense:")
        print(expense)

        print("\nLeave a field blank to keep the current value.")

        amount = input("New amount: ").strip()
        category = input("New category: ").strip()
        description = input(
            "New description (leave blank to keep current): "
        ).strip()
        date = input(
            "New date YYYY-MM-DD (leave blank to keep current): "
        ).strip()

        amount = amount if amount else None
        category = category if category else None
        description = description if description else None
        date = date if date else None

        updated = expenses.edit_expense(
            expense_id,
            amount,
            category,
            description,
            date
        )

        print("\nExpense updated successfully!")
        print(updated)

    except ExpenseTrackerError as err:
        print("Oops:", err)


def delete_expense_interactively(expenses):
    """Deletes an expense."""
    expense_id = input("Enter expense ID: ").strip()

    try:
        expense = expenses.get_expense(expense_id)

        print("\nExpense to delete:")
        print(expense)

        confirm = input(
            "Are you sure? (y/n): "
        ).strip().lower()

        if confirm == "y":
            expenses.delete_expense(expense_id)
            print("Expense deleted successfully!")
        else:
            print("Delete cancelled.")

    except ExpenseTrackerError as err:
        print("Oops:", err)


def search_expenses_interactively(expenses):
    """Searches expenses."""
    keyword = input(
        "Enter category or description keyword: "
    )

    results = expenses.search(keyword)
    display_expenses(results)


def show_total_spent(expenses):
    """Displays total amount spent."""
    total = expenses.total_spent()
    print(f"\nTotal spent: ${total:.2f}")


def set_budget_interactively(budgets):
    """Sets a category budget."""
    category = input("Category: ")
    amount = input("Monthly budget amount: ")

    try:
        budgets.set_budget(category, amount)
        print("Budget set successfully!")
    except ExpenseTrackerError as err:
        print("Oops:", err)


def check_budget_interactively(expenses, budgets):
    """Checks budget status for a month."""
    month = input("Month YYYY-MM: ").strip()

    try:
        month_expenses = expenses.get_by_month(month)
        status_report = budgets.check_status(month_expenses)

        if not status_report:
            print("\nNo budgets have been set.")
            return

        print(f"\n--- Budget Status for {month} ---")

        for status in status_report:
            print(f"\nCategory: {status['category']}")
            print(f"Budget: ${status['budget']:.2f}")
            print(f"Spent: ${status['spent']:.2f}")
            print(f"Remaining: ${status['remaining']:.2f}")
            print(f"Status: {status['status']}")

    except ExpenseTrackerError as err:
        print("Oops:", err)
