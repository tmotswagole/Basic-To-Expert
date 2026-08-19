# Basic-To-Expert

This is a list of projects showing my coding proficiency across multiple
technologies.

**THE COMPLETE TECHNICAL**  
**INTERVIEW & MASTERY GUIDE**

Python · FastAPI · PostgreSQL · Redis · Supabase · Next.js

Security · API Design · LLMs · RAG · AI Agents · System Design · DevOps

_Basic → Intermediate → Expert, one domain at a time._

Prepared for Thabiso Motswagole  
August 2026

## **How This Guide Works**

Each domain below is split into three levels: Basic, Intermediate, and Expert.
Basic covers what you need to hold a conversation about the topic without
embarrassing yourself. Intermediate is where most mid-level interview questions
live — the trade-offs, the 'why' behind the tool. Expert is where senior and
staff-level questions live: failure modes, scaling limits, and the follow-up
question after your first answer.

Work through a domain top to bottom rather than jumping straight to Expert — the
later sections assume the earlier ones. Code blocks are meant to be typed out
and run, not just read. Tables are built for quick pre-interview review; skim
them the morning of.

The domain order follows the priority weighting that makes sense for your stack:
Python and FastAPI first, then PostgreSQL and Redis, then Next.js and Supabase,
then the AI-native layer (LLMs, RAG, Agents), and finally System Design and
DevOps, which pull everything else together.

## **Table of Contents**

**1\. Python** _— Basic · Intermediate · Expert_

**2\. FastAPI** _— Basic · Intermediate · Expert_

**3\. PostgreSQL** _— Basic · Intermediate · Expert_

**4\. Redis** _— Basic · Intermediate · Expert_

**5\. Supabase** _— Basic · Intermediate · Expert_

**6\. Next.js** _— Basic · Intermediate · Expert_

**7\. Authentication & Security** _— Basic · Intermediate · Expert_

**8\. API Design** _— Basic · Intermediate · Expert_

**9\. LLMs & AI Engineering** _— Basic · Intermediate · Expert_

**10\. RAG (Retrieval-Augmented Generation)** _— Basic · Intermediate · Expert_

**11\. AI Agents** _— Basic · Intermediate · Expert_

**12\. System Design** _— Basic · Intermediate · Expert_

**13\. DevOps & Deployment** _— Basic · Intermediate · Expert_

## Appendix: Priority Resources

## Appendix: Study Time Allocation

## **1\. Python**

_Python is the language underneath FastAPI, your LLM orchestration code, and
most of the scraping and automation work you already run through Make.com.
Interviewers use it to check whether you understand what's happening under the
syntax, not whether you've memorized the standard library._

### **BASIC _— Python_**

#### **Core types and mutability**

Lists, dicts, and sets are mutable — you can change them in place, and that
matters the moment you pass one into a function or use it as a default argument.
Tuples, strings, ints, floats, and frozensets are immutable; any 'change'
actually builds a new object.

- list: ordered, mutable, allows duplicates — \[1, 2, 3\]

- tuple: ordered, immutable — (1, 2, 3), often used for fixed records

- set: unordered, unique elements, O(1) average membership test — {1, 2, 3}

- dict: key-value mapping, O(1) average lookup, insertion order preserved since
  3.7

- The classic footgun: def f(x, cache=\[\]): — the default list is created once,
  at function definition, and shared across every call that doesn't pass its
  own.

#### **is vs \==**

\== compares values. is compares identity — whether two names point to the same
object in memory. Use is only for None, True, and False. CPython caches small
ints and short strings, which is why a is b sometimes looks true for values by
accident; never rely on that.

#### **Functions, \*args, \*\*kwargs**

```text

```

\*args collects extra positional arguments into a tuple; \*\*kwargs collects
extra keyword arguments into a dict. You'll use this pattern constantly wrapping
LLM tool calls where the argument shape isn't known ahead of time.

#### **Classes and objects**

A class defines the shape and behavior; an object is an instance of it.
\_\_init\_\_ runs after the object already exists (that's \_\_new\_\_'s job) and
sets its initial state. Inheritance lets a subclass reuse and override a
parent's behavior; composition builds an object out of other objects instead,
and is usually the safer default when the relationship isn't a strict 'is-a'.

#### **Exceptions**

```text

```

Catch the narrowest exception type you can actually handle. A bare except:
swallows KeyboardInterrupt and SystemExit along with real bugs, and it's an
instant red flag in an interview.

### **INTERMEDIATE _— Python_**

#### **The object model**

Creating an instance is a two-step process: Python calls \_\_new\_\_ to allocate
the object, then \_\_init\_\_ to initialize it. Almost everyone only overrides
\_\_init\_\_; you override \_\_new\_\_ when you need to control allocation
itself, as with immutable subclasses or singletons.

- \_\_repr\_\_: unambiguous, for developers — should ideally be valid Python
  that recreates the object

- \_\_str\_\_: readable, for end users — falls back to \_\_repr\_\_ if not
  defined

- \_\_eq\_\_: defines value equality; if you override it you should also define
  \_\_hash\_\_ or the object becomes unhashable

- \_\_len\_\_: powers len(obj) and truthiness in some contexts

- \_\_hash\_\_: required for an object to be a dict key or set member

#### **Shallow vs deep copy**

```text

```

A shallow copy duplicates only the top level. If the contents are themselves
mutable and shared, mutating them affects both copies. deepcopy recursively
rebuilds every nested structure, which is safer but costs more.

#### **Decorators**

```text

```

A decorator is a function that takes a function and returns a replacement.
functools.wraps preserves the original function's name and docstring — skip it
and every decorated function looks like 'wrapper' in stack traces and
introspection. @property, @staticmethod, and @classmethod are decorators built
into the language: @property turns a method into an attribute-like accessor,
@staticmethod strips the implicit self, @classmethod passes the class itself as
the first argument instead.

#### **Generators and lazy evaluation**

```text

```

A generator produces values one at a time instead of building the whole result
in memory. yield pauses the function and hands back a value; the function
resumes from that exact point on the next call. This is the difference between
loading a 10GB export file into a list and streaming it row by row.

#### **Context managers**

```text

```

with guarantees \_\_exit\_\_ runs even if the block raises, which makes it the
right tool for anything that must be released or finalized: files, locks, DB
transactions, timers. contextlib.contextmanager lets you write the same thing as
a generator function with a single yield splitting setup from teardown.

### **EXPERT _— Python_**

#### **Async Python and the event loop**

asyncio runs a single-threaded event loop that switches between coroutines at
await points. Nothing runs in true parallel; what you get is concurrency during
I/O waits. A CPU-bound loop with no awaits blocks the entire event loop — every
other coroutine, including the ones handling other users' requests, stalls
behind it.

```text

```

- asyncio.gather() runs coroutines concurrently and returns results in order

- asyncio.create\_task() schedules a coroutine to start running now, without
  waiting for it

- An async lock (asyncio.Lock) protects shared state between coroutines on the
  same loop — it does not protect against multiple processes

- CPU-bound work belongs in a process pool
  (concurrent.futures.ProcessPoolExecutor) or a separate worker; threading helps
  with blocking I/O calls that don't have an async version

- A synchronous, blocking call inside an async function (e.g. calling requests
  instead of httpx) blocks the whole loop, not just that coroutine — this is the
  single most common async bug in FastAPI apps

#### **Memory model and reference counting**

CPython uses reference counting plus a cyclic garbage collector for reference
cycles reference counting alone can't catch (an object graph that references
itself). sys.getrefcount, weak references (weakref module), and \_\_slots\_\_
(which trades dynamic attribute assignment for a fixed, lower-memory layout)
come up in interviews about memory-sensitive services — long-running workers
processing millions of small objects are where this actually bites you.

#### **Typing for large codebases**

| from typing import Protocol, TypeVar, Generic class Retriever(Protocol): def
search(self, query: str, k: int \= 5\) \-\> list\[dict\]: ... T \= TypeVar("T")
class Cache(Generic\[T\]): def get(self, key: str) \-\> T | None: ... def
set(self, key: str, value: T) \-\> None: ... | | :---- |

Protocol gives you structural typing — anything with a matching search method
satisfies Retriever, no inheritance required. This is how you decouple a RAG
pipeline's business logic from a specific vector-database client: swap Milvus
for pgvector without touching the calling code, as long as both satisfy the same
Protocol.

#### **Concurrency model comparison**

| Model           | Best for                                                      | Limitation                                                          |
| :-------------- | :------------------------------------------------------------ | :------------------------------------------------------------------ |
| asyncio         | High-volume I/O-bound work (API calls, DB queries, LLM calls) | One blocking call stalls the whole loop                             |
| threading       | I/O-bound work using libraries without async support          | GIL prevents true CPU parallelism                                   |
| multiprocessing | CPU-bound work (embeddings, parsing, image processing)        | Higher memory overhead, slower startup, no shared memory by default |

