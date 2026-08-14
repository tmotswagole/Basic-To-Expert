# Project: Python Personal Finance Tracker CLI

You are building a command-line application that lets a user manage income, expenses, budgets, and transactions.

Example:

```text
========================================
        PERSONAL FINANCE TRACKER
========================================

1. Add transaction
2. View transactions
3. View summary
4. Set budget
5. View budget
6. Search transactions
7. Delete transaction
8. Exit

Choose an option: 1

Type: expense
Amount: 250
Category: food
Description: Groceries

Transaction added.
```

Later:

```text
Choose an option: 3

========== SUMMARY ==========

Income:       P15,000
Expenses:     P7,250
Balance:      P7,750

Top categories:

food          P2,500
transport     P1,800
entertainment P1,200
```

## Why this project fits your Python study

You'll naturally use:

* `list`
* `dict`
* `set`
* `tuple`
* mutable vs immutable objects
* `is` vs `==`
* functions
* `*args`
* `**kwargs`
* classes
* objects
* inheritance
* composition
* exceptions
* custom exceptions
* `try`
* `except`
* `else`
* `finally`

And because it's Python-only, you can focus entirely on the language.

---

# Stage 1 — Transactions

Start with a simple list:

```python
transactions = []
```

Each transaction can initially be a dictionary:

```python
{
    "id": 1,
    "type": "expense",
    "amount": 250,
    "category": "food",
    "description": "Groceries"
}
```

Your program should allow:

```text
Add transaction
View transactions
Delete transaction
```

### Your first challenge

Write:

```python
def add_transaction(...):
    ...
```

Don't worry about classes yet.

---

# Stage 2 — Lists and dictionaries

Implement:

```python
def get_transactions():
    ...


def delete_transaction(transaction_id):
    ...


def find_transaction(transaction_id):
    ...
```

You'll be manipulating lists and dictionaries constantly.

For example:

```python
for transaction in transactions:
    if transaction["id"] == transaction_id:
        ...
```

This is where you should get comfortable with mutation.

---

# Stage 3 — Sets

Categories shouldn't be duplicated.

Create:

```python
categories = {
    "food",
    "transport",
    "rent",
    "entertainment",
    "utilities"
}
```

When somebody creates a transaction:

```text
Category: food
```

check:

```python
if category in categories:
    ...
```

Then add functionality to create a custom category.

You'll get practice with:

```python
category in categories
```

and understand why sets are useful.

---

# Stage 4 — Tuples

Represent transaction types as an immutable collection:

```python
TRANSACTION_TYPES = (
    "income",
    "expense"
)
```

Then:

```python
if transaction_type not in TRANSACTION_TYPES:
    raise ValueError(...)
```

You can also experiment with immutable transaction records:

```python
transaction = (
    1,
    "expense",
    250,
    "food",
    "Groceries"
)
```

Then compare that approach with dictionaries.

Ask yourself:

> When is a tuple better than a dictionary?

That's part of the learning.

---

# Stage 5 — `is` vs `==`

Create functions that return `None` when something isn't found.

```python
transaction = find_transaction(100)

if transaction is None:
    print("Transaction not found")
```

This gives you a real reason to use:

```python
is None
```

rather than:

```python
== None
```

Then create your own experiments with:

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a
```

and test:

```python
a == b
a is b

a == c
a is c
```

---

# Stage 6 — The mutable default argument trap

Create this deliberately:

```python
def add_transaction(transaction, transactions=[]):
    transactions.append(transaction)
    return transactions
```

Test it.

Figure out why it behaves unexpectedly.

Then fix it:

```python
def add_transaction(transaction, transactions=None):
    if transactions is None:
        transactions = []

    transactions.append(transaction)
    return transactions
```

Don't just memorize the fix.

Understand **why** the original happens.

---

# Stage 7 — Functions with `*args`

Add a transaction filtering system.

You should eventually be able to do something like:

```python
filter_transactions(
    "category",
    "food"
)
```

But also:

```python
filter_transactions(
    "category",
    "food",
    "transport",
    "rent"
)
```

So you can implement:

```python
def filter_transactions(field, *values):
    ...
```

Now:

```python
filter_transactions(
    "category",
    "food",
    "transport"
)
```

means:

> Find transactions whose category is either food or transport.

Remember that `values` becomes a tuple.

---

# Stage 8 — `**kwargs`

Build a more flexible search function:

```python
search_transactions(
    category="food",
    transaction_type="expense"
)
```

or:

```python
search_transactions(
    category="food",
    min_amount=100,
    max_amount=1000
)
```

Implement:

```python
def search_transactions(**filters):
    ...
