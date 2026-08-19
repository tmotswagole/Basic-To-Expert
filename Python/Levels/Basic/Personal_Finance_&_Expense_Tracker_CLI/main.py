"""Entry point for the Personal Finance Tracker CLI.

This file will orchestrate the application and hold the main menu loop.
"""

from __future__ import annotations

try:
    from .exceptions import FinanceError
    from .tracker import FinanceTracker
    from .utils import format_money, print_heading
except ImportError:
    from exceptions import FinanceError
    from tracker import FinanceTracker
    from utils import format_money, print_heading


def print_transactions(transactions) -> None:
    if not transactions:
        print("No transactions found.")
        return
    for item in transactions:
        print(
            f"{item.id:>3} | {item.transaction_type:<7} | {format_money(item.amount):>10} | "
            f"{item.category:<15} | {item.description}"
        )


def add_transaction_cli(tracker: FinanceTracker) -> None:
    try:
        transaction_type = input("Type (income/expense): ")
        amount = float(input("Amount: "))
        category = input("Category: ")
        description = input("Description: ")
        tracker.add_transaction(transaction_type, amount, category, description)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
    except FinanceError as exc:
        print(f"Error: {exc}")
    else:
        print("Transaction added.")
    finally:
        print("Returning to menu...")


def main() -> None:
    tracker = FinanceTracker()
    while True:
        print_heading("PERSONAL FINANCE TRACKER")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. View summary")
        print("4. Set budget")
        print("5. View budget")
        print("6. Search transactions")
        print("7. Delete transaction")
        print("8. Add category")
        print("9. Monthly report")
        print("10. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction_cli(tracker)
        elif choice == "2":
            print_transactions(tracker.list_transactions())
        elif choice == "3":
            print(tracker.summary())
        elif choice == "4":
            try:
                tracker.set_budget(input("Category: "), float(input("Monthly budget: ")))
                print("Budget saved.")
            except (ValueError, FinanceError) as exc:
                print(f"Error: {exc}")
        elif choice == "5":
            for status in tracker.budget_statuses():
                print(
                    f"{status['category']}: budget {format_money(status['budget'])}, "
                    f"spent {format_money(status['spent'])}, "
                    f"remaining {format_money(status['remaining'])}"
                )
        elif choice == "6":
            print_transactions(tracker.search_transactions(text=input("Search text: ")))
        elif choice == "7":
            try:
                deleted = tracker.delete_transaction(int(input("Transaction ID: ")))
                print(f"Deleted transaction {deleted.id}.")
            except (ValueError, FinanceError) as exc:
                print(f"Error: {exc}")
        elif choice == "8":
            try:
                print(f"Added category: {tracker.add_category(input('Category: '))}")
            except FinanceError as exc:
                print(f"Error: {exc}")
        elif choice == "9":
            print(tracker.monthly_report())
        elif choice == "10":
            print("Goodbye.")
            break
        else:
            print("Choose a valid option.")


if __name__ == "__main__":
    main()