#### **Interview-ready explanations to have ready**

- Why dict lookup is O(1) average but O(n) worst case (hash collisions)

- Why list.insert(0, x) is O(n) but list.append(x) is amortized O(1)

- The difference between a memory leak from a reference cycle and one from a
  growing cache with no eviction

- Why 'async def' alone doesn't make code fast — it removes blocking, it doesn't
  add parallelism

- GIL: what it is, why it exists, and why it doesn't matter for I/O-bound async
  code but does for CPU-bound threaded code

## **2\. FastAPI**

_FastAPI is the layer that turns your Python logic into an HTTP API — the same
role it plays in Jurifica's LRMAS backend. Interviewers use it as a proxy for
whether you understand request lifecycles, validation, and where async actually
helps._

### **BASIC _— FastAPI_**

#### **Anatomy of a route**

```text

```

Path parameters (case\_id) come from the URL. Query parameters (include\_docs)
come from the query string and get a default when you give them one. FastAPI
infers all of this from the function signature and type hints — no separate
schema file to keep in sync.

#### **Request bodies with Pydantic**

```text

```

Pydantic validates the incoming JSON against the model before your function body
ever runs. A malformed request gets a 422 automatically, with a body telling the
client exactly which field failed and why — you don't write that validation code
yourself.

#### **Status codes worth knowing cold**

| Code | Meaning               | When                                        |
| :--- | :-------------------- | :------------------------------------------ |
| 200  | OK                    | Successful GET/PUT                          |
| 201  | Created               | Successful POST that creates a resource     |
| 204  | No Content            | Successful DELETE, nothing to return        |
| 400  | Bad Request           | Malformed request, client's fault           |
| 401  | Unauthorized          | Missing or invalid credentials              |
| 403  | Forbidden             | Authenticated but not allowed               |
| 404  | Not Found             | Resource doesn't exist                      |
| 409  | Conflict              | State conflict, e.g. duplicate unique field |
| 422  | Unprocessable Entity  | Validation failed (Pydantic's default)      |
| 429  | Too Many Requests     | Rate limited                                |
| 500  | Internal Server Error | Unhandled exception                         |

#### **Automatic docs**

Every route you define shows up at /docs (Swagger UI) and /redoc, generated
straight from your type hints and Pydantic models. This is free documentation
that can't drift out of sync with the code, because it is the code.

### **INTERMEDIATE _— FastAPI_**

#### **Dependency injection**

```text

```

Depends() is FastAPI's way of injecting reusable logic — DB sessions, auth
checks, shared query parameters — into a route without duplicating code.
Dependencies can depend on other dependencies, and FastAPI resolves the whole
chain, caching results within a single request so get\_db doesn't open two
connections if two dependencies both need it.

The reason to reach for it instead of just calling a helper function directly:
testability. In tests you override a dependency
(app.dependency\_overrides\[get\_db\] \= get\_test\_db) and swap in a fake
without touching route code.

#### **Middleware vs dependency injection**

Middleware wraps every request regardless of route — logging, CORS, request IDs,
gzip. Dependencies are scoped to the routes that declare them and can access
path/query parameters and raise route-specific errors. If the logic needs to
know which route matched or what the validated body looked like, it belongs in a
dependency; if it needs to run universally before routing even happens, it's
middleware.

#### **Background tasks vs a real queue**

```text

```

BackgroundTasks runs after the response is sent, in the same process. It's fine
for a quick email send. It is the wrong tool for anything that takes more than a
couple of seconds, needs retries, or must survive a server restart — an LLM
document-processing job, a large batch export — because there's no persistence
and no worker isolation. That belongs in Celery, Redis Queue, or a dedicated
worker process reading off a queue.

#### **Error handling**

```text

```

Centralized exception handlers keep route bodies clean — raise domain exceptions
(CaseNotFoundError, InvalidJurisdictionError) from business logic and translate
them to HTTP responses in one place, instead of scattering try/except
HTTPException everywhere.

### **EXPERT _— FastAPI_**

#### **Async endpoints: when they actually help**

def routes run in FastAPI's thread pool automatically; async def routes run
directly on the event loop. The performance win from async only materializes if
every I/O call inside it is genuinely async (asyncpg, httpx.AsyncClient, an
async Redis client). Mix in a synchronous DB driver inside an async def and
you've blocked the event loop for every other request being served concurrently
— worse than just using def and letting the thread pool handle it.

#### **Lifespan events and connection pooling**

```text

```

Lifespan replaces the older startup/shutdown event decorators. It's where
connection pools, model clients, and cache clients get created once and shared
across the app's lifetime — never inside a route, or you'd open a new pool per
request.

#### **Testing async apps**

```text

```

httpx's AsyncClient with ASGITransport calls the app in-process, no real network
socket. Combine with dependency\_overrides for a fast, hermetic test suite.
TestClient (sync) still exists and is simpler for endpoints that don't need to
test concurrency behavior.

#### **Scaling a FastAPI service**

- Uvicorn workers (--workers N) give you process-level parallelism; each worker
  has its own event loop and DB pool, so pool sizes need to account for worker
  count × pool size ≤ DB max connections

- Put a reverse proxy (nginx, or a managed load balancer) in front for TLS
  termination and to fan out across workers/instances

- Long LLM calls behind a synchronous request-response cycle tie up a connection
  for the full generation time — for anything beyond a few seconds, move to SSE
  streaming or a job-plus-polling pattern so the connection isn't held open at
  full cost

- Rate limit at the gateway or with a Redis-backed limiter, not in application
  memory, or it won't survive multiple workers/instances agreeing on the same
  counter

#### **Security review checklist for a FastAPI service**

- Every mutating route behind an auth dependency, not just 'most of them'

- Response models (response\_model=) to strip fields you don't want serialized
  back out, e.g. password hashes

- Pydantic validators on anything used to build a file path, SQL fragment, or
  shell command

- CORS configured with an explicit origin allowlist, never
  allow\_origins=\['\*'\] alongside allow\_credentials=True

- Secrets loaded from environment/secret manager, never hardcoded or committed

## **3\. PostgreSQL**

_Postgres is the highest-leverage thing to study in this whole stack, because it
underpins Supabase, most of the RAG pipelines you'll build with pgvector, and
nearly every backend interview that isn't purely frontend._

### **BASIC _— PostgreSQL_**

#### **SQL fundamentals**

```text

```

WHERE filters rows before grouping; HAVING filters after GROUP BY, which is why
'HAVING COUNT(\*) \> 5' works but 'WHERE COUNT(\*) \> 5' doesn't — COUNT doesn't
exist yet at the point WHERE runs.

#### **Joins**

| Join            | Returns                                                                              |
| :-------------- | :----------------------------------------------------------------------------------- |
| INNER JOIN      | Only rows with a match in both tables                                                |
| LEFT JOIN       | All rows from the left table, matched or not (unmatched right-side columns are NULL) |
| RIGHT JOIN      | Mirror of LEFT JOIN                                                                  |
| FULL OUTER JOIN | All rows from both sides, matched or not                                             |
| CROSS JOIN      | Every row from A paired with every row from B (cartesian product)                    |

#### **Constraints**

```text

```

A primary key uniquely identifies a row and is implicitly NOT NULL and unique. A
foreign key ties a column to another table's primary key, and Postgres enforces
referential integrity — you can't insert a case with a client\_id that doesn't
exist, and by default you can't delete a client that still has cases (unless you
set ON DELETE CASCADE or SET NULL).

#### **Transactions, at a glance**

```text

```

Everything between BEGIN and COMMIT either all happens or none of it does. If
any statement fails, ROLLBACK undoes the whole block. This is what stops a bank
transfer from debiting one account and crashing before it credits the other.

### **INTERMEDIATE _— PostgreSQL_**

#### **ACID, explained with the transfer example**

| Property    | In the transfer                                                                                           |
| :---------- | :-------------------------------------------------------------------------------------------------------- |
| Atomicity   | Debit and credit succeed together or not at all                                                           |
| Consistency | Balances can't go negative if a CHECK constraint says so — the DB enforces its own rules before and after |
| Isolation   | A concurrent read of account A mid-transfer doesn't see a half-updated state                              |
| Durability  | Once COMMIT returns, the transfer survives a crash a millisecond later                                    |

#### **Isolation levels**

Postgres defaults to Read Committed: each statement sees only data committed
before it started, so a long transaction can still see different values across
two SELECTs if something else commits in between (a non-repeatable read).
Repeatable Read fixes that by taking a consistent snapshot for the whole
transaction. Serializable adds full protection against phantom reads and write
skew, at the cost of possible serialization failures your app has to retry.

