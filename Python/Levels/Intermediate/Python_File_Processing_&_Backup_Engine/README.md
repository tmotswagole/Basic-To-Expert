# Project: Python File Processing & Backup Engine

Build a command-line **file processing engine** that can scan directories,
process large files lazily, create backups, compare file snapshots, and safely
manage operations.

You will use **only Python's standard library**.

No:

- FastAPI
- databases
- Redis
- APIs
- third-party packages
- web frameworks
- LLMs

The project should force you to use the intermediate Python features you're
studying.

---

## What the finished program does

You should eventually be able to run:

```text
$ python main.py

========================================
       PYTHON FILE PROCESSOR
========================================

1. Scan directory
2. Analyze files
3. Create snapshot
4. Compare snapshots
5. Backup files
6. Stream file contents
7. View operation history
8. Exit

Choose: 1

Directory: ./documents

Scanning...

12 files found
8.4 MB total
3 Python files
4 text files
5 other files
```

Then:

```text
Choose: 2

File Analysis
----------------------------------------

main.py
  Lines:       243
  Characters:  8,421
  Words:       1,204
  Size:        8.2 KB

notes.txt
  Lines:       1,532
  Characters: 42,921
  Words:       7,230
  Size:        42.0 KB
```

And eventually:

```text
Choose: 3

Snapshot created:
snapshot_2026_08_14.json
```

Then:

```text
Choose: 4

Comparing snapshots...

NEW
  report.py

MODIFIED
  main.py

DELETED
  old_notes.txt

UNCHANGED
  config.txt
  README.md
```

This is a small but realistic systems-style Python project.

---

## 1. Object model

Create a `FileInfo` object.

```text
FileInfo
├── path
├── name
├── extension
├── size
├── modified_time
└── checksum
```

For example:

```python
file = FileInfo("documents/report.txt")
```

You should implement:

```python
repr(file)
str(file)
len(file)
file == another_file
hash(file)
```

This gives you direct practice with:

- `__repr__`
- `__str__`
- `__len__`
- `__eq__`
- `__hash__`

---

## 2. `__repr__`

Make `repr()` useful to developers.

Something like:

```text
FileInfo(path='documents/report.txt', size=42192)
```

Ideally:

```python
repr(file)
```

should contain enough information to understand exactly what object you're
looking at.

Then test:

```python
print(file)
print(repr(file))
```

and make them intentionally different.

---

## 3. `__str__`

Make `str()` user-friendly.

For example:

```text
report.txt — 42.0 KB
```

So:

```python
print(file)
```

produces:

```text
report.txt — 42.0 KB
```

while:

```python
repr(file)
```

produces:

```text
FileInfo(path='documents/report.txt', size=42192)
```

That's the exact distinction your notes describe.

---

## 4. `__len__`

Give `FileInfo` a meaningful length.

For example:

```python
len(file)
```

could return the number of lines in the file.

Then:

```python
if file:
    print("File contains data")
```

can demonstrate how `__len__` can influence truthiness.

---

## 5. `__eq__`

Two `FileInfo` objects representing the same file should compare correctly.

For example:

```python
a = FileInfo("report.txt")
b = FileInfo("report.txt")

print(a == b)
```

should produce:

```text
True
```

even though:

```python
a is b
```

is:

```text
False
```

This gives you a practical way to reinforce **identity vs equality**.

---

## 6. `__hash__`

Make `FileInfo` usable inside a set:

```python
files = {
    file_a,
    file_b,
    file_c
}
```

Or as a dictionary key:

```python
file_sizes = {
    file_a: 1024,
    file_b: 2048
}
```

But this is where you need to think carefully.

If the object's equality depends on mutable attributes, your hash strategy can
become dangerous.

That's part of the exercise.

---

## 7. Shallow vs deep copy

Create a `DirectorySnapshot`.

It contains:

```text
DirectorySnapshot
    │
    ├── FileInfo
    ├── FileInfo
    ├── FileInfo
    └── FileInfo
```

Internally:

```python
snapshot.files
```

might be:

```python
[
    FileInfo(...),
    FileInfo(...),
    FileInfo(...)
]
```

Now experiment with:

```python
import copy

shallow = copy.copy(snapshot)
deep = copy.deepcopy(snapshot)
```

Then modify something nested.

For example:

```python
shallow.files[0].size = 999999
```

Observe what happens to:

```python
snapshot.files[0].size
```

Then do the same with `deep`.

Your goal is to understand **exactly what is being copied**.

---

## 8. Build a snapshot system

Your application should be able to capture:

```text
filename
path
size
modified time
checksum
```

A snapshot might conceptually look like:

```python
{
    "documents/report.txt": {
        "size": 42192,
        "modified": 1723620000,
        "checksum": "abc123..."
    }
}
```

Don't use a database.

Store snapshots in JSON files using Python's standard library.

For example:

```text
snapshots/
    snapshot_001.json
    snapshot_002.json
    snapshot_003.json
```

---

## 9. Decorators

Now add an operation logger.

You want to be able to write:

```python
@timed
def scan_directory(...):
    ...
```

and automatically get:

```text
scan_directory took 0.032s
```

Implement:

```python
def timed(func):
    ...
```

Use:

```python
functools.wraps
```

and:

```python
time.perf_counter()
```

This directly mirrors the material you're studying.

---

## 10. Create several decorators

Don't stop at `@timed`.

Create:

```python
@timed
@logged
@requires_directory
def create_snapshot(...):
    ...
```

Possible decorators:

### `@timed`

Measures execution time.

### `@logged`

Records:

```text
CREATE_SNAPSHOT started
CREATE_SNAPSHOT completed
```

### `@validate_path`

Ensures the supplied path exists.

### `@operation`

Records the operation in your history.

Now you have a reason to understand **decorator stacking**.

---

## 11. Test `functools.wraps`

Create a decorated function:

```python
@timed
def analyze_file(path):
    """Analyze a file."""
    ...
```

Then inspect:

```python
analyze_file.__name__
analyze_file.__doc__
```

Without `functools.wraps`, you'll discover that they can become:

```text
wrapper
```

With `wraps`, they remain:

```text
analyze_file
```

This makes the reason for `functools.wraps` obvious.

---

## 12. Generators

This is where the project gets interesting.

You need to process **large files without loading them entirely into memory**.

Don't do:

```python
contents = file.read()
```

for your streaming functionality.

Instead create:

```python
def stream_lines(path):
    ...
    yield ...
```

Then:

```python
for line in stream_lines("large_file.txt"):
    process(line)
```

---

## 13. Build a large-file analyzer

Your program should support:

```text
Analyze file
```

and calculate:

```text
Lines
Words
Characters
Empty lines
Longest line
Average line length
```

But the function should process the file **one line at a time**.

Conceptually:

```python
def stream_lines(path):
    with open(path, "r") as file:
        for line in file:
            yield line
```

Then your analyzer consumes the generator.

This is the key lesson:

```text
10 GB file
      ↓
stream one line
      ↓
process
      ↓
discard
      ↓
next line
```

rather than:

```text
10 GB file
      ↓
load everything into RAM
```

---

## 14. Generator pipelines

Take it further.

Create:

```python
def stream_lines(path):
    ...


def non_empty_lines(lines):
    ...


def normalize_lines(lines):
    ...


def filter_lines(lines, keyword):
    ...
```

Then chain them:

```python
lines = stream_lines(path)
lines = non_empty_lines(lines)
lines = normalize_lines(lines)
lines = filter_lines(lines, "error")
```

Finally:

```python
for line in lines:
    print(line)
```

You're building a lazy processing pipeline.

Nothing should happen until iteration begins.

---

## 15. Generator challenge

Create a function:

```python
def stream_chunks(path, chunk_size=4096):
    ...
```

It should read a file in chunks:

```text
4096 bytes
4096 bytes
4096 bytes
...
```

without loading the entire file.

Then implement:

```python
def calculate_checksum(path):
    ...
```

using your generator.

This is a very practical use of generators.

---

## 16. Context managers

Now build a custom context manager.

Create:

```python
class FileOperation:
    ...
```

so you can write:

```python
with FileOperation("report.txt") as operation:
    operation.process()
```

The context manager should:

1. open the resource
2. prepare the operation
3. execute the block
4. clean everything up
5. handle errors
6. close resources

Implement:

```python
__enter__
__exit__
```

---

## 17. Build a backup context manager

Create:

```python
with BackupOperation(source, destination):
    ...
```

The operation should:

```text
START
  ↓
create backup directory
  ↓
copy files
  ↓
verify copies
  ↓
COMMIT
```

If something fails:

```text
START
  ↓
copy files
  ↓
ERROR
  ↓
ROLLBACK / CLEANUP
```

This gives you a real reason to understand:

```python
__enter__()
__exit__()
```

---

## 18. Context manager with `contextlib`

After you've implemented the class version, implement the same thing using:

```python
from contextlib import contextmanager
```

For example:

```python
@contextmanager
def operation(...):
    ...
    yield
    ...
```

Then compare:

```text
Class-based context manager
            vs
contextlib.contextmanager
```

You should understand both.

---

## 19. Snapshot comparison

Now make the project actually useful.

Given:

```text
snapshot_001
snapshot_002
```

produce:

```text
================================
       SNAPSHOT DIFFERENCE
================================

NEW FILES

+ report.py
+ backup.txt


MODIFIED FILES

~ main.py
~ config.json


DELETED FILES

- old_notes.txt


UNCHANGED

= README.md
= requirements.txt
```

This requires:

- dictionaries
- sets
- object equality
- hashing
- iteration
- generators

---

## 20. Final architecture

Once you're finished, your Python project could look like:

```text
file_processor/
│
├── main.py
│
├── models.py
│   ├── FileInfo
│   ├── Directory
│   └── Snapshot
│
├── scanner.py
│   ├── scan_directory()
│   └── stream_files()
│
├── analyzer.py
│   ├── analyze_file()
│   ├── stream_lines()
│   └── calculate_checksum()
│
├── snapshots.py
│   ├── create_snapshot()
│   ├── load_snapshot()
│   └── compare_snapshots()
│
├── backup.py
│   └── BackupOperation
│
├── decorators.py
│   ├── timed
│   ├── logged
│   └── validate_path
│
└── exceptions.py
```

Still **nothing but Python**.

---

## What each topic maps to

| Your topic        | Project feature                                         |
| ----------------- | ------------------------------------------------------- |
| `__new__`         | Experiment with immutable/singleton `FileInfo` variants |
| `__init__`        | Object initialization                                   |
| `__repr__`        | Developer representation of files                       |
| `__str__`         | CLI-friendly representation                             |
| `__eq__`          | Comparing snapshots/files                               |
| `__len__`         | File line count                                         |
| `__hash__`        | Sets/dicts of `FileInfo`                                |
| `copy.copy()`     | Snapshot duplication                                    |
| `copy.deepcopy()` | Independent snapshot duplication                        |
| Decorators        | Timing/logging/validation                               |
| `functools.wraps` | Preserve metadata                                       |
| Generators        | Large-file processing                                   |
| Lazy evaluation   | File processing pipelines                               |
| `yield`           | Streaming lines/chunks                                  |
| Context managers  | File/backup operations                                  |
| `__enter__`       | Resource setup                                          |
| `__exit__`        | Cleanup/rollback                                        |
| `contextlib`      | Generator-based context managers                        |

## One important exception: `__new__`

Don't force `__new__` into the main application.

Create a **separate experimental exercise** inside the project:

```text
experiments/
    new_experiment.py
```

Build:

1. an immutable `FileIdentifier`
2. a singleton `ApplicationConfig`

and use them to understand why `__new__` exists.

That's much better than artificially putting `__new__` into your file processor
just to say you've used it.

---

## Your final challenge

When you've completed everything, your program should be able to handle
something like:

```text
$ python main.py

Python File Processor

> scan ./project

Found 1,284 files.

> analyze ./project

Streaming analysis...

Files:        1,284
Total size:   482.4 MB
Python files: 347
Text files:   189

> snapshot ./project

Creating snapshot...
Snapshot created.

> backup ./project ./backups/project_001

Starting backup...
Backup completed in 2.41 seconds.

> compare snapshot_001 snapshot_002

NEW:       23
MODIFIED:  47
DELETED:   4
UNCHANGED: 1210

> stream ./large.log --filter ERROR

ERROR Database connection failed
ERROR Request timeout
ERROR Authentication failed

> history

SCAN       0.31s
ANALYZE    0.82s
SNAPSHOT   0.44s
BACKUP     2.41s
COMPARE    0.02s
STREAM     0.17s

> exit
```

And the important thing is that **you built the machinery yourself using
Python's standard library**.

This project is a much better fit for the intermediate material than another
CRUD-style application because every feature gives you a concrete reason to
learn Python's object model, decorators, generators, copying semantics, and
context managers.
