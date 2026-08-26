# Project: PyFlow — High-Performance Async Data Processing Engine

Build a **Python-only, high-throughput document ingestion and processing
engine**.

It takes a directory containing potentially millions of files, streams them
through an asynchronous pipeline, processes CPU-heavy work in separate
processes, maintains an in-memory cache, generates snapshots, tracks metrics,
and exposes a small CLI for controlling the engine.

## Definitions and architecture boundaries

PyFlow is an educational **bounded ingestion system**. It accepts a lazy stream
of file records, schedules independent work, applies the right processor, and
publishes results without allowing input volume to dictate memory usage. The
point is not to claim that every workload should be asynchronous. The point is
to make each concurrency choice explicit and measurable.

- **Throughput** is the amount of work completed per unit of time.
- **Latency** is the time from accepting one file to producing its result.
- **Backpressure** is the mechanism that slows producers when consumers cannot
    keep up. In PyFlow, the bounded `asyncio.Queue` is the control point.
- **Concurrency** means multiple operations are in progress; **parallelism**
    means work is executing at the same time on multiple CPU cores.
- **I/O-bound work** spends time waiting for files or other external resources.
- **CPU-bound work** spends time executing instructions and may require
    processes to obtain parallel execution in CPython.
- **Idempotency** means retrying an operation does not create duplicate or
    corrupt results.
- **Observability** means exposing enough metrics, logs, and events to explain
    what the engine is doing and why it is slow or failing.

Keep the ownership boundaries clear:

1. The scanner discovers records and never owns the full input collection.
2. The scheduler controls queue capacity, worker count, cancellation, and
     shutdown.
3. Process workers perform picklable CPU functions and return data, not live
     event-loop objects or open file handles.
4. The cache owns reuse and eviction policy; it must not silently become an
     unlimited data store.
5. The aggregator owns result classification and snapshot output.
6. Metrics and event handlers observe operations without changing their
     correctness.

## Non-negotiable concurrency contracts

Document and test these rules as part of the project:

- Do not create one task per discovered file. The queue and fixed worker pool
    must bound pending work.
- Every produced queue item must eventually receive `task_done()`, including
    failure paths, so shutdown cannot wait forever.
- Cancellation must close or await resources. A cancelled task is not proof that
    the underlying thread or process operation stopped immediately.
- `asyncio.Lock` protects coroutines in one event loop. It does not coordinate
    separate processes; use process-safe primitives or aggregate results in one
    owner process instead.
- Never call blocking `time.sleep()`, large synchronous CPU functions, or
    blocking file operations directly on the event loop when responsiveness
    matters. Move suitable work to `asyncio.to_thread()` or a process pool.
- Process-pool functions must be importable and serializable, especially on
    platforms that use the `spawn` start method. Protect CLI startup with the
    normal `if __name__ == "__main__":` guard.
- Retries must target transient failures, use asynchronous delays in async code,
    and stop after a documented limit. Retrying validation errors wastes work.

## Result and failure model

Represent success and failure as structured results rather than relying only on
log text. A result should identify the path, processor, status, duration,
bytes processed, cache state, and an error type or message when applicable.
Separate these categories:

- **Permanent failure:** invalid input, unsupported format, or permission that
    will not change during this run.
- **Transient failure:** a short-lived resource or operating-system problem
    that may succeed on retry.
- **Cancellation:** work intentionally stopped during shutdown; it should not
    be reported as an ordinary processing error.

This distinction makes metrics meaningful and prevents a graceful shutdown from
looking like a wave of failed files.

## Performance methodology

Every benchmark should state its workload, input size, worker count, process
count, warm-up policy, and number of repetitions. Compare like with like and
report more than one number when possible: elapsed time, files per second, peak
memory, and failure count.

Interpret results carefully:

- Threads may improve I/O-bound work because waiting releases execution time,
    but they generally do not make pure Python CPU work run in parallel under the
    GIL.