- Dirty read: seeing another transaction's uncommitted change — Postgres never
  allows this, even at its loosest level

- Non-repeatable read: the same query returns different results within one
  transaction because another transaction committed in between

- Phantom read: a range query returns a different set of rows on a second run
  within the same transaction

#### **MVCC**

Postgres doesn't lock a row for readers the way some databases do. Every UPDATE
writes a new row version and marks the old one invisible to future transactions
rather than overwriting it in place; readers see a consistent snapshot without
blocking writers, and writers don't block readers. This is why Postgres handles
high read concurrency well, and also why VACUUM exists — those old row versions
('dead tuples') pile up and need to be reclaimed.

#### **Indexes**

```text

```

A B-tree index (the default) speeds up equality and range lookups on ordered
data. A composite index on (jurisdiction, status) helps a query filtering on
jurisdiction alone, or on both columns, but not on status alone — column order
matters, leftmost prefix rule. A partial index (WHERE status \= 'open') is
smaller and faster when most queries only care about a subset of rows.

Every index speeds up reads and slows down writes, since each INSERT/UPDATE has
to maintain it too. Indexing every column 'just in case' is a common junior
mistake — it's a real cost, not a free win.

#### **EXPLAIN ANALYZE**

```text

```

EXPLAIN shows the planned query path; ANALYZE actually runs it and shows real
timings. A Seq Scan on a large table where you expected an Index Scan usually
means a missing index, a function wrapped around the column (which defeats the
index unless it's a functional index), or the planner deciding a sequential scan
is cheaper because the table is small or the filter matches most rows.

### **EXPERT _— PostgreSQL_**

#### **Investigating a slow query, methodically**

- Reproduce it with EXPLAIN ANALYZE, not just EXPLAIN — estimated costs and real
  timings diverge when statistics are stale

- Compare estimated vs actual row counts; a big gap means the planner's
  statistics are out of date — run ANALYZE on the table

- Check for sequential scans on large tables and whether an index exists that
  the planner should be using

- Check join order and join type (nested loop vs hash vs merge) — a nested loop
  over a large unindexed table is the classic 8-second query

- Check for implicit type casts in WHERE clauses that silently disable index
  usage

- Check connection-level context: is the DB under load from something else, is
  autovacuum currently running on this table

#### **Advanced query tools**

```text

```

Window functions compute aggregates across a set of rows related to the current
one without collapsing them into groups, unlike GROUP BY. Recursive CTEs walk
hierarchical or graph-shaped data — org charts, category trees, citation chains
— in pure SQL.

#### **Scaling Postgres**

| Technique                                | Solves                                                                | Trade-off                                                                                   |
| :--------------------------------------- | :-------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| Connection pooling (PgBouncer/Supavisor) | Too many app-level connections exhausting Postgres's connection limit | Adds a hop; transaction-mode pooling breaks session-level features like prepared statements |
| Read replicas                            | Read-heavy load                                                       | Replication lag means replicas can serve slightly stale data                                |
| Partitioning                             | Very large single tables (time-series, logs)                          | Query planning and maintenance get more complex; cross-partition queries can be slower      |
| Sharding                                 | Write throughput beyond a single primary's capacity                   | Significant application complexity; cross-shard joins/transactions are hard                 |
| Materialized views                       | Expensive aggregate queries run often                                 | Data is only as fresh as the last REFRESH                                                   |

#### **pgvector for RAG**

```text

```

HNSW builds a navigable graph over the vectors for fast approximate
nearest-neighbor search — better recall/speed trade-off than IVFFlat for most
workloads, at a higher build cost and memory footprint. Because it lives in the
same database as your relational data, you can combine a vector similarity ORDER
BY with an ordinary WHERE clause (jurisdiction \= 'BW' AND document\_type \=
'regulation') in one query — hybrid filtering without a second system to keep in
sync.

#### **Replication and durability**

Streaming replication ships WAL (write-ahead log) segments from primary to
replica; synchronous replication waits for a replica to confirm before
committing on the primary (safer, slower), asynchronous doesn't wait (faster,
small window of data loss on failover). Logical replication replicates at the
row/table level instead of the byte level, which is what lets you replicate a
subset of tables or replicate into a different schema version — useful for
zero-downtime migrations.

## **4\. Redis**

_Redis shows up in this stack as a cache, a rate limiter, a session store, and a
lightweight message bus. Treating it as 'just a cache' is the fastest way to
miss half an interview's questions about it._

### **BASIC _— Redis_**

#### **Data structures and what they're for**

| Type       | Use case                                                          |
| :--------- | :---------------------------------------------------------------- |
| String     | Simple key-value, counters, cached blobs (SET/GET, INCR)          |
| Hash       | An object's fields without separate keys (a user record)          |
| List       | Ordered queue, recent-activity feed (LPUSH/RPOP)                  |
| Set        | Unique membership, tag sets, deduplication                        |
| Sorted Set | Leaderboards, priority queues, rate-limit windows (score-ordered) |
| Stream     | Append-only event log with consumer groups                        |

#### **Cache-aside, the default pattern**

```text

```

The application checks the cache first; on a miss it reads from the source of
truth and populates the cache with a TTL. This is the pattern to reach for by
default — simple, and the cache can never get permanently ahead of or behind the
database in a way that's hard to reason about.

#### **TTL**

Every cached key should have an expiry unless you have a specific reason it
shouldn't. TTL is also how you implement sessions, OTPs, and short-lived tokens
without a separate cleanup job — Redis just drops the key when it expires.

### **INTERMEDIATE _— Redis_**

#### **Cache strategies beyond cache-aside**

| Strategy      | How it works                                                | Trade-off                                                        |
| :------------ | :---------------------------------------------------------- | :--------------------------------------------------------------- |
| Cache-aside   | App checks cache, falls back to DB on miss, populates cache | Simple; first request after expiry is always slow                |
| Write-through | Every write goes to cache and DB together                   | Cache always warm; extra write latency                           |
| Write-back    | Write to cache first, persist to DB later (async)           | Fast writes; risk of data loss if the cache dies before flushing |
| Read-through  | Cache layer itself knows how to load from the DB on miss    | App code is simpler; requires a cache layer that supports it     |

#### **Invalidation**

The hard part of caching is knowing when a cached value is wrong. TTL-based
expiry is the simplest answer and often good enough. Explicit invalidation
(deleting or updating the key on write) keeps the cache more accurate but means
every write path has to remember to do it. Versioned keys (cache:v3:user:123)
sidestep invalidation entirely — bump the version and old keys just age out
unused.

#### **Rate limiting**

```text

```

Fixed window is cheap but lets a client burst up to 2x the limit right at the
window boundary. Sliding window log is accurate but costs more memory per key.
Token bucket allows controlled bursts while enforcing a steady average rate,
which is usually what you actually want for an API — a client that's been idle
can spend a small burst, but can't sustain above the configured rate.

#### **Pub/Sub, and its limits**

Pub/Sub is fire-and-forget: if no subscriber is listening when a message
publishes, that message is gone. It's fine for ephemeral broadcast (live
dashboard updates, presence pings) and wrong for anything that needs delivery
guarantees or replay.

### **EXPERT _— Redis_**

#### **Streams for durable event handling**

```text

```

Streams persist entries and support consumer groups, so multiple workers can
split the load, each message gets acknowledged once processed, and
unacknowledged ('pending') entries can be reclaimed if a worker crashes
mid-processing. This is Redis's answer to 'I need Pub/Sub but I actually need it
not to lose messages.'

#### **Distributed locks**

```text

```

NX means 'only set if it doesn't already exist' — that's the lock acquisition.
The unique token per lock holder matters because release should be a
compare-and-delete (only delete if the value still matches your token), or you
risk one process releasing a lock that a different process now holds after the
original TTL expired. Redlock (the multi-instance algorithm for stronger
guarantees) is contested in the distributed-systems community — know that a
single-instance Redis lock is a pragmatic mutual-exclusion tool for low-stakes
coordination, not a linearizable guarantee for correctness-critical work like
financial double-spend prevention.

#### **Scaling Redis**

- Redis is single-threaded for command execution (though I/O threading exists in
  newer versions) — a slow command (a huge KEYS scan, an unbounded SORT) blocks
  everything else on that instance

- Use SCAN instead of KEYS in production; KEYS walks the whole keyspace
  synchronously

- Redis Cluster shards data across nodes by hash slot; multi-key operations
  across shards need care (hash tags: {user:123}:profile keeps related keys on
  the same shard)

- Persistence options: RDB snapshots (periodic, faster restarts, can lose recent
  writes) vs AOF (every write logged, safer, larger files, slower restarts) —
  many production setups run both

