# SyncReg OS: Event & Workshop Registration System
> **Product #8 • Operating Systems Concurrency Project**  
> **Core OS Concepts:** Critical Section, Mutex (Mutual Exclusion Lock), Concurrency Control, Race Condition Mitigation

---

## 📌 Problem Statement & Core Scenario

> **"Several users attempt to register when only one or two places remain. How can the remaining capacity be updated correctly?"**

In event registration, e-commerce flash sales, and ticket booking systems, shared state—specifically the **remaining seat capacity**—is concurrently accessed and updated by multiple threads or distributed client requests.

### The Race Condition (Without Mutex / Unsynchronized)
When capacity is low (e.g., only 1 or 2 seats remaining), and multiple users click "Register" at the exact same millisecond, a classic **Check-Then-Act (TOCTOU: Time of Check to Time of Use)** race condition occurs:

```text
Thread 1 (User A)                         Thread 2 (User B)
-----------------                         -----------------
1. READ remainingCapacity = 1
                                          2. READ remainingCapacity = 1 (Stale read!)
3. CHECK capacity > 0 (TRUE)
                                          4. CHECK capacity > 0 (TRUE!)
5. DECREMENT capacity: 1 -> 0
6. WRITE ticket for User A
                                          7. DECREMENT capacity: 0 -> -1  <-- OVERBOOKING!
                                          8. WRITE ticket for User B      <-- DATA HAZARD!
```

**Result:**
- Both users receive booking confirmations.
- Remaining capacity drops below zero ($C_{remaining} = -1$).
- Physical venue / workshop capacity is violated.

---

## 🛡️ The Operating System Solution

To prevent race conditions, the check, decrement, duplicate validation, and ticket assignment must be executed as an **atomic, indivisible operation inside a Critical Section**, protected by an **OS Mutex (Mutual Exclusion Lock)**.

### Classical OS Critical Section Properties Satisfied:
1. **Mutual Exclusion:** Only one thread can enter the critical section for a specific event at any given moment.
2. **Progress:** If the critical section is unoccupied, any waiting thread wishing to enter can proceed immediately without external deadlock.
3. **Bounded Waiting:** A First-Come, First-Served (FIFO) wait queue ensures every competing thread has a deterministic upper bound on wait time, preventing thread starvation.

```text
Thread 1 (User A)                         Thread 2 (User B)
-----------------                         -----------------
1. ACQUIRE MutexLock                      1. REQUEST MutexLock -> BUSY
   [ENTERS CRITICAL SECTION]                 [ENQUEUED IN FIFO WAIT QUEUE]
2. READ capacity = 1                      |
3. CHECK no duplicate                     | (Thread 2 blocked / sleeping)
4. DECREMENT capacity: 1 -> 0             |
5. COMMIT ticket for User A               |
6. RELEASE MutexLock                      |
   [EXITS CRITICAL SECTION]               2. LOCK GRANTED -> Thread 2 Awoken
                                             [ENTERS CRITICAL SECTION]
                                          3. READ capacity = 0
                                          4. CHECK capacity > 0 (FALSE!)
                                          5. REJECT: "Event Sold Out (409 Conflict)"
                                          6. RELEASE MutexLock
                                             [EXITS CRITICAL SECTION]
```

**System Invariant Maintained:**
$$\forall t, \quad 0 \le C_{remaining}(t) \le C_{total}$$
$$C_{remaining}(t) + N_{registered}(t) = C_{total}$$

---

## 🌟 Unique Implementation Features

1. **Event List & Dynamic Capacity Tracking:** Live real-time visualization of total seats, remaining seats, percentage filled, and occupancy badges.
2. **Mutex-Synchronized Registration:** High-throughput async Mutex primitive with FIFO bounded waiting.
3. **Duplicate-Registration Prevention:** Atomic inspection of participant email addresses inside the critical section. Duplicate requests fail immediately with `409 DUPLICATE_REGISTRATION`.
4. **Cancellation with Seat Restoration:** Safe release of registrations that acquires the mutex and increments remaining capacity back up to the maximum pool size.
5. **Interactive Concurrency Lab:** Live dashboard UI allowing users and evaluators to trigger 2 to 50 concurrent requests simultaneously to compare **Mutex Protected Mode** vs **Unsafe Mode (Race Condition)** in real time.
6. **Live Kernel Audit Feed:** Millisecond-precision telemetry stream showing lock requests, acquisitions, critical section entries, and releases.
7. **Fine-Grained Resource Locking:** `KeyedMutexRegistry` locks per event ID, ensuring concurrent registrations for Event A do not block Event B.