- Processes can parallelize CPU work but add startup, serialization, and
    inter-process communication costs.
- Asyncio improves coordination of waiting tasks; it does not make blocking
    code non-blocking by itself.
- A cache can increase throughput while increasing memory use. Track hit rate,
    eviction count, entry age, and size together.
- `sys.getsizeof()` measures only an object's shallow footprint. Use
    `tracemalloc` or a deliberately documented measurement method for aggregate
    memory conclusions.

## Expert checkpoints

### Checkpoint A: bounded synchronous core

Build the scanner, records, processors, cache, snapshots, and deterministic
result aggregation without asyncio. This gives every later benchmark a correct
baseline.

### Checkpoint B: async scheduler

Add a bounded queue, a fixed number of workers, metrics protected by an async
lock, and cancellation tests. Demonstrate that a slow consumer causes producer
backpressure instead of unbounded task creation.

### Checkpoint C: mixed concurrency

Move blocking I/O to threads and CPU-heavy functions to a process pool. Measure
serialization overhead and ensure the event loop remains responsive while work
is running elsewhere.

### Checkpoint D: production-shaped lifecycle

Add retries, events, structured failures, snapshots, context-managed sessions,
and graceful shutdown. Exercise success, permanent failure, transient failure,
cache hit, cancellation, and process-worker failure.

## Minimum acceptance checklist

PyFlow is ready for the expert challenge when it can:

- ingest a lazy stream without retaining all records;
- apply processors through a `Protocol`-based registry;
- use a typed cache with bounded eviction and useful statistics;
- maintain a bounded async queue and fixed worker pool;
- distinguish coroutine concurrency from process parallelism;
- offload blocking I/O and CPU-bound work to appropriate executors;
- retry only eligible failures and preserve the final cause;
- shut down without stranded tasks, queue joins, or process workers;
- generate comparable snapshots and structured run metrics; and
- support benchmarks that explain trade-offs rather than merely printing faster
    numbers.

## Testing and observability expectations

Test pure models and cache policy synchronously, then use small deterministic
fixtures for scheduler tests. Include tests for queue saturation, duplicate
records, cancellation, retry timing, process-pool result ordering, cache
eviction, and snapshot consistency. Avoid making tests depend on exact timing;
assert ordering, counts, state transitions, and bounded behavior instead.

Expose a run identifier so logs, events, metrics, and snapshots can be joined.
At minimum record discovered, queued, started, completed, cached, retried,
failed, cancelled, and bytes-processed counts. A system that is fast but cannot
explain missing work is not complete.
No:

- FastAPI
- Django
- Flask
- Redis
- PostgreSQL
- external APIs
- third-party packages
- Celery
- NumPy
- Pandas
- LLMs

**Python standard library only.**

The point is to make the Python runtime itself the thing you're demonstrating.

---

## 1. What you're building

This section defines PyFlow as a complete ingestion system rather than a
collection of isolated Python demonstrations. The finished engine should make
file discovery, scheduling, processing, reuse, measurement, and shutdown work
together under a single CLI-controlled lifecycle.

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

This is essentially a small **data-engineering/runtime framework written from
scratch in Python**.

---

## 2. The problem

This section explains the scale and pressure the design must handle. Millions
of files expose the cost of eager lists, unbounded tasks, repeated processing,
and unclear failure handling, so each later feature answers one of those
constraints.

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

## 3. The architecture

This section assigns responsibilities to modules and runtime components. Treat
the diagram as a dependency guide: data should flow from discovery toward
results, while control signals such as cancellation, limits, and metrics flow
back through the engine.

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

## 4. Phase 1 — Build the object model

This phase establishes the immutable identity and observable state of one file
before concurrency makes debugging harder. The model should be useful in
collections, logs, snapshots, and tests without owning the whole pipeline.

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

## 5. Make `FileRecord` memory efficient

This phase measures object representation instead of assuming that `__slots__`
is automatically better. Compare realistic collections, because the instance
size alone may omit referenced values and does not describe total application
memory.

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

