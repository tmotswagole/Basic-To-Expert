# Project: Python Personal Finance Tracker CLI

You are building a command-line application that lets a user manage income,
expenses, budgets, and transactions.

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

- `list`
- `dict`
- `set`
- `tuple`
- mutable vs immutable objects
- `is` vs `==`
- functions
- `*args`
- `**kwargs`
- classes
- objects
- inheritance
- composition
- exceptions
- custom exceptions
- `try`
- `except`
- `else`
- `finally`

And because it's Python-only, you can focus entirely on the language.

---

## Stage 1 — Transactions

This stage establishes the smallest useful version of the application: a user
can create, inspect, and remove financial records. The goal is to make the
program's data flow visible before adding abstractions, persistence, or
advanced validation.

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

## Stage 2 — Lists and dictionaries

This stage explains why a list is useful for preserving a collection of
transactions and why a dictionary is useful for naming each field. You will
also define predictable return values and learn how mutation changes shared
state.

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

## Stage 3 — Sets

This stage uses a set for membership and uniqueness rather than storing another
list of repeated category names. The important result is understanding that a
set represents the domain of allowed categories, while each transaction stores
the category it selected.

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

## Stage 4 — Tuples

This stage contrasts a fixed, immutable sequence with a named, mutable mapping.
You will decide where immutability communicates a rule, such as a transaction
type that should not be changed accidentally after validation.

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

## Stage 5 — `is` vs `==`

This stage separates value comparison from object identity using a real
not-found result. You will learn why `is None` is the correct sentinel check and
why identity should not be used as a general substitute for equality.

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

## Stage 6 — The mutable default argument trap

This stage demonstrates that default argument expressions are evaluated once
when a function is defined, not once per call. The deliberate bug and its fix
should leave you able to explain object lifetime and shared mutable state.

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

## Stage 7 — Functions with `*args`

This stage makes one filtering function accept a variable number of permitted
values without changing its signature. It demonstrates that `*args` is a tuple
of positional values and that the function still needs to validate the field
and define what no values means.

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

## Stage 8 — `**kwargs`

This stage turns named search criteria into a dictionary so callers can combine
filters without a long list of optional parameters. Define supported filter
names, comparison behavior, and whether multiple filters are combined with
logical AND or OR.

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

## Stage 9 — Classes

This stage moves from loose dictionaries to objects with a defined state and
behavior. The purpose is not to use classes everywhere, but to make invalid
transactions harder to create and to give the tracker a clear owner for its
collection.

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

## Stage 10 — Composition

This stage divides the application into cooperating objects that each have one
responsibility. Composition means the tracker has managers; it does not mean
the managers need to inherit from one another.

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

## Stage 11 — Inheritance

This stage introduces inheritance only where income and expense are specialized
forms of a shared transaction concept. The learning target is polymorphism:
the tracker can ask either object for its financial effect without inspecting
its concrete class.

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

Now you can see actual polymorphism rather than inheritance existing just
because you need to demonstrate it.

---

## Stage 12 — Exceptions

This stage gives invalid domain states names that the rest of the application
can handle deliberately. Custom exceptions communicate whether the problem is
with an amount, category, budget, or requested transaction rather than forcing
the CLI to interpret generic error text.

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

## Stage 13 — `try / except / else / finally`

This stage places error handling at the user-input boundary while keeping the
domain methods reusable. `except` handles known failures, `else` runs only
after success, and `finally` performs work that must happen on every path.

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

## Stage 14 — Budget system

This stage introduces a second financial rule: expenses can be evaluated
against a category limit. It connects stored transactions to derived values
such as spent, remaining, and exceeded, so the budget report must always be
calculated from one consistent source of truth.

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

## Stage 15 — Reports

This stage turns raw records into information a person can act on. Grouping
amounts by type and category gives practice with dictionary accumulation,
sorting, formatting, and checking that totals reconcile with the balance.

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

## Final project structure

Use this structure only after the behavior is understood in one or two files.
Each module should have a reason to exist, a small public interface, and tests
that do not need to run the interactive menu.

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

