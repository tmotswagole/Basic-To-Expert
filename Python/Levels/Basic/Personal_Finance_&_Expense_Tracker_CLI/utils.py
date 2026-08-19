"""Utility helpers.

This module will hold reusable helper functions for formatting and validation.
"""

from __future__ import annotations


def normalize_text(value: str) -> str:
    """Normalize menu/category/type input without hiding empty values."""
    return value.strip().lower()


def format_money(amount: float) -> str:
    return f"P{amount:,.2f}".rstrip("0").rstrip(".")


def print_heading(title: str) -> None:
    line = "=" * max(20, len(title) + 8)
    print(line)
    print(title.center(len(line)))
    print(line)
