"""Core finance tracker logic.

This module will manage transactions, budgets, and reporting behavior.
"""

from __future__ import annotations

try:
    from .budgets import BudgetManager
    from .reports import ReportGenerator
    from .transactions import TransactionManager
except ImportError:
    from budgets import BudgetManager
    from reports import ReportGenerator
    from transactions import TransactionManager


class FinanceTracker:
    def __init__(
        self,
        transaction_manager: TransactionManager | None = None,
        budget_manager: BudgetManager | None = None,
        report_generator: ReportGenerator | None = None,
    ):
        self.transaction_manager = transaction_manager or TransactionManager()
        self.budget_manager = budget_manager or BudgetManager(self.transaction_manager.categories)
        self.report_generator = report_generator or ReportGenerator()

    def add_transaction(self, transaction_type: str, amount: float, category: str, description: str = ""):
        return self.transaction_manager.add_transaction(
            transaction_type=transaction_type,
            amount=amount,
            category=category,
            description=description,
        )

    def list_transactions(self):
        return self.transaction_manager.get_transactions()

    def delete_transaction(self, transaction_id: int):
        return self.transaction_manager.delete_transaction(transaction_id)

    def add_category(self, category: str):
        return self.transaction_manager.add_category(category)

    def set_budget(self, category: str, amount: float):
        return self.budget_manager.set_budget(category, amount)

    def budget_statuses(self):
        return self.budget_manager.iter_budget_statuses(self.list_transactions())

    def summary(self) -> str:
        return self.report_generator.summary(self.list_transactions())

    def monthly_report(self) -> str:
        return self.report_generator.monthly_report(self.list_transactions())

    def search_transactions(self, **filters):
        return self.transaction_manager.search_transactions(**filters)
