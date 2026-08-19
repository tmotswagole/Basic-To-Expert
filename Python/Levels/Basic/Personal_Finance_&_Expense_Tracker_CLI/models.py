"""Domain models for the finance tracker.

This module will contain the core data models used across the project.
"""

from __future__ import annotations

from dataclasses import dataclass


TRANSACTION_TYPES = ("income", "expense")


@dataclass(frozen=True)
class Transaction:
    id: int
    transaction_type: str
    amount: float
    category: str
    description: str = ""

    def calculate_effect(self) -> float:
        raise NotImplementedError


class Income(Transaction):
    def __init__(self, id: int, amount: float, category: str, description: str = ""):
        super().__init__(id, "income", amount, category, description)

    def calculate_effect(self) -> float:
        return self.amount


class Expense(Transaction):
    def __init__(self, id: int, amount: float, category: str, description: str = ""):
        super().__init__(id, "expense", amount, category, description)

    def calculate_effect(self) -> float:
        return -self.amount
