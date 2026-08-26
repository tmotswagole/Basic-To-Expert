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

This section defines the data object that carries file metadata through the
engine. The methods are not decoration: they determine how records display,
compare, behave in conditions, and participate in sets or dictionaries.

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

This section focuses on developer-facing diagnostics. A useful representation
should reveal enough stable state to debug a scan or failing test without
pretending that it is the same output intended for an end user.

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

This section separates human-readable presentation from debugging output. The
display should be concise and useful in the CLI, while `repr()` remains more
explicit for logs, collections, and interactive debugging.

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

This section gives the object a meaningful size-related behavior and shows how
Python uses `__len__` for both `len(value)` and, when no `__bool__` exists,
truth testing. Choose a definition that is cheap enough or document its I/O
cost.

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

This section defines value equality independently from object identity. Decide
which fields make two file records represent the same logical file and test
that unrelated metadata changes do or do not affect that decision.

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

This section explores the contract that equal objects must have equal hashes.
It also exposes why mutable fields should not participate in a hash used by a
set or dictionary key: changing them can make an existing entry unreachable.

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

This section makes reference sharing visible inside a snapshot. A shallow copy
duplicates the outer container but reuses nested objects; a deep copy recursively
duplicates them, which is safer for independent experimentation but more costly.

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

This section turns a momentary scan into durable, comparable state. JSON is
intentionally simple and inspectable, so you can focus on serialization rules,
stable paths, timestamps, checksums, and handling incomplete or invalid files.

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

This section adds cross-cutting behavior around operations without putting
timing and logging code inside every function. The decorator must preserve the
wrapped function's calling convention, metadata, return value, and exceptions.

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

This section demonstrates how independent decorators compose around one
operation. Their order matters, so record which wrapper validates, logs, times,
and records history, and verify behavior when the wrapped operation fails.

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

This section explains why wrapper metadata affects debugging, documentation,
introspection, and tooling. The experiment should compare decorated functions
with and without `wraps`, rather than treating it as a line to copy blindly.

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

This section introduces lazy iteration as a memory boundary. A generator does
not hold the complete file in memory; it pauses at `yield` and resumes only
when the consumer requests the next item.

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

This section applies streaming to a real measurement task. Keep only running
counters and the small amount of state needed for longest-line and average-line
calculations, so memory use depends on the measurement rather than file size.

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

This section composes small lazy transformations into a reusable processing
pipeline. Each stage should accept an iterable and yield transformed values,
allowing filtering and normalization to happen only as results are consumed.

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

This section moves streaming from text lines to raw bytes. Fixed-size chunks
make checksum calculation predictable and demonstrate why binary processing
must avoid accidental decoding or whole-file reads.

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

This section gives resource lifetime a clear boundary. A context manager makes
opening, preparation, cleanup, and exception behavior visible at the call site
and protects files from being left open after failure.

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

This section models backup as a controlled operation rather than a bare copy.
The implementation must define when work is committed, how copied data is
verified, and what partial artifacts are removed after an error.

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

This section implements the same lifecycle with a generator-based helper. The
comparison should explain when the class form is clearer, when `contextmanager`
reduces ceremony, and how exceptions cross the `yield` boundary.

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

This section combines the earlier model, set, hashing, and generator work into
a useful change report. Comparison should be deterministic, should not confuse
renames with content changes unless explicitly supported, and should preserve
enough detail for a user to act on the result.

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

This section is a responsibility map, not a requirement to create every file
immediately. Introduce modules when they reduce coupling and make testing or
replacement easier, while keeping the CLI as a thin orchestration layer.

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

Use this table as a revision map after implementation. For every row, point to
one function, class, or test that demonstrates the topic and be able to explain
why that feature belongs at that location.

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

This section is intentionally isolated from the main workflow because custom
allocation is easy to misuse. The experiments should clarify the difference
between creating an object and initializing it, especially for immutable values
and controlled instance reuse.

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