- object size
- attribute access
- memory usage
- ability to dynamically add attributes

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

## 6. Explore `__new__`

This phase isolates allocation control from ordinary initialization. Use it to
understand immutable construction and interning, while documenting why identity
reuse can save work in one case and create surprising shared state in another.

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

This demonstrates that you understand **why `__new__` exists**, rather than
simply knowing that it exists.

---

## 7. File discovery must be lazy

This phase makes input volume independent from the number of objects retained
at once. The scanner should yield records as they are found and define explicit
policies for symlinks, inaccessible paths, ignored directories, and ordering.

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

## 8. Build generator pipelines

This phase composes discovery, filtering, deduplication, and batching without
breaking laziness. Each stage should have one responsibility and a clear memory
bound so a later stage cannot accidentally force the entire input into a list.

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

## 9. Deep and shallow copying

This phase investigates which parts of mutable pipeline state are shared after a
copy. The result should guide snapshotting, retries, and worker isolation rather
than treating `deepcopy()` as a universal solution.

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

## 10. Create a plugin system with `Protocol`

This phase introduces structural typing as an extension boundary. The pipeline
depends on the behavior a processor provides, not on a common inheritance tree,
which lets new formats be added without editing the scheduler.

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

## 11. Generic cache

This phase builds reuse into the engine with explicit key, value, capacity, and
expiration semantics. Cache correctness includes distinguishing a miss from a
cached falsey value and ensuring eviction cannot return stale or incorrect data.

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

## 12. Understand the memory leak distinction

This phase separates memory retained by application policy from memory retained
by object references. The experiments should show that an unbounded cache, a
reference cycle, and a temporary allocation have different causes and remedies.

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

## 13. Weak references

This phase models non-owning registries and lifecycle-sensitive metadata. A weak
reference can observe an object without keeping it alive, but it must be treated
as optional because the target may disappear between checks.

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

## 14. Async architecture

This phase adds cooperative concurrency for operations that spend time waiting.
The scheduler should define worker count, ownership of the event loop, result
collection, and how exceptions move from a worker to the controlling command.

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

## 15. `asyncio.gather()`

This phase demonstrates coordinated waiting for a known group of operations.
Test result ordering, exception behavior, and cancellation so you understand
what `gather()` guarantees beyond simply running functions concurrently.

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

Demonstrate that the results are returned in the order of the supplied
awaitables.

---

## 16. `asyncio.create_task()`

This phase distinguishes scheduling background work from immediately awaiting a
coroutine. Every created task needs an owner, a completion path, and exception
handling; otherwise it can outlive the operation that created it.

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

## 17. Async backpressure

This phase protects the engine from a fast scanner overwhelming slower workers.
A bounded queue makes pressure observable and forces the producer to wait,
which keeps pending work and memory within a deliberate limit.

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

## 18. Async locks

This phase makes shared in-process metrics consistent when multiple coroutines
update them. It also clarifies the boundary of an asyncio lock: it coordinates
tasks in one event loop, not memory shared by separate processes.

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

Then explain why this lock protects coroutines sharing one event loop but does
**not** protect multiple processes.

---

## 19. Deliberately introduce the blocking bug

This phase turns event-loop responsiveness into an experiment rather than an
assumption. Compare blocking and cooperative waits, then confirm with timestamps
that one bad coroutine can pause unrelated tasks on the same loop.

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

## 20. Async vs threading

This phase chooses threads for blocking operations that cannot be awaited
directly. Measure the trade-off in thread creation, shared state, cancellation,
and whether the underlying library actually releases the GIL while waiting.

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

## 21. CPU-bound processing

This phase moves expensive computation away from the event loop and into worker
processes. Define a serializable input and result contract, then account for
process startup and data-transfer costs before claiming an improvement.

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

## 22. Demonstrate the GIL

This phase uses controlled benchmarks to explain why threads and processes can
behave differently for CPU and I/O workloads. Results are evidence for this
machine and workload, not a universal performance promise.

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