## What the project is teaching

This is a deliberately small **in-memory CLI**. A CLI, or command-line
interface, is a program that receives input and displays output in a terminal
instead of a browser. "In-memory" means that the first version stores data in
Python objects while the program is running; closing the program may discard
the data. That limitation keeps attention on Python fundamentals rather than
file formats or databases.

The important design question is not only whether an operation works, but also
which object should own it:

- A transaction owns transaction data and transaction-specific behavior.
- A manager owns a collection and operations such as add, find, and delete.
- A report generator reads data and calculates totals without changing it.
- The CLI translates user input into function or method calls and formats the
  result for a person to read.

Keeping those responsibilities separate makes the later class-based version a
refactoring of the procedural version, not a completely different project.

## Domain rules

Write these rules down before implementing the menu. They are the contract that
your functions must enforce:

1. Every transaction has a unique positive integer ID.
2. Amounts are positive numbers. The transaction type determines whether the
    amount increases income or increases expenses.
3. The type must be `income` or `expense`.
4. Categories are normalized consistently, for example by trimming whitespace
    and converting it to lowercase.
5. Deleting or looking up a missing ID raises a meaningful error or returns
    `None`, depending on the function's documented contract.
6. A budget belongs to one category and cannot be negative.
7. A summary must satisfy `balance = total income - total expenses`.

Decide whether money is represented as `float` or `Decimal`. `float` is easier
for the first exercise, but `Decimal` is safer for real currency because many
decimal fractions cannot be represented exactly in binary floating point. The
choice and its trade-off should be documented in your implementation.

## Suggested implementation checkpoints

Do not move forward only because the menu displays. At each checkpoint, be
able to explain the data structure and prove the behavior with a small test or
manual example.

### Checkpoint A: procedural core

Implement adding, listing, finding, and deleting transactions with a list of
dictionaries. Test an empty list, a single transaction, duplicate-looking
transactions with different IDs, and deletion of a missing ID.

### Checkpoint B: validation and queries

Add set-based category validation, tuple-based type validation, `*args`
category filtering, and `**kwargs` search. Test boundary values such as zero,
negative amounts, unknown fields, no filters, and several matching categories.

### Checkpoint C: object-oriented model

Convert one concept at a time to classes. A `Transaction` should validate its
own state; a `FinanceTracker` should coordinate collections; and reports should
be derived from stored transactions rather than duplicated state.

### Checkpoint D: budgets and reports

Set and retrieve budgets, calculate spending by category, and display the
remaining amount. Test a budget with no spending, spending exactly equal to the
budget, and spending above the budget. Make the over-budget policy explicit:
reject the transaction, allow it with a warning, or raise an exception that
the CLI catches.

### Checkpoint E: errors and user interaction

The CLI should never crash because a user typed text where a number was
expected. Convert input at the boundary, catch only errors that can be handled,
and keep the domain layer independent from `input()` and `print()`.

## Minimum acceptance checklist

The finished beginner version should be able to:

- add income and expense transactions;
- list transactions in a stable, readable order;
- find, search, and delete by ID;
- reject invalid amounts, types, and categories;
- create custom categories without duplicates;
- set and display category budgets;
- calculate income, expenses, balance, and category totals;
- return to the menu after handled errors; and
- explain why each list, dictionary, set, tuple, class, and exception exists.

## Useful experiments

Keep small experiments beside the project in ordinary Python files. Compare
`a == b` with `a is b`, call the mutable-default example twice, and inspect the
type of `values` inside a `*args` function and `filters` inside a `**kwargs`
function. Each experiment should record an observation and a conclusion, not
just print a result.

Once the core behavior works, add tests for the tracker and managers. The most
valuable tests are small: one rule, one input, one expected result. That makes
it obvious whether a failure comes from validation, calculation, or formatting.

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

## The progression I want you to follow

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

The key rule: **don't move to the next stage until you can explain why the
Python feature you're using is appropriate.**