This section describes the integration milestone: the separate exercises must
work together as a reliable command-line tool. Treat the sample session as an
acceptance scenario and verify both successful output and sensible behavior for
invalid paths, unreadable files, and interrupted work.

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

## Definitions and design intent

This project is a **file-processing engine**, not a file browser. Its job is to
turn file-system state into measured, repeatable results. The standard library
provides the required building blocks: `pathlib` for paths, `Path.stat()` for
metadata, `hashlib` for checksums, `json` for snapshots, `shutil` for copying,
and `contextlib` for managed cleanup.

- A **file record** is the in-memory description of one file at a point in
    time.
- A **snapshot** is a serialized record of many files that can be compared
    later.
- A **checksum** is a digest of file contents. It helps detect changes that
    size and modification time alone can miss.
- A **generator** produces values on demand, which limits memory use and makes
    pipelines composable.
- A **context manager** owns setup and cleanup around a block, including cleanup
    when the block raises an exception.
- A **backup transaction** is an operation with a clear success state and a
    cleanup or rollback path when verification fails.

The core separation should be:

1. Scanning discovers paths and metadata.
2. Analysis reads file contents and calculates measurements.
3. Snapshot storage serializes data and restores it later.
4. Comparison classifies paths as new, modified, deleted, or unchanged.
5. The CLI coordinates operations and formats messages; it should not contain
     checksum or comparison algorithms.

## Correctness contracts

Use these as implementation rules and test cases:

- Never follow symlinked directories unless the user explicitly requests it.
- Ignore the snapshot output directory while scanning the source directory, or
    the tool will repeatedly analyze its own output.
- Store paths in a consistent form, preferably relative to the scanned root,
    so the same directory can be compared across machines.
- Open text files with an explicit encoding and an error policy. A binary file
    must not be decoded accidentally just because its extension is unknown.
- A checksum must be calculated from bytes, not from platform-dependent text
    decoding.
- A backup is complete only after the destination file exists and its content
    verifies against the source checksum.
- Writing a snapshot should not leave a misleading file after a failed write. A
    temporary file followed by a rename is a good standard-library approach.

## Recommended checkpoints

### Checkpoint A: inspect and stream

Scan a small fixture directory, build `FileInfo` objects, stream lines, and
produce analysis totals. Include an empty file, a Unicode text file, a binary
file, and a missing path in the fixture set.

### Checkpoint B: persist and compare

Write and load JSON snapshots. Change one file, add one file, and delete one
file, then verify all four comparison categories. Keep comparison output
deterministic by sorting paths before displaying them.

### Checkpoint C: decorators and lifecycle

Add timing, logging, validation, and operation-history decorators. Verify with
`functools.wraps` that decorated functions retain their name and docstring.
Then implement the class-based backup context manager and test both success and
failure cleanup.

### Checkpoint D: safe backup

Back up a directory into a separate destination, verify checksums, and decide
how existing destination files are handled. Test a destination inside the
source, a read failure, a name collision, and a partially completed copy.

## Minimum acceptance checklist

The intermediate version is ready when it can:

- scan recursively without eagerly materializing every path;
- analyze large text files one line at a time;
- calculate a streaming checksum in fixed-size chunks;
- create, load, and compare JSON snapshots;
- classify new, modified, deleted, and unchanged files correctly;
- preserve function metadata through stacked decorators;
- copy and verify files with a clear cleanup policy;
- record successful and failed operations; and
- explain why a shallow copy, text-mode checksum, or unbounded list would be
    incorrect for a particular situation.

## Testing strategy

Use temporary directories created with `tempfile.TemporaryDirectory()` so tests
never modify the user's real files. Keep unit tests for analysis and comparison
separate from integration tests for scanning and backup. Assert both returned
values and side effects: destination files, snapshot contents, history entries,
and cleanup after an exception.

Performance observations should include the machine, file sizes, encoding, and
whether the operation was warm or cold. A generator is not automatically faster
than a list; its primary benefit here is bounded memory use and lazy work.
