# Project: PyFlow — High-Performance Async Data Processing Engine

Build a **Python-only, high-throughput document ingestion and processing engine**.

It takes a directory containing potentially millions of files, streams them through an asynchronous pipeline, processes CPU-heavy work in separate processes, maintains an in-memory cache, generates snapshots, tracks metrics, and exposes a small CLI for controlling the engine.

No:

* FastAPI
* Django
* Flask
* Redis
* PostgreSQL
* external APIs
* third-party packages
* Celery
* NumPy
* Pandas
* LLMs

**Python standard library only.**

The point is to make the Python runtime itself the thing you're demonstrating.

---

# 1. What you're building

The finished system looks conceptually like this:

```text
                         ┌────────────────────┐
                         │       CLI          │
                         └─────────┬──────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │      Pipeline Engine     │
                    └────────────┬─────────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                  ▼              ▼              ▼
             File Scanner   Async Scheduler   Cache
                  │              │              │
                  ▼              ▼              │
             Generators      Async Workers      │
                  │              │              │
                  └──────────────┼──────────────┘
                                 ▼
                         CPU Process Pool
                                 │
                     ┌───────────┼───────────┐
                     ▼           ▼           ▼
                   Hash       Parse        Analyze
                     │           │           │
                     └───────────┼───────────┘
                                 ▼
                          Result Aggregator
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
                Snapshot       Metrics      Reports
```

This is essentially a small **data-engineering/runtime framework written from scratch in Python**.

---

# 2. The problem

Imagine you have:

```text
dataset/
    ├── customer_001.txt
    ├── customer_002.txt
    ├── customer_003.txt
    ├── ...
    └── customer_500000.txt
```

The engine needs to:

1. discover files
2. stream them rather than loading everything into memory
3. calculate metadata
4. hash contents
5. parse files
6. perform CPU-heavy analysis
7. maintain a cache
8. avoid duplicate processing
9. process independent files concurrently
10. limit concurrency
11. handle failures
12. retry failed operations
13. track performance
14. generate snapshots
15. compare snapshots
16. shut down cleanly

And it needs to remain responsive while doing all of this.

---

# 3. The architecture

Your eventual project should look roughly like:

```text
pyflow/
│
├── main.py
│
├── core/
│   ├── engine.py
│   ├── pipeline.py
│   ├── scheduler.py
│   ├── registry.py
│   └── events.py
│
├── models/
│   ├── file.py
│   ├── result.py
│   ├── snapshot.py
│   └── config.py
│
├── processing/
│   ├── scanner.py
│   ├── parser.py
│   ├── analyzer.py
│   ├── hashing.py
│   └── workers.py
│
├── concurrency/
│   ├── async_pool.py
│   ├── process_pool.py
│   └── locks.py
│
├── cache/
│   ├── base.py
│   ├── memory.py
│   └── eviction.py
│
├── storage/
│   ├── snapshots.py
│   └── history.py
│
├── decorators/
│   ├── timing.py
│   ├── retry.py
│   └── logging.py
│
├── memory/
│   ├── profiling.py
│   └── weakrefs.py
│
├── exceptions.py
│
└── tests/
    ├── test_models.py
    ├── test_cache.py
    ├── test_pipeline.py
    ├── test_async.py
    ├── test_workers.py
    └── test_snapshots.py
```

Don't start with this structure.

Build it progressively.

---

# 4. Phase 1 — Build the object model

Create a `FileRecord`.

It represents one discovered file.

```text
FileRecord
├── path
├── name
├── extension
├── size
├── modified_at
├── checksum
└── status
```

Implement:

```python
__new__
__init__
__repr__
__str__
__eq__
__hash__
__len__
```

For example:

```text
repr(record)

FileRecord(
    path='data/report.txt',
    size=42091,
    checksum='...'
)
```

while:

```text
str(record)
```

might be:

```text
report.txt — 41.1 KB — processed
```

And:

```python
len(record)
```

could represent the number of lines.

---

# 5. Make `FileRecord` memory efficient

This is where the expert material begins.

Create a second implementation using:

```python
__slots__
```

Compare:

```text
FileRecord
vs
SlimFileRecord
```

Measure:

* object size
* attribute access
* memory usage
* ability to dynamically add attributes

Use:

```python
sys.getsizeof()
```

and potentially:

```python
tracemalloc
```

Your program should have a benchmark command:

```text
> benchmark objects

Regular object:
Memory: ...

__slots__ object:
Memory: ...

Difference:
...
```

Now you have a practical reason to understand `__slots__`.

---

# 6. Explore `__new__`

Don't artificially use `__new__` everywhere.

Create a specialized immutable object:

```text
FileKey
```

It represents:

```text
absolute path + checksum
```

Two identical keys should potentially resolve to the same object.

Use `__new__` to experiment with object allocation/interning.

For example:

```python
a = FileKey(...)
b = FileKey(...)

a is b
```

You can investigate when identity can be deliberately controlled.

This demonstrates that you understand **why `__new__` exists**, rather than simply knowing that it exists.

---

# 7. File discovery must be lazy

Your scanner should **never** build a list of millions of files.

Don't do:

```python
files = list(Path(directory).rglob("*"))
```

Instead create:

```python
def stream_files(directory):
    ...
    yield FileRecord(...)
```

Then:

```python
for file in stream_files(directory):
    process(file)
```

The engine can therefore process:

```text
10 files
10,000 files
10 million files
```

without creating a giant list of `FileRecord` objects.

---

# 8. Build generator pipelines

Create:

```python
stream_files()
filter_files()
deduplicate_files()
batch_files()
```

Then:

```text
stream_files
      │
      ▼
filter_files
      │
      ▼
deduplicate_files
      │
      ▼
batch_files
      │
      ▼
processor
```

For example:

```python
files = stream_files("./dataset")

files = filter_files(
    files,
    extensions={".txt", ".log", ".json"}
)

files = deduplicate_files(files)

for batch in batch_files(files, 100):
    ...
```

Nothing should be evaluated until iteration occurs.

This tests whether you genuinely understand **lazy evaluation**.

---

# 9. Deep and shallow copying

Create a `PipelineState`.

It contains nested mutable structures:

```text
PipelineState
│
├── configuration
│   └── dictionaries
│
├── statistics
│   └── dictionaries
│
├── active_files
│   └── list
│
└── results
    └── dictionaries/lists
```

Then support:

```python
state.clone()
```

with both:

```python
copy.copy()
```

and:

```python
copy.deepcopy()
```

Create tests showing exactly which objects are shared.

Then answer:

> Why would a shallow copy be dangerous here?

That should become part of your documentation.

---

# 10. Create a plugin system with `Protocol`

This is one of the most important expert-level pieces.

Your pipeline shouldn't care how a file is processed.

Define a protocol:

```python
class Processor(Protocol):
    def process(self, record: FileRecord) -> ProcessingResult:
        ...
```

Then implement:

```text
TextProcessor
JsonProcessor
LogProcessor
BinaryProcessor
```

None of them need to inherit from `Processor`.

If they satisfy the interface, they're valid processors.

That's **structural typing**.

---

# 11. Generic cache

Build:

```python
class Cache(Generic[T]):
    ...
```

Your engine might have:

```python
Cache[str, ProcessingResult]
```

conceptually:

```text
FileKey
   ↓
ProcessingResult
```

Implement:

```python
get()
set()
delete()
contains()
clear()
```

Then add:

```text
LRU eviction
TTL expiration
maximum size
statistics
```

For example:

```text
Cache statistics
----------------

Hits:        91,203
Misses:       8,442
Hit rate:      91.5%
Evictions:    2,193
Entries:      10,000
```

---

# 12. Understand the memory leak distinction

Now deliberately create two scenarios.

### Growing cache

```text
request
  ↓
cache.set(unique_key, result)
  ↓
cache never removes anything
```

Memory continually grows.

### Reference cycle

Create objects that reference each other:

```text
A → B
↑   ↓
└───┘
```

Then investigate:

```python
gc
weakref
```

Your project should include a small:

```text
> memory-demo
```

command showing both cases.

The point is to be able to explain:

> A growing cache isn't necessarily a garbage collector problem.

---

# 13. Weak references

Use:

```python
weakref
```

for objects that shouldn't keep resources alive.

For example, create an object registry:

```text
FileRecord registry
```

where the registry should not necessarily own every `FileRecord`.

Then investigate what happens when the only strong reference disappears.

This is excellent interview material.

---

# 14. Async architecture

Now introduce `asyncio`.

The engine should have an asynchronous scheduler.

Conceptually:

```text
                Scheduler
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Worker 1     Worker 2     Worker 3
       │            │            │
       ▼            ▼            ▼
    File A        File B        File C
```

Create:

```python
async def process_files(files):
    ...
```

---

# 15. `asyncio.gather()`

Create independent asynchronous operations.

For example:

```python
async def inspect_file(record):
    ...
```

Then:

```python
results = await asyncio.gather(
    inspect_file(a),
    inspect_file(b),
    inspect_file(c),
)
```

Demonstrate that the results are returned in the order of the supplied awaitables.

---

# 16. `asyncio.create_task()`

Create background jobs:

```python
task = asyncio.create_task(
    process_file(record)
)
```

Then allow the scheduler to continue doing other work.

This gives you a reason to understand the distinction:

```text
await coroutine
```

versus:

```text
create_task(coroutine)
```

---

# 17. Async backpressure

This is where the project becomes much more serious.

Suppose the scanner finds:

```text
1,000,000 files
```

You cannot create:

```python
1_000_000 asyncio.Task objects
```

just because you can.

Build a bounded queue:

```python
asyncio.Queue(maxsize=1000)
```

Architecture:

```text
Scanner
   │
   ▼
┌─────────────┐
│ Async Queue │
│ max = 1000  │
└──────┬──────┘
       │
 ┌─────┼─────┐
 ▼     ▼     ▼
 W1    W2    W3
```

When workers fall behind, the producer must slow down.

That's **backpressure**.

This is much more valuable than simply demonstrating `asyncio.gather()`.

---

# 18. Async locks

Create shared metrics:

```text
processed
failed
cached
retried
bytes_processed
```

Multiple coroutines update these values.

Protect them with:

```python
asyncio.Lock()
```

For example:

```python
async with metrics_lock:
    metrics.processed += 1
```

Then explain why this lock protects coroutines sharing one event loop but does **not** protect multiple processes.

---

# 19. Deliberately introduce the blocking bug

Create:

```python
async def bad_worker():
    time.sleep(5)
```

Run it alongside another coroutine.

Observe:

```text
Worker A starts
Worker B starts

A blocks...

B stops completely
```

Then replace it appropriately.

This is one of the most important things to understand for real async Python.

---

# 20. Async vs threading

Create a processor that uses a deliberately blocking standard-library operation.

Run it using:

```python
asyncio.to_thread()
```

or an executor.

Compare:

```text
asyncio
threading
```

and explain why threading can help when a library has no asynchronous interface.

---

# 21. CPU-bound processing

Now introduce a CPU-heavy operation.

For example:

```text
Calculate SHA-256
Parse a large document
Perform statistical analysis
Find word frequencies
Calculate prime numbers
Compress data
```

Create:

```python
def cpu_heavy_analysis(data):
    ...
```

Then run it using:

```python
concurrent.futures.ProcessPoolExecutor
```

Architecture:

```text
Async Event Loop
       │
       │
       ▼
ProcessPoolExecutor
       │
 ┌─────┼─────┐
 ▼     ▼     ▼
P1    P2    P3
```

Now your system has:

```text
asyncio
    +
multiprocessing
```

for different workloads.

---

# 22. Demonstrate the GIL

Build a benchmark:

```text
> benchmark cpu
```

Run:

```text
1. synchronous
2. threads
3. processes
```

For a CPU-bound operation.

You should produce something like:

```text
CPU Benchmark
--------------------------------

Synchronous:     8.21s
Threads:         8.03s
Processes:       2.71s
```

The exact numbers will depend on the machine.

The important thing is understanding **why** the results differ.

Then create an I/O-bound benchmark:

```text
> benchmark io
```

Compare the concurrency models there.

---

# 23. Decorator system

Create decorators:

```python
@timed
@logged
@retry
@counted
```

For example:

```python
@timed
@retry(max_attempts=3)
async def process_file(...):
    ...
```

Your decorators must work correctly with:

* normal functions
* async functions
* `*args`
* `**kwargs`

And must preserve metadata with:

```python
functools.wraps
```

This is a good test of whether you actually understand decorators rather than just their syntax.

---

# 24. Async-aware retry decorator

Build:

```python
@async_retry(
    attempts=3,
    delay=0.5
)
async def operation():
    ...
```

The decorator should:

1. execute the coroutine
2. catch specific failures
3. wait asynchronously
4. retry
5. eventually raise the original failure

Critically, it must use:

```python
await asyncio.sleep(...)
```

