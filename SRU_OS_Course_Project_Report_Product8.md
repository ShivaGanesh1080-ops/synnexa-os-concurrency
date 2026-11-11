# Title of the Project
## SYNNEXA: A FULL-STACK CONCURRENCY CONTROL AND MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM
### (Product #8: Event / Workshop Registration System)

**A Course Project report submitted in partial fulfillment of requirement for the award of degree of**  
**BACHELOR OF TECHNOLOGY**  
in  
**SCHOOL OF COMPUTER SCIENCE AND ARTIFICIAL INTELLIGENCE**  

by  
1. **Ch. Naveen Reddy** (HTNO: 2503A51108) — Systems Core & Concurrency  
2. **K. Shiva Saketh** (HTNO: 2503A51109) — Payment Gateway Integration  
3. **A. Shiva Ganesh** (HTNO: 2503A51110) — **Team Leader & Full-Stack Architect**  
4. **V. Saicharan** (HTNO: 2503A51111) — Database & State Management  
5. **T. Geethika** (HTNO: 2503A1112) — UI/UX & Editorial Layouts  
6. **G. Vishwas** (HTNO: 2503A51113) — Benchmarking & QA Testing  

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
**SR University, Ananthasagar, Warangal, Telangana - 506371**  
**Academic Year:** 2025–2026  

---

## CERTIFICATE

