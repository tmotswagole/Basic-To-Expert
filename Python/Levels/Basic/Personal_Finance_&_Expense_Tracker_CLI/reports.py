"""Reporting and summary generation.

This module will format summary and monthly report output.
"""

from __future__ import annotations

try:
    from .models import Transaction
    from .utils import format_money
except ImportError:
    from models import Transaction
    from utils import format_money


class ReportGenerator:
    def totals_by_type(self, transactions: list[Transaction]) -> dict[str, float]:
        totals = {"income": 0.0, "expense": 0.0}
        for transaction in transactions:
            totals[transaction.transaction_type] += transaction.amount
        return totals

    def totals_by_category(
        self, transactions: list[Transaction], transaction_type: str | None = None
    ) -> dict[str, float]:
        totals: dict[str, float] = {}
        for transaction in transactions:
            if transaction_type and transaction.transaction_type != transaction_type:
                continue
            totals[transaction.category] = totals.get(transaction.category, 0.0) + transaction.amount
        return totals

    def summary(self, transactions: list[Transaction]) -> str:
        totals = self.totals_by_type(transactions)
        balance = totals["income"] - totals["expense"]
        category_totals = self.totals_by_category(transactions, "expense")
        lines = [
            "========== SUMMARY ==========",
            f"Income:   {format_money(totals['income'])}",
            f"Expenses: {format_money(totals['expense'])}",
            f"Balance:  {format_money(balance)}",
            "",
            "Top categories:",
        ]
        for category, amount in sorted(category_totals.items(), key=lambda item: item[1], reverse=True):
            lines.append(f"{category:<15} {format_money(amount)}")
        return "\n".join(lines)

    def monthly_report(self, transactions: list[Transaction]) -> str:
        income = self.totals_by_category(transactions, "income")
        expenses = self.totals_by_category(transactions, "expense")
        total_income = sum(income.values())
        total_expenses = sum(expenses.values())

        lines = ["================================", "          MONTHLY REPORT", "================================", ""]
        lines.append("Income")
        for category, amount in sorted(income.items()):
            lines.append(f"{category.title():<20} {format_money(amount):>10}")
        lines.append(f"{'Total':<20} {format_money(total_income):>10}")
        lines.extend(["", "Expenses"])
        for category, amount in sorted(expenses.items()):
            lines.append(f"{category.title():<20} {format_money(amount):>10}")
        lines.append(f"{'Total':<20} {format_money(total_expenses):>10}")
        lines.extend(["", f"{'Balance':<20} {format_money(total_income - total_expenses):>10}"])
        return "\n".join(lines)