not:

```python
time.sleep(...)
```

Otherwise you've just blocked your event loop.

---

# 25. Context-managed pipeline

Create:

```python
with PipelineSession(config) as session:
    session.process(...)
```

Then make it asynchronous:

```python
async with AsyncPipelineSession(config) as session:
    await session.process(...)
```

Implement:

```python
__enter__
__exit__
```

and:

```python
__aenter__
__aexit__
```

Now you're demonstrating both synchronous and asynchronous resource management.

---

# 26. Graceful shutdown

This is essential.

If the user presses:

```text
Ctrl+C
```

the application should:

```text
STOP ACCEPTING NEW WORK
        ↓
FINISH CURRENT WORK
        ↓
CANCEL PENDING TASKS
        ↓
WAIT FOR PROCESS WORKERS
        ↓
FLUSH METRICS
        ↓
SAVE SNAPSHOT
        ↓
CLOSE RESOURCES
        ↓
EXIT
```

This forces you to understand:

* cancellation
* `asyncio.Task`
* cleanup
* context managers
* exceptions
* event loop shutdown

---

# 27. Snapshot engine

Combine your previous project.

Every processing run creates:

```text
snapshots/
    run_001.json
    run_002.json
    run_003.json
```

Each contains:

```text
path
size
mtime
checksum
processing status
processing duration
```

Then compare:

```text
> diff run_001 run_002
```

Output:

```text
NEW
----
23 files

MODIFIED
--------
41 files

DELETED
-------
7 files

UNCHANGED
---------
9,812 files
```

Use sets and hashing heavily here.

---

# 28. Memory profiler

Add:

```text
> memory
```

Display:

```text
Object statistics
----------------------------

FileRecord objects:       18,203
ProcessingResult objects: 18,203
Cache entries:             9,821

Current memory:            42.3 MB
Peak memory:               61.7 MB

Garbage collections:
Generation 0:  41
Generation 1:   7
Generation 2:   1
```

Use the standard library:

```python
gc
sys
tracemalloc
weakref
```

This makes your memory-model knowledge visible.

---

# 29. Type the entire system

Use:

```python
Protocol
TypeVar
Generic
TypeAlias
TypedDict
dataclass
```

where appropriate.

For example:

```python
class Processor(Protocol):
    def process(
        self,
        record: FileRecord
    ) -> ProcessingResult:
        ...
```

And:

```python
T = TypeVar("T")

class Cache(Generic[T]):
    ...
```

Your pipeline shouldn't know whether it's receiving:

```text
TextProcessor
JsonProcessor
LogProcessor
CustomProcessor
```

as long as it satisfies the protocol.

---

# 30. Add a plugin registry

Build:

```python
ProcessorRegistry
```

with:

```python
registry.register(".txt", TextProcessor())
registry.register(".json", JsonProcessor())
registry.register(".log", LogProcessor())
```

Then:

```python
processor = registry.get(".json")
```

This combines:

* dictionaries
* classes
* protocols
* generics
* exceptions
* object identity
* composition

---

# 31. Build an event system

Create events such as:

```text
FileDiscovered
ProcessingStarted
ProcessingCompleted
ProcessingFailed
CacheHit
CacheMiss
SnapshotCreated
PipelineShutdown
```

Then implement listeners:

```python
metrics.handle(event)
logger.handle(event)
snapshotter.handle(event)
```

Use a `Protocol`:

```python
class EventHandler(Protocol):
    def handle(self, event: Event) -> None:
        ...
```

Now you're building an actual extensible architecture.

---

# 32. Final system

Your finished project should look like:

```text
                         PyFlow
                           │
             ┌─────────────┴─────────────┐
             │                           │
          CLI/API*                    Engine
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
                      Scanner         Scheduler         Cache
                         │               │               │
                     Generator       asyncio           Generic
                         │               │               │
                         │         ┌─────┴─────┐         │
                         │         │           │         │
                         │      Async I/O    Process     │
                         │                    Pool       │
                         │                       │       │
                         └───────────────────────┘       │
                                                         │
                              ┌──────────────────────────┘
                              │
                         Results
                              │
                 ┌────────────┼────────────┐
                 │            │            │
              Snapshot      Metrics      Events
```

`*` Don't actually add an API. Keep the interface as a CLI. The architecture can be API-ready without building one.

---

# What this project demonstrates