## 23. Decorator system

This phase adds reusable timing, logging, retry, and counting behavior while
preserving normal and asynchronous call semantics. Test decorator order,
metadata, arguments, return values, and exception propagation explicitly.

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

- normal functions
- async functions
- `*args`
- `**kwargs`

And must preserve metadata with:

```python
functools.wraps
```

This is a good test of whether you actually understand decorators rather than
just their syntax.

---

## 24. Async-aware retry decorator

This phase makes retry delays cooperative and failure selection deliberate. The
decorator should preserve the final exception, avoid retrying permanent errors,
and stop promptly when cancellation requests the operation to end.

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

## 25. Context-managed pipeline

This phase gives synchronous and asynchronous sessions a formal resource
boundary. Entering a session prepares dependencies; exiting it must release
workers, flush state, and preserve the original exception when cleanup succeeds.

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

## 26. Graceful shutdown

This phase defines shutdown as a state transition rather than an abrupt exit.
The engine must stop accepting work, settle or cancel pending work according to
policy, close executors, flush observations, and leave a recoverable snapshot.

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

- cancellation
- `asyncio.Task`
- cleanup
- context managers
- exceptions
- event loop shutdown

---

## 27. Snapshot engine

This phase connects processing results to durable run history. A snapshot should
be self-describing, consistently keyed, safe to write, and sufficient to explain
what changed between two runs without consulting in-memory objects.

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

## 28. Memory profiler

This phase turns memory behavior into measured evidence. Report what each tool
actually measures, distinguish current from peak allocations, and relate object
counts to queue size, cache policy, and retained results.

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

## 29. Type the entire system

This phase uses type information to make contracts visible across module and
process boundaries. Types should clarify valid states and plugin interfaces,
not merely annotate every variable without improving design or checking.

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

## 30. Add a plugin registry

This phase makes processor selection data-driven. The registry should normalize
extensions, define duplicate-registration behavior, report unsupported formats
clearly, and allow the engine to remain unchanged when a processor is replaced.

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

- dictionaries
- classes
- protocols
- generics
- exceptions
- object identity
- composition

---

## 31. Build an event system

This phase separates facts about pipeline activity from the components that
observe them. Events should carry enough context for metrics and logs while
listeners remain unable to alter the processing result accidentally.

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

## 32. Final system

This phase integrates every earlier contract into one operational workflow. The
CLI should expose useful commands and status, while the engine remains testable
without terminal input and continues to behave predictably under load and
failure.

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

`*` Don't actually add an API. Keep the interface as a CLI. The architecture can
be API-ready without building one.

---

## What this project demonstrates

Use this table as a verification map, not just a list of vocabulary. Each row
should correspond to working code, a focused test, or a benchmark whose result
you can explain in terms of runtime behavior.

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

## The part that makes it genuinely expert-level

This section turns implementation into investigation. Deliberately build small
experiments, record their conditions and observations, and explain where the
results may not generalize before applying a conclusion to the main engine.

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

This turns the project into both an application **and a Python runtime
laboratory**.

---

## The interview questions this project prepares you for

These questions are prompts for reasoning from your own measurements and design
decisions. A strong answer should identify assumptions, failure modes, and
trade-offs rather than recite a definition without connecting it to PyFlow.

By the end, you should be able to answer these from experience rather than
memorization:

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
> How would you replace one processor implementation without changing the
> pipeline?
> Where should shared state live?
> How would you prevent unbounded task creation?

### Concurrency

> Why use an `asyncio.Queue`?
> What is backpressure?
> What does `asyncio.Lock` protect?
> Does an asyncio lock protect multiple processes?
> What happens if one coroutine performs blocking CPU work?

If you can **build PyFlow, profile it, deliberately break it, fix it, benchmark
the alternatives, and explain the results**, you're no longer just demonstrating
that you know Python syntax.

You're demonstrating that you understand **Python as a runtime and as a systems
programming environment**.
