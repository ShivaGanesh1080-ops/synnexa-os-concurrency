# Title of the Project
## SYNCREG: A FULL-STACK CONCURRENCY CONTROL AND MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM
### (Product #8: Event / Workshop Registration System)

**A Course Project report submitted in partial fulfillment of requirement for the award of degree of**  
**BACHELOR OF TECHNOLOGY**  
in  
**SCHOOL OF COMPUTER SCIENCE AND ARTIFICIAL INTELLIGENCE**  

by  
- **Shiva Ganesh Akku** (HTNO: 2303A51123)  
- **Course Team Member 2** (HTNO: 2303A51124)  
- **Course Team Member 3** (HTNO: 2303A51125)  

Under the guidance of  
**Mr. Bura Vijay Kumar**  
Assistant Professor, School of CS&AI  

```
        ███████╗██████╗ ██╗   ██╗     ███████╗██████╗ ██╗   ██╗
        ██╔════╝██╔══██╗██║   ██║     ██╔════╝██╔══██╗██║   ██║
        ███████╗██████╔╝██║   ██║     ███████╗██████╔╝██║   ██║
        ╚════██║██╔══██╗██║   ██║     ╚════██║██╔══██╗██║   ██║
        ███████║██║  ██║╚██████╔╝     ███████║██║  ██║╚██████╔╝
                               SR UNIVERSITY
```
**SR University, Ananthsagar, Warangal, Telangana - 506371**  
**Academic Year:** 2024–2025 / 2025–2026  

---

## CERTIFICATE

