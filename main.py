from storage import FakeStorage
from managers import ExpenseManager, BudgetManager
from ui import (
    add_expense_interactively,
    display_expenses,
    edit_expense_interactively,
    delete_expense_interactively,
    search_expenses_interactively,
    show_total_spent,
    set_budget_interactively,
    check_budget_interactively,
)


def main():
    storage = FakeStorage()

    expenses = ExpenseManager(storage)
    budgets = BudgetManager(storage)

    while True:
        print("\n" + "=" * 45)
        print("        EXPENSE TRACKER")
        print("=" * 45)

        print("1. Add an expense")
        print("2. Show all expenses")
        print("3. Edit an expense")
        print("4. Delete an expense")
        print("5. Search expenses")
        print("6. Show total spent")
        print("7. Set a budget for a category")
        print("8. Check budget status for a month")
        print("9. Quit")

        choice = input("\nEnter 1-9: ").strip()

        if choice == "1":
            add_expense_interactively(expenses)

        elif choice == "2":
            display_expenses(expenses.get_all_expenses())

        elif choice == "3":
            edit_expense_interactively(expenses)

        elif choice == "4":
            delete_expense_interactively(expenses)

        elif choice == "5":
            search_expenses_interactively(expenses)

        elif choice == "6":
            show_total_spent(expenses)

        elif choice == "7":
            set_budget_interactively(budgets)

        elif choice == "8":
            check_budget_interactively(expenses, budgets)

        elif choice == "9":
            print("\nThank you for using Expense Tracker!")
            print("Goodbye!")
            break

        else:
            print(
                "\nInvalid choice. "
                "Please enter a number from 1 to 9."
            )


if __name__ == "__main__":
    main()