```

Now `filters` is a dictionary.

This is a very practical use of `**kwargs`.

---

# Stage 9 — Classes

Once the procedural version works, rebuild it using classes.

Create:

```python
class Transaction:
    ...
```

It should contain things like:

```python
transaction.id
transaction.amount
transaction.category
transaction.description
```

Then:

```python
class FinanceTracker:
    ...
```

The tracker manages transactions.

Conceptually:

```text
FinanceTracker
│
├── Transaction
├── Transaction
├── Transaction
└── Transaction
```

---

# Stage 10 — Composition

Give `FinanceTracker` several components.

For example:

```python
class TransactionManager:
    ...


class BudgetManager:
    ...


class ReportGenerator:
    ...
```

Then:

```python
class FinanceTracker:
    def __init__(
        self,
        transaction_manager,
        budget_manager,
        report_generator
    ):
        self.transaction_manager = transaction_manager
        self.budget_manager = budget_manager
        self.report_generator = report_generator
```

That's composition.

Your tracker **has** managers.

---

# Stage 11 — Inheritance

Don't force inheritance into the whole project.

Use it somewhere where it makes sense.

For example:

```python
class Transaction:
    ...


class Income(Transaction):
    ...


class Expense(Transaction):
    ...
```

Both inherit from `Transaction`.

Then give them different behavior.

For example:

```python
income.calculate_effect()
```

could return:

```text
+15000
```

while:

```python
expense.calculate_effect()
```

returns:

```text
-250
```

Now you can see actual polymorphism rather than inheritance existing just because you need to demonstrate it.

---

# Stage 12 — Exceptions

Create custom exceptions:

```python
class FinanceError(Exception):
    pass


class InvalidAmountError(FinanceError):
    pass


class TransactionNotFoundError(FinanceError):
    pass


class InvalidCategoryError(FinanceError):
    pass


class BudgetExceededError(FinanceError):
    pass
```

Now your application has meaningful errors.

For example:

```python
if amount <= 0:
    raise InvalidAmountError(
        "Amount must be greater than zero."
    )
```

---

# Stage 13 — `try / except / else / finally`

Your CLI should handle errors properly.

Something like:

```python
try:
    amount = float(input("Amount: "))

    tracker.add_transaction(
        amount=amount,
        category=category
    )

except InvalidAmountError as e:
    print(f"Invalid amount: {e}")

except InvalidCategoryError as e:
    print(f"Invalid category: {e}")

except ValueError:
    print("Please enter a valid number.")

else:
    print("Transaction added successfully.")

finally:
    print("Returning to menu...")
```

This directly practices the exception structure from your study notes.

---

# Stage 14 — Budget system

Add budgets:

```text
Set budget

Category: food
Monthly budget: 3000
```

Then:

```text
========== BUDGET ==========

food
Budget:    P3,000
Spent:     P2,750
Remaining: P250
```

If spending goes over:

```text
WARNING:
Food budget exceeded by P250.
```

This gives you more opportunities to practice exceptions.

---

# Stage 15 — Reports

Add:

```text
View summary
```

Example:

```text
================================
          MONTHLY REPORT
================================

Income

Salary                 P15,000
Freelance               P3,000
                       -------
Total                   P18,000


Expenses

Rent                    P5,000
Food                    P2,500
Transport               P1,800
Utilities               P1,200
                       -------
Total                   P10,500


Balance                  P7,500
```

Use dictionaries to calculate totals:

```python
{
    "food": 2500,
    "rent": 5000,
    "transport": 1800
}
```

---

# Final project structure

Only once the project becomes large should you split it up:

```text
finance_tracker/
│
├── main.py
│
├── models.py
│
├── tracker.py
│
├── transactions.py
│
├── budgets.py
│
├── reports.py
│
├── exceptions.py
│
└── utils.py
```

Still **100% Python**.

No frameworks.

No packages.

No APIs.

No database.

No web application.

No frontend.

No LLM.

Just Python.

---

# The progression I want you to follow

Don't build the final version immediately.

Build it through these stages:

```text
                    PROJECT
                       │
                       ▼
              ┌─────────────────┐
              │ 1. Basic CLI    │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 2. Lists/dicts  │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 3. Sets/tuples  │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 4. Functions    │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 5. *args/**kwargs│
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 6. Classes      │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 7. Inheritance  │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 8. Composition  │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 9. Exceptions   │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ 10. Refactoring │
              └─────────────────┘
```

The key rule: **don't move to the next stage until you can explain why the Python feature you're using is appropriate.**