"""Budget management logic.

This module will store budget rules and calculate remaining amounts.
"""

from __future__ import annotations

try:
    from .exceptions import BudgetExceededError, InvalidAmountError, InvalidCategoryError
    from .models import Transaction
    from .utils import normalize_text
except ImportError:
    from exceptions import BudgetExceededError, InvalidAmountError, InvalidCategoryError
    from models import Transaction
    from utils import normalize_text


class BudgetManager:
    def __init__(self, categories: set[str]):
        self.categories = categories
        self.budgets: dict[str, float] = {}

    def set_budget(self, category: str, amount: float) -> None:
        category = normalize_text(category)
        if amount <= 0:
            raise InvalidAmountError("Budget must be greater than zero.")
        if category not in self.categories:
            raise InvalidCategoryError(f"Unknown category '{category}'.")
        self.budgets[category] = float(amount)

    def get_budget_status(
        self, category: str, transactions: list[Transaction]
    ) -> dict[str, float | str]:
        category = normalize_text(category)
        if category not in self.budgets:
            raise InvalidCategoryError(f"No budget has been set for '{category}'.")

        spent = sum(
            item.amount
            for item in transactions
            if item.transaction_type == "expense" and item.category == category
        )
        budget = self.budgets[category]
        remaining = budget - spent
        if remaining < 0:
            raise BudgetExceededError(
                f"{category.title()} budget exceeded by {abs(remaining):.2f}."
            )
        return {
            "category": category,
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
        }

    def iter_budget_statuses(
        self, transactions: list[Transaction]
    ) -> list[dict[str, float | str]]:
        statuses = []
        for category, budget in self.budgets.items():
            spent = sum(
                item.amount
                for item in transactions
                if item.transaction_type == "expense" and item.category == category
            )
            statuses.append(
                {
                    "category": category,
                    "budget": budget,
                    "spent": spent,
                    "remaining": budget - spent,
                }
            )
        return statuses