This is to certify that the project entitled **“SYNNEXA: A FULL-STACK CONCURRENCY CONTROL AND MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM (Product #8)”** is the bona fide work carried out as part of the **Operating Systems Course Project** for the partial fulfillment of the requirements of the **Bachelor of Technology, School of Computer Science & Artificial Intelligence, SR University** during the academic year 2025–2026 under my guidance and supervision by:

- **Ch. Naveen Reddy** (2503A51108)
- **K. Shiva Saketh** (2503A51109)
- **A. Shiva Ganesh** (2503A51110) — Team Leader
- **V. Saicharan** (2503A51111)
- **T. Geethika** (2503A1112)
- **G. Vishwas** (2503A51113)

| | |
| :--- | :--- |
| **Mr. Bura Vijay Kumar** | **Dr. M. Sheshikala** |
| Assistant Professor, School of CS&AI | Professor & Head, School of CS&AI |
| SR University, Ananthasagar, Warangal | SR University, Ananthasagar, Warangal |

---

## ACKNOWLEDGEMENT

We express our deep gratitude to our course project guide **Mr. Bura Vijay Kumar**, Assistant Professor, School of CS&AI, for his technical guidance, architectural review, and constant encouragement throughout the design and benchmarking of this system. We thank **Dr. M. Sheshikala**, Professor & Head, School of CS&AI, for providing the required computational laboratory resources and supportive academic environment. We also acknowledge our peers, faculty members, and families for their continuous support.

---

## ABSTRACT

In modern concurrent web architectures, high-demand ticketing platforms, and university registration portals, simultaneous access to shared, finite resources represents a fundamental vulnerability for data corruption. When available capacity is low—specifically when only one seat or quota place remains—uncontrolled simultaneous requests trigger a classic **Time-of-Check to Time-of-Use (TOCTOU)** race condition. Competing threads read stale capacity numbers before any write operation commits, allowing capacity to drop below zero ($C_{remaining} < 0$), minting duplicate tickets for the same physical seat and causing venue overselling.

This project implements **“SYNNEXA”**, an enterprise-grade high-concurrency event management and Tatkal squad reservation platform designed to solve Dijkstra’s classical **Critical Section Problem**. The backend implements an asynchronous **Mutex (Mutual Exclusion Lock)** primitive with an explicit **First-In, First-Out (FIFO) wait queue**. The implementation mathematically satisfies all three classical Operating System synchronization requirements:
1. **Mutual Exclusion:** At most one thread executes inside the critical section at any given time.
2. **Progress:** If no thread is in the critical section, selection of the next thread cannot be postponed indefinitely.
3. **Bounded Waiting:** A bound exists on the number of times other threads can enter the critical section after a request has been made ($O(k)$ starvation elimination).

To prevent cross-resource blocking, a **Keyed Mutex Registry** provides fine-grained per-event lock isolation. The full-stack platform features an editorial luxury user interface, official **Razorpay Standard Checkout SDK** integration, printable physical boarding passes (`window.print()`), a unified **Organizer Admin Console**, and a live **2-Device Concurrency Test Station**. Live physical demonstration across two separate hardware devices (Teacher on Laptop vs. Friend on Mobile) proves that with Mutex disabled, both devices claim the single remaining seat ($C_{remaining} = -1$), whereas with Mutex enabled, the first transaction commits atomically and the second is safely serialized and rejected with HTTP 409 Sold Out.

---

## KEYWORDS
Operating Systems, Concurrency Control, Critical Section, Mutex (Mutual Exclusion), Race Condition, Time-of-Check to Time-of-Use (TOCTOU), Bounded Waiting, FIFO Queue, Starvation Elimination, Keyed Mutex Registry, Fine-Grained Locking, Razorpay Standard Checkout SDK, Printable Boarding Pass, Full-Stack Architecture, Node.js Native HTTP.

---

## ABOUT THE INSTITUTION

**SR University**, located in Ananthasagar, Warangal, Telangana, is a premier state-private university renowned for its innovation-driven curriculum, industry partnerships, and state-of-the-art computational infrastructure. The **School of Computer Science & Artificial Intelligence (CS&AI)** delivers rigorous coursework in Operating Systems, Distributed Systems, Systems Programming, Computer Networks, and Cloud Architecture.

---

## 1. INTRODUCTION

Digital ticketing systems, university symposium portals, and railway Tatkal reservation platforms experience intense traffic bursts when registration windows open. When hundreds of users compete for limited remaining seats, unsynchronized server threads produce race hazard anomalies.

At the underlying CPU architecture level, decrementing a shared integer variable `capacity--` is non-atomic and executes across three discrete machine cycles:
1. `MOV EAX, [capacity]` (Load variable from RAM into CPU register)
2. `SUB EAX, 1` (Perform subtraction in ALU)
3. `MOV [capacity], EAX` (Store modified register value back into RAM)

If an asynchronous context switch, network I/O delay, or payment gateway verification occurs between Step 1 and Step 3, concurrent threads read identical stale capacity values. This project designs and evaluates **SYNNEXA**, a zero-dependency full-stack system proving that OS synchronization primitives eliminate overselling while delivering predictable microsecond latency.

---

## 2. PROBLEM STATEMENT & THE TOCTOU VULNERABILITY

> **Product #8 Specification:**  
> *"Several users attempt to register when only one or two places remain. How can the remaining capacity be updated correctly?"*

Consider an event with $C_{remaining} = 1$:
- **User A (Teacher on Laptop)** clicks "Book Team Pass" at timestamp $t_0$.
- **User B (Friend on Mobile)** clicks "Book Team Pass" at timestamp $t_0 + 200\text{ms}$.

### Unsynchronized Execution (Mutex OFF — Race Hazard):
```text
Teacher Thread (T1)                 Friend Thread (T2)                 Shared State (DB)
───────────────────                 ──────────────────                 ─────────────────
Reads C_remaining = 1                                                  C_remaining = 1
Evaluates (1 > 0) -> TRUE                                              C_remaining = 1
Begins payment delay (await)        Reads C_remaining = 1 (STALE!)     C_remaining = 1
                                    Evaluates (1 > 0) -> TRUE          C_remaining = 1
                                    Begins payment delay (await)       C_remaining = 1
Finishes payment -> writes ticket                                      C_remaining = 0
                                    Finishes payment -> writes ticket  C_remaining = -1  <-- OVERSOLD!
Returns: CONFIRMED (TKT-01)         Returns: CONFIRMED (TKT-02)
```
**Anomaly:** Two confirmed tickets are issued for a single physical seat ($C_{remaining} = -1$). The system invariant $\forall t, 0 \le C_{remaining}(t) \le C_{total}$ is violated.

### Synchronized Execution (Mutex ON — ACID Critical Section):
```text
Teacher Thread (T1)                 Friend Thread (T2)                 Shared State (DB)
───────────────────                 ──────────────────                 ─────────────────
Acquires Mutex Lock -> GRANTED                                         Lock: LOCKED (T1)
Enters Critical Section                                                C_remaining = 1
Reads C_remaining = 1               Requests Mutex Lock -> BLOCKED     Queue: [ T2 ]
Decrements: C_remaining = 0                                            C_remaining = 0
Writes Ticket TKT-01                                                   Tickets: 1
Releases Mutex Lock ──────────────> Dequeues T2 -> GRANTED             Lock: LOCKED (T2)
Returns: 200 CONFIRMED              Enters Critical Section            C_remaining = 0
                                    Reads C_remaining = 0              C_remaining = 0
                                    Evaluates (0 <= 0) -> REJECT!      C_remaining = 0
                                    Releases Mutex Lock                Lock: UNLOCKED
                                    Returns: 409 SOLD OUT
```
**Outcome:** Ticket #1 is safely issued; Thread #2 is rejected with a polite "Sold Out" response. Zero negative capacity anomalies occur.

---

## 3. MATHEMATICAL SPECIFICATION OF THE SYNCHRONIZATION MODEL

Let $\mathcal{T} = \{T_1, T_2, \dots, T_n\}$ denote the set of concurrent reservation threads arriving at the server.

### 3.1 Mutual Exclusion Property
At any wall-clock time $t$, let $\mathcal{C}(t) \subseteq \mathcal{T}$ be the set of threads executing inside the critical section. The Mutex primitive guarantees:
$$\forall t, \quad |\mathcal{C}(t)| \le 1$$

### 3.2 Bounded Waiting & Starvation Elimination
Let thread $T_i$ request the lock at timestamp $t_{req}(T_i)$. Let $W(T_i)$ be the number of other threads granted lock entry before $T_i$. Under our FIFO queue discipline:
$$W(T_i) = |\{T_j \in \mathcal{Q} : t_{req}(T_j) < t_{req}(T_i)\}| = k < \infty$$
Thus, wait time is strictly bounded by $O(k \cdot \Delta t_{CS})$, guaranteeing zero thread starvation.

### 3.3 System Invariant Preservation
Let $R_k(t) \in \{0, 1\}$ denote whether ticket $k$ has been issued by time $t$. The platform strictly enforces:
$$C_{remaining}(t) = C_{total} - \sum_{k=1}^{M} R_k(t) \ge 0, \quad \forall t \ge 0$$

---

## 4. SYSTEM ARCHITECTURE & COMPONENT TOPOLOGY

```text
+─────────────────────────────────────────────────────────────────────────────────+
|               TIER 1: CLIENT PRESENTATION & RESPONSIVE INTERFACE                |
|   • SYNNEXA Events Participant Portal (/)                                       |
|   • Razorpay Standard Checkout SDK Modal Integration                            |
|   • Printable Boarding Pass Engine (window.print() with Print CSS)              |
|   • Unified Organizer & Platform Command Console (/admin)                       |
|   • Live 2-Device Concurrency Test Station (Teacher vs. Friend)                 |
+─────────────────────────────────────────────────────────────────────────────────+
                                       │ HTTP/1.1 REST & Event Polling
                                       ▼
+─────────────────────────────────────────────────────────────────────────────────+
|               TIER 2: NATIVE NODE.JS API & ROUTING ENGINE (server.js)           |
|   • Zero-bloat native HTTP server (no Express, no external framework)           |
|   • Microtask event-loop non-blocking I/O                                       |
|   • PowerPoint (.pptx) direct presentation export stream                        |
+─────────────────────────────────────────────────────────────────────────────────+
                                       │ Lock Acquisition Request
                                       ▼
+─────────────────────────────────────────────────────────────────────────────────+
|               TIER 3: OPERATING SYSTEMS CONCURRENCY KERNEL                      |
|   • Mutex.js: Asynchronous Mutual Exclusion Primitive                          |
|   • KeyedMutexRegistry.js: Fine-grained per-event lock multiplexing             |
|   • FIFO Bounded Waiting queue (array-backed ticket queue)                      |
+─────────────────────────────────────────────────────────────────────────────────+
                                       │ Serialized Critical Section
                                       ▼
+─────────────────────────────────────────────────────────────────────────────────+
|               TIER 4: TATKAL BOOKING SERVICE (BookingService.js)                |
|   • Atomic check-and-decrement inventory validation                             |
|   • Multi-device TOCTOU race condition simulator (Mutex ON vs. Mutex OFF)       |
|   • Razorpay test payment verification & cryptographic ticket code minting      |
+─────────────────────────────────────────────────────────────────────────────────+
                                       │ Atomic Flush
                                       ▼
+─────────────────────────────────────────────────────────────────────────────────+
|               TIER 5: ACID STORAGE & AUDIT LEDGER (Database.js)                 |
|   • Thread-safe JSON persistence with atomic fs.renameSync temp-flush           |
|   • Microsecond critical section audit trail (timestamp, lock state, latency)   |
+─────────────────────────────────────────────────────────────────────────────────+
```

---

## 5. CORE IMPLEMENTATION HIGHLIGHTS

### 5.1 Asynchronous FIFO Mutex Primitive (`src/core/Mutex.js`)
```javascript
class Mutex {
  constructor(name = 'default-mutex') {
    this.name = name;
    this._locked = false;
    this._queue = []; // Strict FIFO queue ensuring Bounded Waiting
    this._currentOwner = null;
    this._lockAcquireTimestamp = 0;
  }

  acquire(threadId = 'anonymous', metadata = null) {
    if (!this._locked) {
      this._locked = true;
      this._currentOwner = threadId;
      this._lockAcquireTimestamp = Date.now();
      return Promise.resolve(() => this._release(threadId));
    }

    return new Promise((resolve) => {
      this._queue.push({
        threadId,
        metadata,
        timestamp: Date.now(),
        grant: () => {
          this._locked = true;
          this._currentOwner = threadId;
          this._lockAcquireTimestamp = Date.now();
          resolve(() => this._release(threadId));
        }
      });
    });
  }

  _release(threadId) {
    if (this._queue.length > 0) {
      const nextThread = this._queue.shift(); // FIFO order: Zero Starvation
      nextThread.grant();
    } else {
      this._locked = false;
      this._currentOwner = null;
    }
  }
}
```

### 5.2 Keyed Mutex Registry for Fine-Grained Locking (`src/core/KeyedMutexRegistry.js`)
To avoid Amdahl’s bottleneck where independent events lock each other out, the system implements a dictionary-backed registry allocating isolated mutex instances per resource key:
$$\text{Lock}(Event_A) \cap \text{Lock}(Event_B) = \emptyset, \quad \forall A \ne B$$

---

## 6. EXPERIMENTAL EVALUATION & BENCHMARKS

### 6.1 Automated Concurrency Rush (50 Concurrent Threads Competing for 2 Seats)
Executed using `npm run test:concurrency`:

| Metric | Mutex Protected Mode (ON) | Unsynchronized Mode (OFF) | Evaluation |
| :--- | :---: | :---: | :--- |
| **Initial Available Seats** | 2 | 2 | Scarcity Baseline |
| **Concurrent Requests** | 50 Threads | 50 Threads | High-Contention Burst |
| **Successful Bookings** | **2 (Exact Match)** | **50 (All Approved!)** | Severe Race Hazard in OFF mode |
| **Rejected Requests (409)**| **48** | **0** | Clean rejection handled |
| **Final Remaining Seats** | **0** | **-48 (Oversold!)** | Invariant preserved with Mutex |
| **Overbooking Anomaly** | **0** | **+48 Phantom Tickets** | Mutual exclusion mathematically verified |
| **Total Test Duration** | 412 ms | 318 ms | Negligible lock overhead (< 2ms per acquisition) |

### 6.2 Real-Device Live Demonstration (Teacher Laptop vs. Friend Mobile)
Tested live under Wi-Fi local network:
1. **Initial Condition:** Event #1 set to **1 Tatkal Seat Remaining**.
2. **Experiment 1 (Mutex OFF):**
   - Both devices click "Book Team Pass" within 1.5 seconds.
   - Both devices bypass lock synchronization.
   - Result: Both receive confirmed booking passes with unique ticket codes!
   - Event remaining capacity drops to **-1** with red alert banner `⚠️ OVERBOOKED (-1)`.
3. **Experiment 2 (Mutex ON):**
   - Event #1 reset to **1 Tatkal Seat Remaining**.
   - Teacher completes Razorpay checkout first -> Confirmed Boarding Pass issued!
   - Capacity immediately decrements to 0.
   - Friend's concurrent request is serialized -> Rejected with `SOLD OUT: No seats remaining`.
   - Result: Remaining capacity holds strictly at **0**. Zero overselling.

---

## 7. TEAM ROSTER & DIVISION OF RESPONSIBILITIES

The project was conceptualized, designed, implemented, and benchmarked by the following 6-member team from **SR University (CSE Core, Academic Year 2025–2026)**:

| S.No | Hall Ticket No | Student Name | Assigned Core Engineering Role |
| :---: | :---: | :--- | :--- |
| 1 | `2503A51108` | **Ch. Naveen Reddy** | Systems Core, Mutex Primitive & FIFO Wait Queue Implementation |
| 2 | `2503A51109` | **K. Shiva Saketh** | Razorpay Standard Checkout SDK Integration & Payment Verification |
| 3 | `2503A51110` | **A. Shiva Ganesh (Team Leader)** | System Architecture, Full-Stack Engine, TOCTOU Simulator & Technical Documentation |
| 4 | `2503A51111` | **V. Saicharan** | Database Atomic Operations, Temp-File Flushing & State Invariant Auditing |
| 5 | `2503A1112` | **T. Geethika** | Commercial Luxury Editorial UI/UX, Cinematic Portal & Responsive Breakpoints |
| 6 | `2503A51113` | **G. Vishwas** | Concurrency Benchmarking, 50-Thread Stress Testing & Live Multi-Device QA |

---

## 8. CONCLUSION

The **SYNNEXA Event & Tatkal Registration System** delivers a conclusive, mathematically verifiable solution to Product #8. By implementing an asynchronous Mutex with FIFO bounded waiting and fine-grained resource isolation, the system guarantees 100% data integrity under arbitrary concurrent loads, eliminating negative capacity anomalies and bridging classical Operating System theory with production full-stack engineering.

---

## 9. REFERENCES

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). John Wiley & Sons. (Chapters 5 & 6: Process Synchronization & Concurrency).
2. Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.). Pearson Education.
3. Dijkstra, E. W. (1965). *Cooperating Sequential Processes*. Technological University, Eindhoven.
4. Lamport, L. (1974). *A New Solution of Dijkstra's Concurrent Programming Problem*. Communications of the ACM, 17(8), 453-455.
5. Peterson, G. L. (1981). *Myths About the Mutual Exclusion Problem*. Information Processing Letters, 12(3), 115-116.
6. Razorpay Technologies. (2026). *Standard Checkout Integration Guide & Payment Callbacks*. https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/
7. Node.js Foundation. (2026). *Node.js Core Architecture: Asynchronous Flow Control, Events & HTTP Module*. https://nodejs.org/api/