| Python knowledge      | Where PyFlow demonstrates it             |
| --------------------- | ---------------------------------------- |
| Lists                 | pipeline collections                     |
| Dicts                 | registries/cache/indexes                 |
| Sets                  | deduplication/snapshot comparison        |
| Tuples                | immutable records                        |
| Mutability            | pipeline state                           |
| `is` vs `==`          | sentinels/object identity                |
| `*args`               | generic decorators/tools                 |
| `**kwargs`            | configurable operations                  |
| Classes               | entire domain model                      |
| Inheritance           | specialized processors where appropriate |
| Composition           | engine architecture                      |
| Exceptions            | failure model                            |
| `__new__`             | immutable/interned objects               |
| `__init__`            | object initialization                    |
| `__repr__`            | debugging                                |
| `__str__`             | CLI output                               |
| `__eq__`              | record comparison                        |
| `__len__`             | file/object semantics                    |
| `__hash__`            | deduplication                            |
| `__slots__`           | memory optimization                      |
| `copy`                | pipeline state                           |
| `deepcopy`            | independent snapshots                    |
| Decorators            | timing/retry/logging                     |
| `functools.wraps`     | decorator metadata                       |
| Generators            | file discovery/streaming                 |
| Lazy evaluation       | processing pipeline                      |
| Context managers      | resource lifecycle                       |
| `contextlib`          | generator context managers               |
| `Protocol`            | processor abstraction                    |
| `Generic`             | cache                                    |
| `TypeVar`             | reusable components                      |
| `weakref`             | non-owning registries                    |
| `gc`                  | memory investigation                     |
| `tracemalloc`         | memory profiling                         |
| `asyncio`             | I/O concurrency                          |
| `gather()`            | concurrent operations                    |
| `create_task()`       | background tasks                         |
| `asyncio.Lock`        | shared async state                       |
| `asyncio.Queue`       | backpressure                             |
| `ProcessPoolExecutor` | CPU parallelism                          |
| threading             | blocking I/O                             |
| GIL                   | benchmark/analysis                       |
| Event loop            | core architecture                        |
| graceful shutdown     | production lifecycle                     |

---

# The part that makes it genuinely expert-level

Don't just make the application work.

Build **experiments into the project** that prove you understand Python.

For example:

```text
> benchmark concurrency
```

```text
I/O workload
-------------------------
Sequential:       10.2s
asyncio:           2.1s
threads:           2.4s
processes:         3.8s


CPU workload
-------------------------
Sequential:        8.7s
threads:           8.4s
processes:         2.9s
```

Then:

```text
> benchmark memory
```

```text
1,000,000 objects

normal class:      96 MB
__slots__:         48 MB

difference:        50%
```

And:

```text
> benchmark generators
```

Compare:

```text
list-based processing
vs
generator-based processing
```

Then:

```text
> benchmark copy
```

Compare:

```text
shallow copy
deep copy
```

This turns the project into both an application **and a Python runtime laboratory**.

---

# The interview questions this project prepares you for

By the end, you should be able to answer these from experience rather than memorization:

### Object model

> What actually happens when you instantiate a Python object?

> When would you override `__new__`?

> Why does overriding `__eq__` affect hashing?

> Why would `__slots__` reduce memory?

### Memory

> How does CPython manage memory?

> What does reference counting do?

> What happens with reference cycles?

> How is a memory leak different from an unbounded cache?

> When would you use `weakref`?

### Async

> What exactly happens at `await`?

> Why doesn't `asyncio` give you parallelism?

> Why does `time.sleep()` break an async application?

> When would you use threads?

> When would you use processes?

> What is the GIL?

### Generators

> Why use a generator instead of a list?

> What does `yield` actually do?

> Why can generators process datasets larger than memory?

### Architecture

> Why use `Protocol` instead of inheritance?

> How would you replace one processor implementation without changing the pipeline?

> Where should shared state live?

> How would you prevent unbounded task creation?

### Concurrency

> Why use an `asyncio.Queue`?

> What is backpressure?

> What does `asyncio.Lock` protect?

> Does an asyncio lock protect multiple processes?

> What happens if one coroutine performs blocking CPU work?

If you can **build PyFlow, profile it, deliberately break it, fix it, benchmark the alternatives, and explain the results**, you're no longer just demonstrating that you know Python syntax.

You're demonstrating that you understand **Python as a runtime and as a systems programming environment**.