- Client-side caching (RESP3 tracking) pushes invalidation events to clients
  holding a local cache of a key, cutting network round-trips for very hot keys

#### **Redis vs a real message queue**

Redis Pub/Sub and Streams are good enough for a lot of internal event-driven
work, but for guaranteed delivery, complex routing, dead-letter queues, and
cross-service durability at scale, purpose-built systems (Kafka, RabbitMQ, SQS)
give you more built-in guarantees. Reaching for Redis first and only migrating
when you hit an actual limit is a reasonable default, not a mistake.

## **5\. Supabase**

_Supabase packages managed Postgres with auth, storage, realtime, and edge
functions. In interviews, most of the interesting questions collapse into one
topic: Row Level Security, because it's the part people get wrong._

### **BASIC _— Supabase_**

#### **The core pieces**

- PostgreSQL — a real, full Postgres instance, not a proprietary database with
  SQL-like syntax bolted on

- Auth — email/password, OAuth, magic links, session and JWT management

- Storage — S3-like file buckets with access policies

- Realtime — subscribe to database changes over websockets

- Edge Functions — Deno-based serverless functions for logic close to the
  database

#### **Two keys, two very different trust levels**

| Key                    | Respects RLS?              | Where it belongs                            |
| :--------------------- | :------------------------- | :------------------------------------------ |
| anon / publishable key | Yes                        | Client-side code, browsers, mobile apps     |
| service\_role key      | No — bypasses RLS entirely | Server-side only, never shipped to a client |

The service role key is effectively database-admin-in-a-string. Shipping it in
frontend code, even accidentally through a bundled env var, hands out full
read/write access to every table.

#### **Auth basics**

