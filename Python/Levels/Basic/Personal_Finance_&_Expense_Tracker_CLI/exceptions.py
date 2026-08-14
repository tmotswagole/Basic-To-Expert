"""Custom exceptions for the finance tracker CLI.

This module will define domain-specific error types.
"""


class FinanceError(Exception):
    """Base exception for finance tracker errors."""


class InvalidAmountError(FinanceError):
    """Raised when a transaction amount is invalid."""


class TransactionNotFoundError(FinanceError):
    """Raised when a transaction cannot be found."""


class InvalidCategoryError(FinanceError):
    """Raised when a category is invalid."""


class BudgetExceededError(FinanceError):
    """Raised when a category budget is exceeded."""
