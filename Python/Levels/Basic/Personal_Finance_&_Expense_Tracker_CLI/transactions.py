"""Transaction-related logic.

This module will handle transaction creation, lookup, deletion, and filtering.
"""

from __future__ import annotations

try:
    from .exceptions import InvalidAmountError, InvalidCategoryError, TransactionNotFoundError
    from .models import Expense, Income, TRANSACTION_TYPES, Transaction
    from .utils import normalize_text
except ImportError:
    from exceptions import InvalidAmountError, InvalidCategoryError, TransactionNotFoundError
    from models import Expense, Income, TRANSACTION_TYPES, Transaction
    from utils import normalize_text


DEFAULT_CATEGORIES = {
    "food",
    "transport",
    "rent",
    "entertainment",
    "utilities",
    "salary",
    "freelance",
}


class TransactionManager:
    def __init__(self, categories: set[str] | None = None):
        self.transactions: list[Transaction] = []
        self.categories: set[str] = set(categories or DEFAULT_CATEGORIES)
        self._next_id = 1

    def add_category(self, category: str) -> str:
        category = normalize_text(category)
        if not category:
            raise InvalidCategoryError("Category cannot be empty.")
        self.categories.add(category)
        return category

    def add_transaction(
        self,
        transaction_type: str,
        amount: float,
        category: str,
        description: str = "",
    ) -> Transaction:
        transaction_type = normalize_text(transaction_type)
        category = normalize_text(category)

        if transaction_type not in TRANSACTION_TYPES:
            raise ValueError(f"Type must be one of: {', '.join(TRANSACTION_TYPES)}.")
        if amount <= 0:
            raise InvalidAmountError("Amount must be greater than zero.")
        if category not in self.categories:
            raise InvalidCategoryError(
                f"Unknown category '{category}'. Add it before using it."
            )

        cls = Income if transaction_type == "income" else Expense
        transaction = cls(self._next_id, float(amount), category, description.strip())
        self.transactions.append(transaction)
        self._next_id += 1
        return transaction

    def get_transactions(self) -> list[Transaction]:
        return list(self.transactions)

    def find_transaction(self, transaction_id: int) -> Transaction | None:
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None

    def delete_transaction(self, transaction_id: int) -> Transaction:
        transaction = self.find_transaction(transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(f"Transaction {transaction_id} was not found.")
        self.transactions.remove(transaction)
        return transaction

    def filter_transactions(self, field: str, *values: str) -> list[Transaction]:
        allowed = set(values)
        return [
            transaction
            for transaction in self.transactions
            if str(getattr(transaction, field, "")) in allowed
        ]

    def search_transactions(self, **filters: object) -> list[Transaction]:
        results = self.transactions
        category = filters.get("category")
        transaction_type = filters.get("transaction_type")
        min_amount = filters.get("min_amount")
        max_amount = filters.get("max_amount")
        text = filters.get("text")

        if category is not None:
            results = [item for item in results if item.category == normalize_text(str(category))]
        if transaction_type is not None:
            results = [
                item
                for item in results
                if item.transaction_type == normalize_text(str(transaction_type))
            ]
        if min_amount is not None:
            results = [item for item in results if item.amount >= float(min_amount)]
        if max_amount is not None:
            results = [item for item in results if item.amount <= float(max_amount)]
        if text:
            needle = str(text).lower()
            results = [
                item
                for item in results
                if needle in item.description.lower() or needle in item.category
            ]

        return list(results)


def add_transaction(transaction: Transaction, transactions: list[Transaction] | None = None):
    if transactions is None:
        transactions = []
    transactions.append(transaction)
    return transactions