---

## 🚀 Quick Start Guide

### Prerequisites
- Node.js (v18, v20, v22, or v24)
- No external npm packages required (Built using pure Node.js standard libraries for zero-dependency execution and maximum portability).

### 1. Start the Production Server
```bash
# Option A: Using NPM
npm start

# Option B: Direct Node invocation
node server.js
```
The server will start at: **`http://localhost:3000`**

Open your web browser and navigate to:
- **Web Dashboard & Concurrency Lab:** `http://localhost:3000`
- **Interactive Simulation:** `http://localhost:3000/#lab`
- **Health Check:** `http://localhost:3000/api/health`

---

## 🧪 Automated Testing Suite

The system includes automated unit, integration, and high-concurrency stress test suites:

### Run Core OS & Unit Tests
```bash
npm test
```
**Tests Executed:**
- `[PASS]` Mutex Mutual Exclusion (proves max concurrent threads in critical section $\equiv 1$)
- `[PASS]` Mutex Bounded Waiting (proves strict FIFO execution order)
- `[PASS]` Keyed Mutex Isolation (proves independent event locks do not block each other)
- `[PASS]` Duplicate Registration Prevention (proves same email is rejected)
- `[PASS]` Cancellation Capacity Restoration (proves seat is restored safely)
- `[PASS]` Concurrency Benchmark with Mutex (15 users vs 2 seats -> exactly 2 succeed, 0 overbooked)
- `[PASS]` Race Hazard Demo without Mutex (demonstrates negative capacity anomaly)

### Run High-Load Stress Test (50 Threads vs 2 Seats)
```bash
npm run test:concurrency
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Returns service health status and timestamp |
| `GET` | `/api/events` | Lists all events with live capacity and mutex status |
| `GET` | `/api/events/:id` | Returns single event and registered attendees |
| `POST` | `/api/events` | Creates a new event / workshop |
| `POST` | `/api/events/:id/register` | Registers attendee (supports `useMutex: true \| false`) |
| `POST` | `/api/events/:id/cancel` | Cancels registration and restores seat |
| `POST` | `/api/events/:id/simulate` | Triggers $N$ concurrent registrations simultaneously |
| `POST` | `/api/events/:id/reset` | Resets event capacity back to baseline |
| `POST` | `/api/reset-all` | Resets all events and audit logs |
| `GET` | `/api/logs` | Real-time audit log stream |
| `GET` | `/api/mutex/stats` | Telemetry of active locks, queues, and hold times |

---

## 📂 Project Architecture

```text
event-registration-mutex-system/
├── package.json                   # Project metadata and run scripts
├── server.js                      # High-performance HTTP server & router
├── src/
│   ├── core/
│   │   ├── Mutex.js               # Asynchronous Mutex with FIFO bounded waiting
│   │   └── KeyedMutexRegistry.js  # Fine-grained per-event lock manager
│   ├── storage/
│   │   └── Database.js            # Thread-safe persistent storage engine
│   ├── services/
│   │   ├── EventService.js        # Business logic for registration & concurrency
│   │   └── AuditLogger.js         # Real-time state transition telemetry
│   └── routes/
│       └── api.js                 # REST API endpoints
├── public/
│   ├── index.html                 # Modern glassmorphism web dashboard
│   ├── style.css                  # Dark-mode styling, pipeline visualizer & animations
│   └── app.js                     # Client application & concurrency lab controller
├── tests/
│   ├── run-tests.js               # Comprehensive OS unit & integration test suite
│   └── concurrency-stress-test.js # High-throughput flash-sale benchmark (50 threads)
└── data/
    └── database.json              # File-backed persistence store
```

---

## 🎓 Academic Presentation Summary

| Attribute | Specification |
| :--- | :--- |
| **Product** | Event / Workshop Registration System (Product #8) |
| **Main OS Concept** | Critical Section, Mutex (Mutual Exclusion) |
| **Main Problem Solved** | Multiple users competing for the final few registration places |
| **Vulnerability Solved** | Check-Then-Act Race Condition / TOCTOU Overbooking |
| **Key Invariant** | Capacity never falls below zero ($C_{rem} \ge 0$) |
| **Synchronization Primitive** | FIFO Queue Semaphore / Ticket Mutex (`AsyncMutex`) |
| **Lock Granularity** | Fine-grained per-event ID |
| **Unique Features** | Event list, Registration, Cancellation, Capacity tracking, Duplicate prevention |