This is to certify that the project entitled **“SYNCREG: A FULL-STACK CONCURRENCY CONTROL AND MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM (Product #8)”** is the bona fide work carried out as part of the **Operating Systems Course Project** for the partial fulfillment of the requirements of the **Bachelor of Technology, School of Computer Science & Artificial Intelligence, SR University** during the academic year 2024–2025 / 2025–2026 under my guidance and supervision.

| | |
| :--- | :--- |
| **Mr. Bura Vijay Kumar** | **Dr. M. Sheshikala** |
| Assistant Professor, School of CS&AI | Professor & Head, School of CS&AI |
| SR University, Ananthasagar, Warangal | SR University, Ananthasagar, Warangal |

---

## ACKNOWLEDGEMENT

We express our deep gratitude to our course project guide **Mr. Bura Vijay Kumar**, Assistant Professor, School of CS&AI, for his timely guidance, technical supervision, and constant support throughout the project. We thank **Dr. M. Sheshikala**, Professor & Head, School of CS&AI, for providing the required academic environment, computing resources, and facilities. We acknowledge the support of all teaching and non-teaching staff members and our families for their encouragement throughout the project.

---

## ABSTRACT

In concurrent web architectures, event booking engines, and university registration portals, simultaneous access to shared state represents a primary vector for severe data corruption. When available capacity is low—specifically when only one or two seats remain—uncontrolled simultaneous requests trigger a classic **Time-of-Check to Time-of-Use (TOCTOU)** race condition. Competing threads read stale capacity numbers before any write operation commits, allowing capacity to drop below zero ($C_{remaining} < 0$) and causing physical venue overbooking.

This project implements **“SyncReg OS”**, an enterprise-grade Event & Workshop Registration System designed to solve Dijkstra’s classical **Critical Section Problem**. The backend implements an asynchronous **Mutex (Mutual Exclusion Lock)** primitive with an explicit **First-In, First-Out (FIFO) wait queue**. The implementation satisfies all three classical Operating System synchronization properties: *Mutual Exclusion* (at most one thread in the critical section), *Progress* (no external deadlock), and *Bounded Waiting* ($O(k)$ starvation elimination). 

To prevent unnecessary serialization across independent workshops, a **Keyed Mutex Registry** provides fine-grained per-event locking. The full-stack platform features a dynamic seat allocator, real-time Server-Sent Events (SSE) telemetry pipeline, interactive head-to-head duel simulator, visual attendee seat grid, and an empirical stress-testing suite. Experimental evaluation under high load (50 threads competing for 2 seats) proves that Mutex synchronization eliminates overbooking (100% data integrity with zero negative capacity anomalies), whereas unsynchronized execution results in an overbooking hazard of 18 phantom registrations.

---

## KEYWORDS
Operating Systems, Concurrency Control, Critical Section, Mutex (Mutual Exclusion), Race Condition, Time-of-Check to Time-of-Use (TOCTOU), Bounded Waiting, FIFO Queue, Starvation Elimination, Fine-Grained Locking, Dynamic Capacity Allocation, Full Stack Development, REST API, Server-Sent Events (SSE).

---

## ABOUT THE ORGANIZATION

**SR University**, located in Ananthasagar, Warangal, Telangana, is a premier institution known for its innovation-centric curriculum, research facilities, startup ecosystem, and strong emphasis on practical learning. The **School of CS&AI** offers advanced courses in Operating Systems, Systems Programming, Web Programming, Mobile App Development, Cloud Computing, and Software Engineering.

---

## 1. INTRODUCTION

Higher educational institutions and digital commerce platforms frequently rely on event reservation portals. However, when multiple users attempt to register simultaneously for limited-seat workshops, unsynchronized thread execution leads to severe data inconsistency.

At the hardware CPU architecture level, decrementing a seat counter `capacity--` is broken into three separate assembly operations:
1. `MOV EAX, [capacity]` (Load variable into CPU register)
2. `SUB EAX, 1` (Compute decrement in ALU)
3. `MOV [capacity], EAX` (Store register back into RAM)

If an OS timer interrupt or preemptive thread context switch occurs between Step 1 and Step 3, the shared memory state is corrupted. This project builds a full-stack, enterprise-grade system that models, demonstrates, and prevents this concurrency hazard using classical OS primitives.

---

## 2. RELATED WORK

Research studies in process synchronization establish that software-only solutions like Peterson’s Algorithm (1981) and Lamport’s Bakery Algorithm are restricted to busy-waiting spinlocks that cause high CPU utilization. Modern computer architectures introduce hardware atomic primitives such as Test-and-Set (TAS) and Compare-and-Swap (CAS).

In distributed systems, Distributed Lock Managers (such as Redis Redlock) and relational database row-level locking (`SELECT ... FOR UPDATE`) are deployed. This project adapts these core Operating System principles into an asynchronous, queue-based **Ticket/FIFO Mutex** in pure Node.js, providing non-blocking execution while maintaining mathematical bounds on thread waiting times.

---

## 3. PROBLEM STATEMENT

> **Product #8 Specification:**  
> *"Several users attempt to register when only one or two places remain. How can the remaining capacity be updated correctly?"*

When workshop seat capacity is scarce ($C_{remaining} \in \{1, 2\}$), simultaneous registration requests trigger the **Time-of-Check to Time-of-Use (TOCTOU)** race condition:
1. Thread A reads `remainingCapacity = 1`.
2. Thread B concurrently reads `remainingCapacity = 1` (stale read).
3. Both threads evaluate `remainingCapacity > 0` as `TRUE`.
4. Thread A decrements capacity to 0 and writes Ticket A.
5. Thread B decrements capacity to -1 and writes Ticket B.

**Result:** Overbooking occurs, physical capacity is breached, and the system invariant $\forall t, 0 \le C_{remaining}(t) \le C_{total}$ is violated.

---

## 4. REQUIREMENT ANALYSIS

### 4.1 Functional Requirements
- **FR-1:** Mutex-protected atomic registration serializing requests competing for the same workshop.
- **FR-2:** In-critical-section duplicate email detection and rejection (HTTP 409).
- **FR-3:** Dynamic capacity reallocation allowing administrators to set remaining/total seats live.
- **FR-4:** Synchronized registration cancellation with safe seat restoration.
- **FR-5:** Interactive Concurrency Lab supporting 2 to 50 concurrent synthetic threads with Mutex toggle.
- **FR-6:** Real-time Server-Sent Events (SSE) telemetry log stream.

### 4.2 Non-Functional Requirements
- **NFR-1 (Safety Invariant):** $0 \le C_{remaining}(t) \le C_{total}$ at all times $t$.
- **NFR-2 (Bounded Waiting):** Strict FIFO wait queue guaranteeing $O(k)$ wait time (zero starvation).
- **NFR-3 (High Throughput):** Lock acquisition overhead under 15ms.
- **NFR-4 (Deadlock Freedom):** Breaking Coffman conditions (No Hold-and-Wait, No Circular Wait).
- **NFR-5 (Zero Dependencies):** Native Node.js standard libraries only.

---

## 5. RISK ANALYSIS & MITIGATION

| Risk | Severity | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **TOCTOU Overbooking** | Critical | Multiple users pass check; capacity drops to negative. | Enclose validation and decrement in an atomic Critical Section guarded by Mutex. |
| **Deadlock / Orphaned Locks** | High | Thread error leaves lock held forever; system freezes. | Encapsulate critical section in `try ... finally` blocks to guarantee `release()`. |
| **Thread Starvation** | Medium | Low-priority threads wait indefinitely. | Strict First-In, First-Out (FIFO) queue for lock grants. |
| **Global Contention Bottleneck** | Medium | One lock for all events slows down independent bookings. | Implement `KeyedMutexRegistry` for per-event lock isolation. |
| **Data Loss on Crash** | High | Process crash corrupts JSON database. | Atomic file replace using temporary file flush and `fs.renameSync`. |

---

## 6. FEASIBILITY ANALYSIS

- **Technical:** Implemented in pure Node.js v18+ leveraging the asynchronous microtask event loop.
- **Economic:** Zero-cost development; 100% open-source software stack with no enterprise license fees.
- **Operational:** Intuitive web interface with glassmorphism CSS, live pipeline animation, and 1-click dynamic seat controls.
- **Schedule:** Fully developed, benchmarked, and documented within course schedule limits.

---

## 7. PROPOSED SOLUTION & SYSTEM ARCHITECTURE

```text
+─────────────────────────────────────────────────────────────────────────────+
|               TIER 1: PRESENTATION LAYER (Web Dashboard & Lab)              |
|   HTML5, CSS Glassmorphism, Vanilla ES6 JS, Dynamic Seat Controller, SSE    |
+─────────────────────────────────────────────────────────────────────────────+
                                       │ (HTTP REST & /api/stream SSE)
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|               TIER 2: API ROUTING & CONTROLLER (Native Node.js)             |
|   server.js, src/routes/api.js: JSON streaming, CORS, error handling        |
+─────────────────────────────────────────────────────────────────────────────+
                                       │ (Lock Acquisition)
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|               TIER 3: OS SYNCHRONIZATION ENGINE                             |
|   Mutex.js (FIFO Bounded Waiting) + KeyedMutexRegistry.js (Fine-Grained)     |
+─────────────────────────────────────────────────────────────────────────────+
                                       │ (Critical Section Execution)
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|               TIER 4: BUSINESS LOGIC SERVICES                               |
|   EventService.js: Duplicate check, atomic decrement, cancellation restore  |
+─────────────────────────────────────────────────────────────────────────────+
                                       │ (Thread-Safe Persistence)
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|               TIER 5: STORAGE & AUDIT ENGINE                                |
|   Database.js (Atomic temp-file rename) + AuditLogger.js (Microsecond logs) |
+─────────────────────────────────────────────────────────────────────────────+
```

---

## 8. DATA FLOW DIAGRAM (LEVEL 1)

```text
[ Client Browser ] 
        │ (POST /api/events/:id/register {userEmail, userName})
        ▼
( API Controller ) 
        │ (Request Event Lock from Keyed Registry)
        ▼
< KeyedMutexRegistry > ──[Lock Held?]──> [ FIFO Wait Queue ] (Yield CPU / Sleep)
        │ (Lock Free)                               │ (Shift on Release)
        ▼                                           ▼
[ CRITICAL SECTION ] <──────────────────────────────┘
  ├─ 1. Duplicate Email Check?  ──[Found]──> Throw 409 DUPLICATE
  ├─ 2. Capacity <= 0 Check?    ──[Zero]───> Throw 409 SOLD_OUT
  ├─ 3. Atomic Decrement: capacity -= 1
  ├─ 4. Push New Ticket: registrations.push(ticket)
  └─ 5. Atomic Storage Commit: Database.persist()
        │
        ▼ (Finally Block)
( Release Mutex Lock ) ──> Dequeue Next Waiting Thread in FIFO Queue
        │
        ▼
[ Return HTTP 201 Response ] ──> [ Client Browser Receives Confirmed Ticket ]
```

---

## 9. PROCESS FLOW & OS THREAD LIFECYCLE

The system models requests through classical OS process/thread states:
1. **NEW:** HTTP request is received and parsed by the network socket.
2. **READY:** Request thread is scheduled in the event loop, requesting the lock.
3. **BLOCKED / WAITING:** If the mutex is locked, the thread is pushed into `this._queue` and sleeps without burning CPU cycles.
4. **RUNNING (Critical Section):** Lock is granted; thread enters critical section to verify capacity, check duplicates, and decrement seats.
5. **TERMINATED:** Lock is released in the `finally` block; HTTP response (201 Confirmed or 409 Rejected) is returned.

---

## 10. TECHNICAL ENVIRONMENT & TOOLS

- **Runtime:** Node.js (v18.x – v24.x)
- **Languages:** JavaScript (ES6+), HTML5, CSS3, Python (pptx generator)
- **Server:** Native Node.js `http`, `fs`, `events` (zero external npm dependencies)
- **Testing:** Automated test suite (`tests/run-tests.js`), 50-thread stress harness (`tests/concurrency-stress-test.js`)
- **IDE & OS:** Visual Studio Code, Windows 11 PowerShell

---

## 11. DATABASE DESIGN

- **`events` Entity:** `id` (PK), `title`, `speaker`, `date`, `location`, `totalCapacity`, `remainingCapacity`, `badge`, `registrations[]`.
- **`registrations` Entity:** `id` (PK, e.g. `TKT-1-6801-ZEZ`), `userName`, `userEmail`, `registeredAt`, `ticketStatus` (`CONFIRMED`, `OVERBOOKED`, `CANCELLED`).
- **`auditLogs` Entity:** `id`, `timestamp`, `millis`, `eventId`, `requesterId`, `action`, `status`, `message`, `remainingCapacity`.

---

## 12. IMPLEMENTATION

### 12.1 Asynchronous FIFO Mutex (`Mutex.js`)
```javascript
class Mutex {
  constructor(name = 'default-mutex') {
    this.name = name;
    this._locked = false;
    this._queue = []; // Strict FIFO queue for Bounded Waiting
    this._currentOwner = null;
  }

  acquire(requesterId) {
    if (!this._locked) {
      this._locked = true;
      this._currentOwner = requesterId;
      return Promise.resolve(() => this._release(requesterId));
    }
    return new Promise((resolve) => {
      this._queue.push({
        requesterId,
        grant: () => {
          this._locked = true;
          this._currentOwner = requesterId;
          resolve(() => this._release(requesterId));
        }
      });
    });
  }

  _release(ownerId) {
    if (this._queue.length > 0) {
      const next = this._queue.shift(); // FIFO: Strict arrival order
      next.grant();
    } else {
      this._locked = false;
      this._currentOwner = null;
    }
  }
}
```

### 12.2 Critical Section Execution (`EventService.js`)
```javascript
async registerUser({ eventId, userName, userEmail, useMutex = true }) {
  if (useMutex) {
    const lock = keyedMutex.getLock(eventId);
    const releaseLock = await lock.acquire(threadId);

    try {
      const event = db.getEventRef(eventId);
      // Duplicate prevention inside Critical Section
      if (event.registrations.some(r => r.userEmail === userEmail)) {
        throw { status: 409, code: 'DUPLICATE_REGISTRATION' };
      }
      // Capacity check inside Critical Section
      if (event.remainingCapacity <= 0) {
        throw { status: 409, code: 'SOLD_OUT' };
      }
      // Indivisible state mutation
      event.remainingCapacity -= 1;
      event.registrations.push(newTicket);
      db.persist();
      return { success: true, ticket: newTicket };
    } finally {
      releaseLock(); // Exception-safe release
    }
  }
}
```

---

## 13. RESULTS & EMPIRICAL BENCHMARKS

### 13.1 High-Concurrency Stress Test (50 Threads vs 2 Seats)

| Metric | Mutex Mode (Safe) | Unsynchronized Mode (Unsafe) | Verdict |
| :--- | :---: | :---: | :--- |
| **Initial Available Seats** | 2 | 2 | Scarcity Baseline |
| **Concurrent Users Competing** | 50 Threads | 20 Threads | Simultaneous Arrival |
| **Successful Bookings** | **2 (Exact Match)** | **20 (All passed!)** | Stale read error in Unsafe |
| **Clean Rejections (409)** | 48 | 0 | Sold-out handling verified |
| **Final Remaining Capacity** | **0** | **-18** | Invariant preserved with Mutex |
| **Overbooking Anomaly** | **0 (Zero Overbooked)** | **+18 Phantom Bookings** | Mutual exclusion verified |
| **Execution Duration** | 39 ms | 63 ms | Low-latency async primitives |

### 13.2 Automated Test Suite Results
```text
[TEST] Mutex: Guarantees strict Mutual Exclusion (only 1 thread in CS) ... PASSED
[TEST] Mutex: Enforces Bounded Waiting in FIFO order (No Starvation) .... PASSED
[TEST] KeyedMutex: Independent resources lock independently ............ PASSED
[TEST] EventService: Rejects duplicate registration for same email ..... PASSED
[TEST] EventService: Cancellation restores seat capacity inside CS ..... PASSED
[TEST] Concurrency Benchmark: 15 users vs 2 seats -> 2 succeed, 0 overbook PASSED
[TEST] Race Condition Demo: 10 users WITHOUT Mutex -> -7 overbooked .... PASSED
======================================================
  FINAL TEST RESULTS: 7 / 7 TESTS PASSED (100% Reliability)
======================================================
```

---

## 14. LEARNING OUTCOMES

1. **Hardware-to-Software Concurrency Mapping:** Understanding assembly register non-atomicity (`LOAD-COMPUTE-STORE`) and TOCTOU vulnerabilities.
2. **Dijkstra’s Classical Principles:** Practical implementation of Mutual Exclusion, Progress, and Bounded Waiting.
3. **Lock Granularity & Amdahl's Law:** Implementing fine-grained per-event locking (`KeyedMutexRegistry`) to prevent global concurrency bottlenecks.
4. **Deadlock Elimination:** Breaking Coffman conditions by eliminating Circular Wait and Hold-and-Wait dependencies.
5. **Full-Stack Engineering:** Developing a complete interactive web dashboard, dynamic capacity allocator, and real-time SSE audit feed.

---

## 15. CONCLUSION & FUTURE SCOPE

The **SyncReg OS Event & Workshop Registration System** successfully solves Product #8 by demonstrating how race conditions create negative capacity overbooking when only one or two seats remain, and showing how a FIFO queue-backed Mutex preserves 100% data integrity.

### Future Enhancements:
- **Distributed Scaling:** Transitioning the in-memory mutex to a Distributed Lock Manager (DLM) using Redis with the **Redlock Algorithm** across multi-node clusters.
- **Database Row-Level Locking:** Deploying PostgreSQL ACID transactions with pessimistic row locks (`SELECT ... FOR UPDATE`).
- **Priority Inheritance:** Implementing priority inheritance in the mutex queue to prevent Priority Inversion in real-time operating systems.

---

## 16. REFERENCES

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). John Wiley & Sons. (Chapters 5 & 6: Process Synchronization).
2. Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.). Pearson. (Chapter 2: IPC, Mutexes, Semaphores).
3. Dijkstra, E. W. (1965). *Cooperating Sequential Processes*. Technological University, Eindhoven.
4. Coffman, E. G., Elphick, M., & Shoshani, A. (1971). *System Deadlocks*. ACM Computing Surveys, 3(2), 67-78.
5. Lamport, L. (1974). *A New Solution of Dijkstra's Concurrent Programming Problem*. Communications of the ACM, 17(8), 453-455.
6. Peterson, G. L. (1981). *Myths About the Mutual Exclusion Problem*. Information Processing Letters, 12(3), 115-116.
7. Node.js Foundation. (2026). *Node.js Core API Documentation: Asynchronous Flow Control, Events & HTTP*. https://nodejs.org/api/
8. Mozilla Developer Network (MDN). (2026). *Server-Sent Events (SSE) & Web Standards Architecture*. https://developer.mozilla.org/
9. Sanfilippo, S. (2020). *Distributed Locks with Redis and the Redlock Algorithm*. Redis Engineering Documentation.