Supabase Auth issues JWTs on login, backed by Postgres user records. The JWT's
claims (including the user's ID as auth.uid()) are what RLS policies check
against, which is the thread connecting auth to authorization.

### **INTERMEDIATE _— Supabase_**

#### **Row Level Security**

```text

```

RLS policies act as an implicit WHERE clause Postgres attaches to every query
against the table, per user, enforced at the database layer. USING controls
which existing rows are visible/affected; WITH CHECK controls what new or
modified rows are allowed to look like — they're not the same thing, and a
policy that only sets USING lets a user insert a row they then can't see, which
usually isn't the intent.

Why this matters versus a frontend check: a frontend permission check only stops
a well-behaved client. Anyone can call the Supabase REST API directly with the
anon key and skip your UI entirely. RLS is the actual security boundary because
it's enforced by the database no matter what called it.

#### **Storage policies**

Storage buckets can be public (anyone with the URL can read) or private (access
controlled by policies, similar in shape to RLS but on storage.objects). Signed
URLs grant time-limited access to a private object without making the whole
bucket public — the right tool for 'let this one client download this one
document for the next hour.'

#### **Realtime**

Realtime can stream Postgres row changes (INSERT/UPDATE/DELETE) to subscribed
clients, or carry ad-hoc broadcast messages and presence state that don't touch
the database at all. Row-change subscriptions still go through RLS — a client
only gets change events for rows it's allowed to see.

### **EXPERT _— Supabase_**

#### **RLS performance and design patterns**

```text

```

A naive RLS policy on a large table can turn an indexed query into something
that evaluates a subquery per row. Wrapping auth.uid() and similar functions in
a SELECT lets Postgres treat them as stable within the statement instead of
re-invoking per row — a well-documented, meaningful performance difference on
tables with real volume. Indexing the columns your policies filter on
(owner\_id, org\_id) matters exactly as much as it does for any other WHERE
clause, because that's what it becomes under the hood.

#### **Multi-tenant patterns**

Row-level tenancy (a tenant\_id/org\_id column plus RLS) is the common default —
one schema, isolation enforced by policy. Schema-per-tenant or
database-per-tenant give harder isolation at the cost of migration complexity
multiplying by tenant count. For a legal-tech platform handling
client-privileged documents, the choice of isolation strategy is itself a
client-facing trust question, not just an engineering one.

#### **Edge Functions vs FastAPI backend**

Edge Functions are good for logic that genuinely belongs close to the database
and benefits from low latency to it — webhooks, lightweight transforms, auth
triggers. For anything with real business logic, LLM orchestration, or a shared
codebase with your main backend, keeping that in your FastAPI service and
treating Supabase as managed Postgres \+ Auth is usually the cleaner
architecture — avoids splitting logic across two runtimes with different
deployment and observability stories.

#### **Auth edge cases interviewers probe**

- What happens to RLS if a table has RLS enabled but zero policies defined —
  nothing is accessible, by design, fail closed

- Why service\_role should only ever be used in a trusted server context, and
  why 'we'll just be careful with it in the frontend' is not an acceptable
  answer

- How SSR frameworks (Next.js) need to handle Supabase session cookies
  differently from a pure SPA — cookie-based session refresh on the server
  versus localStorage on the client

- Why RLS policies should be tested with actual queries as different users, not
  just read as SQL and assumed correct

## **6\. Next.js**

_Next.js interviews center on rendering strategy: what runs on the server, what
runs in the browser, and why that split exists at all._

### **BASIC _— Next.js_**

#### **App Router structure**

```text

```

Layouts nest — a layout wraps every page below it in the folder tree and
persists across navigations within it, so it doesn't remount and its state
doesn't reset when a child page changes.

#### **Server vs Client Components**

Every component is a Server Component by default. It renders on the server, can
access server-only resources (databases, secrets, filesystem) directly, and
ships zero JavaScript for that component to the browser. Add "use client" at the
top of a file to opt a component into the browser — you need this for anything
using useState, useEffect, event handlers, or browser-only APIs.

#### **Rendering models**

| Model | When it runs                                    | Good for                                                      |
| :---- | :---------------------------------------------- | :------------------------------------------------------------ |
| SSR   | Per request, on the server                      | Personalized or frequently-changing pages                     |
| SSG   | At build time                                   | Content that's the same for everyone and rarely changes       |
| ISR   | Built once, revalidated on a timer or on demand | Mostly-static content that updates occasionally               |
| CSR   | In the browser after JS loads                   | Highly interactive, user-specific UI where SEO doesn't matter |

### **INTERMEDIATE _— Next.js_**

#### **Hydration**

The server sends fully-rendered HTML; the browser downloads React and attaches
event handlers and interactivity to that existing HTML instead of re-rendering
it from scratch — that attachment step is hydration. A hydration mismatch
happens when the server-rendered HTML and what React would render on the client
don't agree — using Date.now() or Math.random() directly in render, or reading a
browser-only value (window, localStorage) during the initial render, are the
usual causes. React either warns and patches the DOM or, in bad cases, breaks in
confusing ways.

#### **Data fetching patterns**

```text

```

Server Actions let a form submit straight to server-side logic without you
hand-writing an API route and a fetch call. revalidatePath/revalidateTag tell
Next.js which cached data is now stale so the next render picks up the change.

#### **Caching layers**

Next.js has several independent caches that get confused for one thing
constantly: the fetch request cache (dedupes identical fetches within a render),
the full route cache (caches the rendered output of static routes), the router
cache (client-side, caches visited route segments for fast back/forward
navigation), and whatever your own backend or Redis layer does. A stale page
after a mutation is almost always one of these caches not being told to
revalidate, not a bug in the mutation itself.

### **EXPERT _— Next.js_**

#### **Streaming and Suspense**

```text

```

Streaming lets the server send the shell of a page immediately and fill in
slower sections as their data resolves, instead of holding the whole response
until every fetch finishes. Wrapping a slow Server Component in Suspense is what
unlocks this — the fallback renders first, gets swapped for real content when
it's ready, without blocking the rest of the page.

#### **Server Actions: security concerns**

A Server Action is a public HTTP endpoint under the hood, even though it looks
like a plain function call in your code. Treat every argument as untrusted input
exactly like a route handler — validate it, and re-check authorization inside
the action itself rather than assuming the UI that called it enforced the right
permissions, because nothing stops a request forged directly against that
action's endpoint.

#### **Rendering strategy trade-offs at scale**

| Choice                                   | Trade-off                                                                                 |
| :--------------------------------------- | :---------------------------------------------------------------------------------------- |
| ISR with a long revalidate window        | Cheap, fast, but users can see stale data until the next revalidation                     |
| On-demand revalidation via webhook       | Fresh immediately after a change, adds a moving part (the webhook) that can fail silently |
| Full SSR for personalized dashboards     | Always fresh, but every request pays full render cost — no free CDN caching               |
| Client-side fetching with TanStack Query | Fast perceived nav via cache, but ships more JS and loses SEO for that content            |

#### **State management: when not to reach for global state**

Server state (data from your API) belongs in something like TanStack Query, not
useState plus useEffect — it already solves caching, refetching, and race
conditions you'd otherwise hand-roll. Client-only UI state (a modal being open,
a form's draft values) belongs in local component state or Context. Redux or
Zustand earn their place when state is genuinely shared across many unrelated
parts of the tree and changes frequently enough that prop drilling or Context
re-renders become a real problem — not by default.

## **7\. Authentication & Security**

_This cuts across every layer of the stack. The through-line interviewers are
checking for: do you understand where the actual trust boundary is, versus where
it just looks like one._

### **BASIC _— Authentication & Security_**

#### **Authentication vs authorization**

Authentication answers 'who are you' — logging in, verifying credentials.
Authorization answers 'what are you allowed to do' — checking permissions after
identity is established. A system can authenticate someone correctly and still
authorize them incorrectly (checking the wrong thing, or checking it in the
wrong place).

#### **Password storage**

Passwords get hashed, never encrypted — hashing is one-way, so even a full
database leak doesn't hand over the original password. bcrypt and Argon2 are the
standard choices; both are deliberately slow and include a salt, which defeats
precomputed rainbow-table attacks and stops two users with the same password
from having the same hash.

#### **JWT structure**

A JWT has three parts: a header (algorithm and token type), a payload (claims —
user ID, expiry, roles), and a signature (proves the token wasn't tampered with,
assuming the signing secret stays secret). Anyone can decode and read the
payload without the secret — it's signed, not encrypted — so never put sensitive
data directly in JWT claims.

### **INTERMEDIATE _— Authentication & Security_**

#### **Access tokens vs refresh tokens**

Access tokens are short-lived (minutes to an hour) and sent with every request.
Refresh tokens live longer and are used only to get a new access token,
typically stored more carefully (HttpOnly cookie) since a leaked refresh token
is a much bigger problem than a leaked access token. Revocation is the standing
weakness of stateless JWTs — once issued, a token is valid until it expires,
unless you maintain a server-side denylist or check, which reintroduces the
statefulness JWTs were partly meant to avoid.

#### **Cookies vs localStorage for tokens**

| Storage         | XSS risk                               | CSRF risk                                |
| :-------------- | :------------------------------------- | :--------------------------------------- |
| localStorage    | High — any injected script can read it | None by itself                           |
| HttpOnly cookie | Low — JavaScript can't read it         | Needs CSRF protection (SameSite, tokens) |

HttpOnly cookies with SameSite=Lax or Strict are generally the safer default for
session tokens, because the most common real-world attack against a browser app
is XSS, and an HttpOnly cookie is invisible to any script running on the page,
injected or not.

#### **OAuth, the flow**

The user is redirected to the provider (Google, GitHub), authenticates there,
and the provider redirects back with an authorization code — not a token yet.
The application's backend exchanges that code, plus a client secret, for tokens
directly with the provider, server to server. The code-for-token exchange
happening server-side, away from the browser, is what keeps the client secret
secret.

#### **Common OWASP categories worth being fluent in**

- Injection — untrusted input reaching a query, command, or template interpreter
  as code instead of data

- Broken access control — checking authentication but not authorization, or
  checking authorization only in the UI

- Security misconfiguration — default credentials, verbose error messages
  leaking stack traces, permissive CORS

- Cryptographic failures — storing sensitive data in plaintext, weak or homemade
  hashing/encryption

- SSRF — a server-side request that follows a user-controlled URL somewhere it
  shouldn't (internal network, cloud metadata endpoint)

### **EXPERT _— Authentication & Security_**

#### **SQL injection: why parameterization is non-negotiable**

```text

```

Parameterized queries aren't just escaping special characters more carefully —
the query structure and the data are sent to the database as genuinely separate
things, so there's no string for an attacker's input to break out of, no matter
what it contains. An ORM doesn't automatically save you either; raw SQL
fragments built through string formatting inside an ORM call reopen the same
hole.

#### **Token revocation and rotation strategies**

- Short-lived access tokens plus refresh token rotation — each refresh issues a
  new refresh token and invalidates the old one, so a stolen refresh token that
  gets reused after the legitimate client also uses it can be detected and the
  whole chain revoked

- A server-side allowlist/denylist trades pure statelessness for real-time
  revocation — reasonable when the blast radius of a compromised token is high
  enough to justify the extra lookup

- Scoped tokens (narrow permissions per token) limit the damage of any single
  leaked token

#### **Designing auth for a multi-tenant SaaS**

Authentication proves who the user is once. Authorization then has to be checked
at every layer that touches tenant data — API route, service layer, and database
(RLS or equivalent) — because relying on just one layer means a bug anywhere
else in the stack becomes a full tenant-isolation breach. Defense in depth here
isn't paranoia, it's the actual design pattern: the database enforcing RLS is
what catches the bug in the API layer you didn't know you had.

#### **Threat-modeling questions worth rehearsing**

- What happens if a JWT signing secret leaks — every token becomes forgeable
  until you rotate the secret and invalidate existing sessions

- What happens if an attacker gets a valid but expired-soon access token —
  bounded by the token's remaining lifetime, which is the whole argument for
  keeping access tokens short

- What stops one tenant's API key from reading another tenant's data if a query
  is missing a WHERE clause — ideally, RLS, not application code discipline
  alone

- How do you rotate a service-role or database credential without downtime —
  dual-credential period where old and new both work during rollout

## **8\. API Design**

_The practical question behind every API design interview: what happens to this
contract when the client and server can no longer deploy at the same time?_

### **BASIC _— API Design_**

#### **HTTP methods and what they mean**

| Method | Purpose                        | Idempotent?     |
| :----- | :----------------------------- | :-------------- |
| GET    | Read                           | Yes             |
| POST   | Create / non-idempotent action | No              |
| PUT    | Replace a resource entirely    | Yes             |
| PATCH  | Partially update a resource    | Not necessarily |
| DELETE | Remove a resource              | Yes             |

Idempotent means calling it once or five times leaves the system in the same
state. That's why retrying a failed GET or PUT is safe by default, and retrying
a failed POST without an idempotency key can create duplicates.

#### **REST resource naming**

```text

```

Resources are nouns, plural, and the verb comes from the HTTP method — not from
the URL. /getCases or /cases/delete/{id} is a sign the design leaked from an RPC
mindset into what's supposed to be a REST interface.

### **INTERMEDIATE _— API Design_**

#### **Pagination**

| Style  | Example                  | Weakness                                                                                      |
| :----- | :----------------------- | :-------------------------------------------------------------------------------------------- |
| Offset | ?page=10\&limit=20       | Skipping large offsets gets slow; rows can shift between pages if data changes mid-pagination |
| Cursor | ?cursor=abc123\&limit=20 | Can't jump to an arbitrary page number, only forward/backward from a point                    |

Cursor pagination is usually the better default for large or frequently-changing
datasets — it stays stable even as new rows get inserted, and doesn't force the
database to scan and discard a growing number of skipped rows the deeper you
paginate.

#### **Versioning**

URL versioning (/api/v1/cases) is the most visible and the easiest for clients
to reason about, at the cost of duplicating routes across versions. Header-based
versioning keeps URLs stable but is less discoverable. Either way, the real
discipline is deciding what counts as a breaking change (removing a field,
changing a type) versus additive (a new optional field) — only the former needs
a version bump.

#### **WebSockets vs Server-Sent Events**

WebSockets are full-duplex — either side can send at any time — and are the
right choice for chat or collaborative editing. SSE is server-to-client only,
rides on plain HTTP, and reconnects automatically on drop, which is exactly the
shape of token-by-token LLM streaming: the client doesn't need to send anything
back mid-stream.

### **EXPERT _— API Design_**

#### **Backward compatibility as a design constraint**

A field that's now required used to be optional — that breaks every existing
client that omitted it. Removing a field breaks anyone still reading it. Even
changing a field's type (a string ID becoming a UUID object) breaks strict
parsers. The safe long-term habit: add fields as optional, deprecate before
removing, and never repurpose a field's meaning — introduce a new one instead.

#### **Rate limiting design**

| Algorithm      | Behavior                                                                                                           |
| :------------- | :----------------------------------------------------------------------------------------------------------------- |
| Fixed window   | Simple; allows a burst of up to 2x limit right at window boundaries                                                |
| Sliding window | More accurate; costs more to compute/store                                                                         |
| Token bucket   | Allows short bursts, enforces a steady average rate — usually the best fit for APIs                                |
| Leaky bucket   | Smooths bursts into a constant outflow rate — good for protecting a downstream system with a hard throughput limit |

#### **Designing for LLM-backed endpoints specifically**

- Streaming (SSE) for anything user-facing where generation takes more than
  \~1-2 seconds — perceived latency matters more than total latency

- Idempotency keys on any endpoint that triggers an expensive LLM call, so a
  client's network retry doesn't burn a second full generation

- Separate rate limits for token-expensive endpoints from cheap CRUD endpoints —
  one client hammering an LLM endpoint shouldn't be able to starve capacity for
  everyone else on the general API limit

- Explicit timeouts and a documented behavior for partial results if the LLM
  call is cut off mid-stream

- Cost/usage metadata (tokens used, model called) returned alongside the
  response for client-side or billing-side tracking

#### **gRPC vs REST vs GraphQL, when each earns its complexity**

REST is the right default for public or loosely-coupled APIs — cacheable, widely
understood, easy to debug with a browser or curl. GraphQL earns its complexity
when clients have genuinely different, unpredictable data needs and
over/under-fetching from a fixed REST shape is a real, measured problem, not a
hypothetical one. gRPC fits tightly-coupled internal service-to-service calls
where you control both ends and want strict schemas plus lower overhead than
JSON over HTTP — it's a worse fit for a public API where you don't control every
client's tooling.

## **9\. LLMs & AI Engineering**

_This is the section that separates a candidate who's used ChatGPT from one who
understands what's actually happening between a prompt going in and a response
coming out — and it's increasingly where AI-native roles spend most of the
interview._

### **BASIC _— LLMs & AI Engineering_**

#### **Tokens**

A model doesn't read words, it reads tokens — subword pieces produced by a
tokenizer. 'internationalization' might split into several tokens; a common
short word might be one. Token count, not character or word count, is what
determines cost, latency, and whether a prompt fits in the context window, which
is why prompt engineering pays attention to it directly.

#### **Temperature, top-k, top-p**

At each step the model produces a probability distribution over possible next
tokens. Temperature scales that distribution before sampling: low temperature
sharpens it toward the most likely tokens (more deterministic, more repetitive),
high temperature flattens it (more variety, more risk of incoherence). Top-k
restricts sampling to the k most likely tokens; top-p (nucleus sampling)
restricts to the smallest set of tokens whose combined probability exceeds p —
an adaptive cutoff instead of a fixed count.

#### **Why models hallucinate**

An LLM is a next-token predictor trained to produce plausible continuations, not
a database performing lookups. When it doesn't have the actual fact, it still
has to say something, and what it says is whatever's statistically likely to
follow — plausible-sounding and wrong. This is the entire reason RAG and tool
calling exist: they ground the model in real, retrievable facts instead of
asking it to recall everything from its weights.

#### **Zero-shot vs few-shot prompting**

Zero-shot gives the model just an instruction. Few-shot includes examples of the
input/output pattern you want before the real request, which reliably improves
consistency on tasks with a specific format or style — at the cost of extra
tokens per call.

### **INTERMEDIATE _— LLMs & AI Engineering_**

#### **Structured output**

```text

```

Instead of asking for prose and parsing it after the fact, define the schema you
want up front and either use the provider's native structured-output/JSON-mode
feature or validate the response against a schema (Pydantic) and retry on
failure. This turns an inherently fuzzy generation step into something a
downstream system can actually rely on programmatically.

#### **Tool / function calling**

The model doesn't execute anything itself. Given a set of tool definitions
(name, description, parameter schema), it decides a tool should be called and
returns a structured request to call it with specific arguments; your code
executes the actual function and returns the result back to the model, which
then produces its final answer grounded in that result. The critical design
point: the model choosing to call get\_account\_balance() instead of guessing a
number is the entire value — it converts 'plausible-sounding' into 'actually
looked up.'

```text

```

#### **Model routing by task complexity**

Not every call needs your most expensive model. Routing cheap classification or
extraction tasks to a smaller/faster model (Gemini Flash-Lite, Haiku-class
models) and reserving the larger model for genuinely hard reasoning steps is
standard practice in production LLM systems, and it's exactly the pattern behind
routing across Flash-Lite/Flash/Pro in Jurifica's architecture — match model
cost to task difficulty rather than defaulting every call to the top-tier model.

#### **Context window management**

A bigger context window doesn't mean you should fill it. Long contexts increase
cost and latency, and models don't attend to all parts of a long context equally
well — retrieval and summarization exist specifically to keep what actually
reaches the model relevant and small, rather than dumping everything in and
hoping the model finds the needle.

### **EXPERT _— LLMs & AI Engineering_**

#### **Attention, the intuition**

Self-attention lets each token look at every other token in the sequence and
weigh how relevant each one is to interpreting it, rather than processing
strictly left-to-right with a fixed memory like older recurrent architectures.
Each token produces a query, and is compared against every other token's key to
produce attention weights, which are then used to combine their values — that's
the query/key/value mechanism at the center of 'Attention Is All You Need.'
Multi-head attention runs several of these in parallel with different learned
projections, letting the model track different kinds of relationships (syntax,
coreference, topic) simultaneously.

#### **Evaluation, beyond 'does it look right'**

| Metric                      | What it checks                                                                                               |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------- |
| Faithfulness / groundedness | Does the answer actually follow from the retrieved/provided context, or did the model add unsupported claims |
| Answer correctness          | Is the answer actually right, independent of whether it's grounded                                           |
| Tool-call correctness       | Did the model call the right tool with the right arguments                                                   |
| Retrieval precision/recall  | Of what was retrieved, how much was relevant; of what was relevant, how much got retrieved                   |

LLM-as-judge (using a stronger model to grade a weaker model's outputs against a
rubric) scales better than pure human evaluation but needs its own validation
against a human-labeled sample, or you're just trusting one model's opinion of
another's without checking it holds up.

#### **Cost and latency engineering**

- Prompt caching: providers that support it charge less and respond faster for
  the cached portion of a repeated prompt prefix — structure prompts so the
  stable system/context part comes first and the variable part comes last

- Batch processing for anything not latency-sensitive — often meaningfully
  cheaper than synchronous calls

- Streaming for perceived latency even when total generation time doesn't change
  — the user sees the first token quickly instead of staring at a blank screen

- Track tokens in and out per call, per user, per feature — you can't optimize
  cost you're not measuring, and this is also what makes model routing decisions
  defensible with real numbers instead of guesses

#### **Reliability engineering around inherently non-deterministic calls**

Treat every LLM call like an unreliable network call, because it behaves like
one: set timeouts, retry with backoff on transient failures, validate structured
output against a schema and retry or fall back on failure, and have a defined
behavior for 'the model refused, errored, or returned garbage' rather than
letting that propagate as an unhandled exception into the response your user
sees.

## **10\. RAG (Retrieval-Augmented Generation)**

_RAG is where 'the model doesn't know your data' gets solved without retraining
anything. It's also one of the most heavily probed topics in AI engineering
interviews right now, because most real production LLM systems are RAG systems
in some form._

### **BASIC _— RAG (Retrieval-Augmented Generation)_**

#### **The basic pipeline**

```text

```

RAG splits the problem in two: an offline step that turns your documents into
searchable vectors, and a runtime step that finds the most relevant pieces of
those documents for a given question and hands them to the LLM as context,
instead of asking the model to answer from what it memorized during training.

#### **Why reach for RAG at all**

- The information isn't in the model's training data (private company documents,
  contracts, internal records)

- The information changes too often to retrain around (prices, inventory,
  current case status)

- You need the answer traceable to a specific source, which a model's internal
  knowledge can't give you

#### **Embeddings**

An embedding model turns text into a vector of numbers positioned so that
semantically similar text ends up close together in that vector space — 'how do
I reset my password' and 'I forgot my login' land near each other even without
sharing exact words, which is the whole advantage over plain keyword search.

### **INTERMEDIATE _— RAG (Retrieval-Augmented Generation)_**

#### **Chunking**

There's no universal right chunk size. Too large and irrelevant content dilutes
what the LLM actually needs, pushing up cost and sometimes hurting answer
quality; too small and a chunk loses the surrounding context needed to make
sense of it on its own. Fixed-size chunking is simplest and worst at respecting
document structure; semantic chunking (splitting at natural boundaries —
paragraphs, sections) tends to preserve meaning better at the cost of more
preprocessing. Overlap between chunks (a bit of shared text at each boundary)
helps avoid losing a fact that happens to sit right at a cut point.

#### **Similarity metrics**

| Metric             | Notes                                                                                           |
| :----------------- | :---------------------------------------------------------------------------------------------- |
| Cosine similarity  | Measures angle between vectors, ignores magnitude — the most common default for text embeddings |
| Dot product        | Cheaper to compute; equivalent to cosine similarity if vectors are normalized                   |
| Euclidean distance | Measures straight-line distance; less common for high-dimensional text embeddings               |

#### **Vector databases vs relational databases**

A vector database is built around approximate nearest-neighbor search over
high-dimensional vectors — a fundamentally different query pattern than a
relational database's exact-match/range filtering over rows. pgvector puts that
capability inside Postgres itself, so you get vector search alongside your
normal relational data and can combine both in a single query, rather than
syncing two separate systems and reconciling them when they drift.

#### **Hybrid search**

Pure semantic search misses exact matches on things like case numbers, statute
citations, or proper nouns the embedding model doesn't represent distinctly.
Combining vector similarity with keyword search (BM25) and metadata filtering
(jurisdiction \= 'BW', document\_type \= 'regulation') catches both the 'similar
meaning' cases and the 'exact term' cases a single method alone would miss.

### **EXPERT _— RAG (Retrieval-Augmented Generation)_**

#### **Reranking**

```text

```

Initial retrieval optimizes for speed across a large corpus and is necessarily
approximate. A reranker is a smaller, more expensive model that looks
specifically at the query paired with each candidate and produces a much more
precise relevance score — running it on 50 candidates instead of the whole
corpus keeps it fast while meaningfully improving what actually reaches the LLM.

#### **RAG evaluation, systematically**

- Retrieval precision: of the chunks retrieved, what fraction were actually
  relevant

- Retrieval recall: of the chunks that were relevant somewhere in the corpus,
  what fraction got retrieved

- Faithfulness: does the generated answer only make claims supported by the
  retrieved context

- Answer correctness: independent check against ground truth, since a faithful
  answer can still be wrong if the retrieved context itself was wrong or
  incomplete

- Citation correctness: if the system claims a source, does that source actually
  say what's being attributed to it

Ragas and similar frameworks automate a lot of this against a labeled evaluation
set. The habit that matters more than any specific tool: build the evaluation
set early, alongside the pipeline, not after something in production already
went wrong.

#### **Failure modes specific to legal/regulatory RAG**

- Retrieval pulling a superseded or repealed provision because the corpus wasn't
  kept current — versioning and effective-date metadata on ingested documents
  matters as much as the embeddings

- Cross-jurisdiction contamination: a UK precedent surfacing as relevant context
  for a Botswana-law question because it's semantically similar in topic but
  legally irrelevant — jurisdiction as a hard metadata filter, not just a soft
  ranking signal

- The model synthesizing a plausible-sounding rule from multiple retrieved
  fragments that, combined, misstate the actual law — faithfulness evaluation
  has to check this at the level of the final synthesized claim, not just 'was
  each sentence traceable to something'

#### **Scaling a RAG ingestion pipeline**

Chunking and embedding a large, growing corpus is itself a background-job
problem, not something to run synchronously in a request path — new document
uploads should enqueue an ingestion job, not block the response. Incremental
re-indexing (only re-embedding changed documents) matters once the corpus is
large enough that full re-indexing becomes slow or expensive to run on every
update.

## **11\. AI Agents**

_The line between 'an LLM application' and 'an agent' is whether the system can
decide what to do next on its own, based on what just happened — and that
autonomy is exactly what makes agents both powerful and harder to trust._

### **BASIC _— AI Agents_**

#### **What makes something an agent**

```text

```

A plain LLM call takes an input and produces an output once. An agent runs that
loop repeatedly, using the result of one step to decide the next one — it can
call a tool, look at what came back, and decide to call a different tool, ask a
clarifying question, or conclude it has enough information to answer.

#### **Core building blocks**

- Tool use — the set of functions the agent can call, each with a clear
  description and schema

- Planning — breaking a goal into steps, whether explicitly (write a plan first)
  or implicitly (decide the next step each iteration)

- Memory — what the agent remembers across steps (working memory) or across
  sessions (long-term memory)

- State management — tracking where the agent is in a multi-step process,
  especially if it can be paused and resumed

#### **ReAct, the classic pattern**

ReAct interleaves reasoning ('I need the account balance before I can answer
this') with acting (calling the tool) and observing (reading the result),
repeating until the model decides it has enough to answer. It's less a specific
library and more the mental model most agent frameworks implement under the
hood.

### **INTERMEDIATE _— AI Agents_**

#### **Human-in-the-loop**

Not every agent action should execute automatically. High-stakes or irreversible
actions — sending an email, executing a financial transaction, submitting a
legal filing — usually warrant a confirmation step before execution, where the
agent proposes the action and a human approves it, rather than full autonomy.
Where to draw that line is a product decision as much as an engineering one, and
it should scale with the cost of getting it wrong.

#### **Multi-agent systems: when they help**

| Orchestrator / | \\ Researcher Drafter Reviewer \\ | / Final output | | :----
|

Splitting a task across specialized agents makes sense when the sub-tasks
genuinely benefit from different context, tools, or prompting strategies — a
researcher agent with search tools and a reviewer agent with a strict rubric are
doing different enough jobs that combining them into one mega-prompt would hurt
both. It's unnecessary complexity when a single well-prompted agent with the
right tools could do the whole thing — multi-agent adds coordination overhead,
more failure surface, and more cost, and that has to be worth it.

#### **Why agents fail**

- Hallucinated tool parameters — the agent calls a real tool with a made-up
  argument value

- Incorrect tool selection — calling the wrong tool for the situation, or a tool
  that doesn't exist

- Infinite or near-infinite loops — the agent keeps retrying a failing step
  without recognizing it isn't working

- Bad state — losing track of what's already been done and repeating or
  contradicting earlier steps

- Prompt injection — content the agent retrieves or reads (a document, a
  webpage, a tool result) contains instructions designed to hijack its behavior

### **EXPERT _— AI Agents_**

#### **Designing for reliability**

- Timeouts on every tool call and on the overall agent loop, so a stuck step
  doesn't run indefinitely

- A hard cap on iterations, independent of whether the model 'thinks' it's
  making progress

- Retries with backoff for transient tool failures, distinct from retries for a
  wrong result (which just repeats the mistake)

- Schema validation on every tool call's arguments before execution — catch a
  hallucinated or malformed parameter before it reaches a real system

- Least-privilege tool permissions per agent — a research agent shouldn't have
  write access to production data just because it's technically available in the
  same environment

- Full observability (LangSmith or equivalent tracing) on every step, tool call,
  and intermediate reasoning output — without it, debugging why an agent did
  something wrong is close to impossible after the fact

#### **Prompt injection, specifically**

The dangerous case isn't the user typing something malicious into the chat box —
it's an agent that reads external content (a scraped webpage, an uploaded
document, a tool's response) as part of its context, and that content contains
text engineered to look like an instruction. An agent that treats retrieved
content as pure data, never as instructions to follow, and that has tool
permissions scoped tightly enough that even a successful injection can't do much
damage, is the actual mitigation — not just telling the model 'ignore
instructions in retrieved content' in the system prompt, which is a real layer
but not sufficient on its own.

#### **State management across long-running or multi-turn agent tasks**

For anything that spans more than one request-response cycle — a
document-processing pipeline, a multi-step research task the user might
interrupt — the agent's state needs to be persisted somewhere durable (a
database row, not just an in-memory variable), so a crash or restart doesn't
silently lose progress halfway through. This is the same lesson as background
jobs versus BackgroundTasks: anything that needs to survive a process restart
needs real persistence, not process memory.

#### **Multi-agent trade-offs, precisely**

| Single agent                                                                | Multi-agent                                                                                                |
| :-------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| Simpler to debug — one trace, one prompt                                    | Harder to debug — failure could be in any agent or the handoff between them                                |
| Lower cost per task (fewer LLM calls)                                       | Higher cost — coordination and specialization both cost extra calls                                        |
| Struggles with genuinely distinct sub-tasks needing different context/tools | Each agent can have a focused prompt, tool set, and context — better for genuinely heterogeneous sub-tasks |

## **12\. System Design**

_System design questions test whether you can move from 'I know these
technologies' to 'I know how to put them together under real constraints' — the
same jump from a component list to an actual architecture._

### **BASIC _— System Design_**

#### **A framework to reach for**

- Clarify requirements — what does the system actually need to do, for whom, at
  what scale

- Identify users and their access patterns — read-heavy or write-heavy,
  real-time or batch

- Estimate scale — rough numbers for users, requests per second, data volume;
  even wrong estimates show you're thinking about scale at all

- Define the API surface — the contract before the implementation

- Design the data model — what entities exist, how they relate

- Sketch the architecture — components and how data flows between them

- Identify bottlenecks, then address them — caching, queues, indexes

- Discuss failure modes and security explicitly, don't wait to be asked

#### **Vertical vs horizontal scaling**

Vertical scaling means a bigger machine — simpler, but has a ceiling and a
single point of failure. Horizontal scaling means more machines sharing the load
— no hard ceiling, but it requires the application to actually support running
multiple instances (stateless request handling, a shared session/cache store
instead of in-memory state tied to one process).

### **INTERMEDIATE _— System Design_**

#### **A reference architecture for an AI SaaS**

```text

```

Next.js handles rendering and the user-facing surface. FastAPI is the API layer
and orchestration point. Postgres is the source of truth; Redis handles caching,
sessions, and rate limiting; the LLM API and vector search power the AI-specific
features. Every arrow in that diagram is a place things can fail or get slow,
which is exactly what a system design interview is probing when it asks 'and
then what happens when X goes down.'

#### **Where caching goes**

Caching exists at multiple layers that don't automatically agree with each
other: CDN (static assets, sometimes full pages), application-level (Redis, for
computed results and session data), and database-level (query result caching,
materialized views). A cache invalidation bug in any one layer looks identical
to the others from the outside — 'the UI shows stale data' — so knowing which
layer is actually responsible matters for debugging, not just design.

#### **Queues for anything slow or unreliable**

Background jobs need a queue, not a fire-and-forget in-process task, whenever
the work can fail, take a while, or needs to survive the request that triggered
it. Document processing, LLM batch jobs, email sending, and video processing all
share the same shape: accept the request fast, enqueue the actual work, let a
pool of workers process it independently, and let the client poll or get
notified when it's done.

### **EXPERT _— System Design_**

#### **Failure modes to discuss unprompted**

- What happens if the LLM API is down or rate-limited — graceful degradation,
  cached/fallback responses, or a clear error rather than a hung request

- What happens if the database connection pool is exhausted — request queuing
  with a timeout, not unbounded queuing that eventually OOMs the process

- What happens if a background worker crashes mid-job — is the job resumable, or
  does it need to be idempotent enough to safely restart from the beginning

- What happens during a deploy — is there a moment where old and new code both
  run against the same database schema, and does that moment break anything

#### **Database scaling, in order of when you'd actually reach for each**

Indexes and query optimization first — most performance problems are solved here
and it's the cheapest fix. Connection pooling next, once concurrent load starts
exhausting connections. Read replicas once read load specifically is the
bottleneck and you can tolerate slight staleness. Partitioning once individual
tables get too large for efficient maintenance (vacuum, index rebuilds) even
with good indexes. Sharding last, once write throughput itself exceeds what a
single primary can handle — it's the most complex option and the one to delay as
long as legitimately possible, because it pushes real complexity into every part
of the application that touches data.

#### **Designing 'ChatGPT' as an interview question**

- Streaming responses (SSE) from day one — synchronous request/response for a
  multi-second generation is a bad user experience and ties up server resources
  for the full duration

- Conversation history storage — a message table keyed by conversation ID, with
  pagination for long conversations rather than loading the entire history into
  every request

- Rate limiting and usage tracking per user, separate from general API rate
  limiting, since LLM calls have real per-call cost unlike a typical CRUD
  request

- Context window management — deciding what history actually gets sent to the
  model on each turn, since sending the full conversation forever eventually
  exceeds the context window and gets expensive

- Horizontal scaling of the API layer behind a load balancer, with
  session/conversation state in a shared store (Postgres/Redis), not in-process
  memory tied to one server instance

#### **The senior-level test, applied to any component**

For any technology in the stack, be ready to answer, in order: why would I use
this, when would I not, what happens when it fails, how do I scale it, and how
do I monitor and secure it in production. That progression — not the ability to
list features — is what interviewers are actually listening for.

## **13\. DevOps & Deployment**

_You don't need to be a dedicated DevOps engineer for these interviews, but you
do need to be able to explain how your code actually gets from a laptop to
something users can hit._

### **BASIC _— DevOps & Deployment_**

#### **Docker essentials**

```text

```

An image is a built, immutable snapshot; a container is a running instance of
one. Layer order matters for build speed — copying requirements.txt and
installing dependencies before copying the rest of the source means Docker can
reuse that cached layer on rebuilds as long as dependencies haven't changed,
instead of reinstalling everything on every code change.

#### **Environment variables and secrets**

DATABASE\_URL, REDIS\_URL, API keys, and JWT secrets belong in environment
variables or a secret manager, never hardcoded or committed to git — including
in a config file that looks harmless because it's not literally named 'secrets.'

#### **CI/CD, the basic shape**

Push code, run tests, lint, build, deploy, monitor. The value isn't the tooling
(GitHub Actions, Vercel, whatever) — it's that every change goes through the
same automated gate before reaching production, so 'it worked on my machine'
stops being a valid deploy strategy.

### **INTERMEDIATE _— DevOps & Deployment_**

#### **Multi-stage builds and Compose**

```text

```

Multi-stage builds use one stage to compile/build and a second, leaner stage to
actually run the app, so build tools and intermediate artifacts don't bloat the
final image. Compose is for local development and simple deployments — running
FastAPI, Postgres, and Redis together with one command instead of managing three
separate processes by hand.

#### **Observability, the three pillars**

| Pillar  | Answers                                                      | Tooling examples                         |
| :------ | :----------------------------------------------------------- | :--------------------------------------- |
| Logs    | What happened, in detail, at a specific point in time        | Structured logging, aggregated centrally |
| Metrics | How is the system behaving in aggregate, over time           | Prometheus, Grafana                      |
| Traces  | What was the full path of a specific request across services | OpenTelemetry, Jaeger                    |

Sentry-style error tracking sits alongside all three — it's specifically for
catching and grouping exceptions with enough context (stack trace, request data,
user) to actually debug them, rather than discovering a bug from a user
complaint.

### **EXPERT _— DevOps & Deployment_**

#### **Containerizing the full stack, confidently**

Be ready to answer, concretely: how does the FastAPI container talk to Postgres
and Redis (service names on the Compose network, not localhost); how do
migrations run against a fresh database on first boot; how do you avoid baking
secrets into the image layers themselves (build args vs runtime env vars — build
args can leak into image history); what changes between a local Compose setup
and a production deployment (managed Postgres instead of a container with a
volume, secrets from a real secret manager, health checks wired to your
orchestrator).

#### **Zero-downtime deploys**

- Rolling deploys — bring up new instances, health-check them, then drain and
  remove old ones, so there's never a moment with zero healthy instances

- Database migrations have to be backward-compatible with the previous code
  version during the rollout window — old and new app versions are briefly
  running against the same schema simultaneously

- Feature flags decouple 'deploy the code' from 'turn on the behavior,' which
  makes rollback a config change instead of a redeploy

#### **Production readiness checklist**

- Health check endpoint that actually verifies downstream dependencies (DB,
  Redis, LLM API reachability), not just 'the process is running'

- Structured logging with request IDs that thread through to any background job
  triggered by that request, so a trace can follow the whole chain

- Alerting on the metrics that actually predict user-facing problems (error
  rate, p95 latency, queue depth), not just infrastructure vanity metrics (CPU
  usage in isolation tells you almost nothing about user experience)

- A documented, tested rollback procedure — not just a deploy procedure

- Secrets rotated on a schedule, with a process that doesn't require downtime

## **Appendix: Priority Resources**

Fifteen resources, in the order worth actually reading them. Everything else in
the earlier reading list is reference material — dip into it when a specific
topic above sends you looking for more depth.

| \#  | Resource                                        | Where                                       |
| :-- | :---------------------------------------------- | :------------------------------------------ |
| 1   | Python Official Tutorial                        | docs.python.org/3/tutorial                  |
| 2   | FastAPI Tutorial                                | fastapi.tiangolo.com/tutorial               |
| 3   | PostgreSQL Tutorial                             | postgresql.org/docs/current/tutorial.html   |
| 4   | PostgreSQL Full Docs                            | postgresql.org/docs/current                 |
| 5   | Redis Docs                                      | redis.io/docs/latest                        |
| 6   | Supabase Docs                                   | supabase.com/docs                           |
| 7   | Next.js Learn                                   | nextjs.org/learn                            |
| 8   | React Learn                                     | react.dev/learn                             |
| 9   | Hugging Face LLM Course                         | huggingface.co/learn/llm-course             |
| 10  | The Illustrated Transformer                     | jalammar.github.io/illustrated-transformer  |
| 11  | Attention Is All You Need                       | arxiv.org/abs/1706.03762                    |
| 12  | OpenAI Cookbook                                 | cookbook.openai.com                         |
| 13  | pgvector                                        | github.com/pgvector/pgvector                |
| 14  | System Design Primer                            | github.com/donnemartin/system-design-primer |
| 15  | Designing Data-Intensive Applications (2nd ed.) | O'Reilly                                    |

## **Appendix: Study Time Allocation**

A rough split for how to weight study time across the whole syllabus, not per
week:

| Area                     | Share of study time |
| :----------------------- | :------------------ |
| Python & FastAPI         | 25%                 |
| PostgreSQL & Redis       | 25%                 |
| Next.js & Supabase       | 15%                 |
| LLM / RAG / AI Agents    | 25%                 |
| System Design & Security | 10%                 |
