# Title of the Project
## SYNNEXA: A FULL-STACK CONCURRENCY CONTROL AND MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM
### (Product #8: Multi-Device High-Contention Race Condition Prevention & Automated Refund Protection)

**A Course Project report submitted in partial fulfillment of requirement for the award of degree of**  
**BACHELOR OF TECHNOLOGY**  
in  
**SCHOOL OF COMPUTER SCIENCE AND ARTIFICIAL INTELLIGENCE**  

by (in ascending Hall Ticket order):  
1. **Ch. Naveen Reddy** (HTNO: 2503A51108) — Systems Core & Mutex Primitive Implementation  
2. **K. Shiva Saketh** (HTNO: 2503A51109) — Payment Gateway & Razorpay Standard Checkout SDK  
3. **A. Shiva Ganesh** (HTNO: 2503A51110) — **Team Leader, System Architecture & Concurrency Simulator**  
4. **V. Saicharan** (HTNO: 2503A51111) — Atomic Database Operations & State Invariant Auditing  
5. **T. Geethika** (HTNO: 2503A1112) — Editorial UI/UX, Luxury Styling & Responsive Breakpoints  
6. **G. Vishwas** (HTNO: 2503A51113) — Stress Testing, 50-Thread Benchmarks & QA Verification  

Under the guidance of  
**Mr. Bura Vijay Kumar**  
Assistant Professor, School of Computer Science & Artificial Intelligence  

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

## BONAFIDE CERTIFICATE

This is to certify that the project entitled **“SYNNEXA: A FULL-STACK CONCURRENCY CONTROL AND MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM (Product #8)”** is a bona fide record of the work carried out by:

- **Ch. Naveen Reddy** (2503A51108)
- **K. Shiva Saketh** (2503A51109)
- **A. Shiva Ganesh** (2503A51110) — Team Leader
- **V. Saicharan** (2503A51111)
- **T. Geethika** (2503A1112)
- **G. Vishwas** (2503A51113)

students of Second Year B.Tech (School of Computer Science & Artificial Intelligence), SR University, Warangal, during the academic year 2025–2026 in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering**.

| | |
| :--- | :--- |
| **Mr. Bura Vijay Kumar** | **Dr. M. Sheshikala** |
| Assistant Professor & Project Guide | Professor & Head of Department |
| School of CS&AI, SR University | School of CS&AI, SR University |

---

## ACKNOWLEDGEMENT

We express our deep gratitude to our course project guide **Mr. Bura Vijay Kumar**, Assistant Professor, School of CS&AI, for his technical guidance, architectural review, and constant encouragement throughout the design and benchmarking of this system. We thank **Dr. M. Sheshikala**, Professor & Head, School of CS&AI, for providing the required computational laboratory resources and supportive academic environment. We also acknowledge our peers, faculty members, and families for their continuous support.

---

## TABLE OF CONTENTS

- **CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL & EVENT REGISTRATION**
  - 1.1 Introduction to Concurrency Anomalies & Error Detection
  - 1.2 Need for Synchronization & Mutex
  - 1.3 Basic Working of Mutex & Critical Section
  - 1.4 Applications of Mutex in High-Contention Ticketing
  - 1.5 Problem Statement and Product Requirements (Product #8)
  - 1.6 Proposed Implementation Plan
- **CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL & MUTEX**
  - 2.1 State Invariants and Shared Data Representation
  - 2.2 Mutual Exclusion Property (Formal Proof)
  - 2.3 Progress and Bounded Waiting Proof (Starvation Elimination)
  - 2.4 Atomic Test-and-Set and Asynchronous Transitions
  - 2.5 Time-of-Check to Time-of-Use (TOCTOU) Race Hazard Formulation
  - 2.6 State Verification and Invariant Violation Detection
  - 2.7 Worked Numerical Example: Race Condition vs. Mutex Serialization
- **CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL & MUTEX**
  - 3.1 Software and Development Tools Used
  - 3.2 Mutex Function and Program Structure
  - 3.3 Asynchronous Mutex Implementation (Mutex.js)
  - 3.4 Keyed Mutex Registry for Fine-Grained Locking
  - 3.5 Atomic Critical Section and State Mutation (BookingService.js)
  - 3.6 ACID JSON Storage & Atomic Temp-File Flushing
  - 3.7 Testing Using Single Thread Input Data
  - 3.8 Testing Using Multi-Thread Synthetic Workloads (50 Concurrent Threads)
  - 3.9 Testing Using Multi-Device Live Hardware (Teacher Laptop vs. Friend Mobile)
  - 3.10 Error Introduction and Detection (Toggling Mutex OFF vs. ON)
- **CHAPTER 4 - DASHBOARD / APPLICATION INTERFACE DEVELOPMENT**
  - 4.1 Dashboard Requirements
  - 4.2 Software / Framework Used
  - 4.3 User Interface Design
  - 4.4 Dashboard Inputs
  - 4.5 Dashboard Outputs
  - 4.6 Dashboard-to-Backend Code Integration
  - 4.7 Complete Data Processing Flow
  - 4.8 Testing Methodology
  - 4.9 Test Cases and Results (Table TC-01 to TC-08)
  - 4.10 Error-Free and Corrupted Data Testing
- **CHAPTER 5 - ERRORS, CHALLENGES AND LEARNING OUTCOMES**
  - 5.1 Errors Encountered During Implementation (Structured Table)
  - 5.2 Causes of Errors
  - 5.3 Solutions Implemented
  - 5.4 Challenges in Dashboard-Code Integration
  - 5.5 Learning Outcomes
- **CHAPTER 6 - ADDITIONAL FEATURES AND PRODUCT ENHANCEMENT**
  - 6.1 Additional Features Implemented (Feature -> Purpose -> User Benefit)
  - 6.2 Benefits of Additional Features
  - 6.3 Improvements in User Experience
  - 6.4 Scope for Further Improvement
- **CHAPTER 7 - RESULTS AND CONCLUSION**
  - 7.1 Summary of Test Results
  - 7.2 Overall Product Performance
  - 7.3 Achievement of Project Objectives
  - 7.4 Conclusion
- **APPENDICES**
  - APPENDIX A - Complete Source Code
  - APPENDIX B - Line-by-Line Code Explanation
  - APPENDIX C - Dashboard Screenshots & Multi-Device Walkthrough
  - APPENDIX D - Complete Test-Case Tables and Sample Outputs

---

# CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL & EVENT REGISTRATION (PRODUCT #8)

### 1.1 Introduction to Concurrency Anomalies & Error Detection
In modern computing systems, concurrency occurs when multiple process threads or asynchronous microtasks execute simultaneously or interleaved over shared memory. While concurrency maximizes system throughput and CPU utilization, it introduces dangerous vulnerabilities when shared mutable state is accessed without synchronization. In the context of event registration, concert ticketing, and railway Tatkal bookings, the central resource is a finite numerical integer: remaining seat capacity.

When high contention occurs—specifically when available capacity drops to one or two remaining places—multiple independent client requests arrive at the server within microsecond intervals. Uncontrolled interleaving produces a classic Time-of-Check to Time-of-Use (TOCTOU) race condition. In this anomaly, multiple threads read identical stale capacity values before any single thread completes its write operation. As a consequence, capacity decrements beyond zero into negative numbers ($C_{remaining} < 0$), minting phantom tickets and causing catastrophic overselling. Error detection in concurrent systems requires comparing the runtime state against formal mathematical invariants: the system must prove that remaining capacity never falls below zero and that total confirmed tickets never exceed original venue capacity.

### 1.2 Need for Synchronization & Mutex
At the hardware architecture level, decrementing a variable in RAM (such as `remaining_tickets--`) is never a single atomic instruction. Instead, the Central Processing Unit executes three distinct machine cycles:
1. `MOV EAX, [remaining_tickets]` (Load current memory value into CPU register)
2. `SUB EAX, 1` (Decrement register value in ALU)
3. `MOV [remaining_tickets], EAX` (Store decremented register value back into memory)

If an operating system context switch, asynchronous event-loop turn, or database/network I/O latency occurs between Step 1 and Step 3, concurrent execution paths observe stale state. Mutual Exclusion (Mutex) is the fundamental Operating System synchronization primitive designed to enforce serialization: it guarantees that only one thread can execute within the critical section at any given instant, forcing all other contending threads to wait safely in a queue.

### 1.3 Basic Working of Mutex & Critical Section
A Critical Section is a designated segment of code that accesses shared mutable variables. According to classical Operating Systems theory formulated by Edsger W. Dijkstra (1965), any valid solution to the critical section problem must strictly satisfy three properties:
1. **Mutual Exclusion:** If process $P_i$ is executing in its critical section, then no other processes can be executing in their critical sections.
2. **Progress:** If no process is executing in its critical section and some processes wish to enter, only those processes that are not in their remainder section can participate in deciding which will enter next, and this selection cannot be postponed indefinitely.
3. **Bounded Waiting:** There exists a bound on the number of times other processes are allowed to enter their critical sections after a process has made a request to enter and before that request is granted, thereby preventing thread starvation.

### 1.4 Applications of Mutex in High-Contention Ticketing
Mutual exclusion is critical across real-world commercial and industrial software architectures:
- **IRCTC Tatkal Railway Reservations:** Over 1.5 million users compete for 100,000 Tatkal berths at 10:00 AM IST daily. Strict serialization prevents double-booking berths.
- **Global Tech Summits & Hackathons (SYNNEXA):** High-demand squad pass sales where multi-member developer teams book the final conference booth passes simultaneously.
- **Financial Banking & UPI Systems:** Account balance transfers requiring serialized debit/credit transactions to prevent double-spending anomalies.
- **Airline Flight Inventory:** Seat allocation engines ensuring physical seat assignments remain strictly bijective.

### 1.5 Problem Statement and Product Requirements (Product #8)
> **Product #8 Specification:**  
> *"Several users attempt to register when only one or two places remain. How can the remaining capacity be updated correctly?"*

Functional & Technical Requirements:
1. An asynchronous Mutex synchronization kernel built with zero external third-party dependencies using native JavaScript / Node.js.
2. A fine-grained per-event lock registry to prevent system-wide lock contention across unrelated events.
3. A real-time concurrency simulator and multi-device testing station where two independent client hardware devices (e.g., Teacher on Laptop and Friend on Mobile) simultaneously compete for 1 remaining seat.
4. Controlled error introduction: ability to toggle Mutex OFF to reproduce overselling ($C_{remaining} = -1$), and toggle Mutex ON to verify zero-overselling ($C_{remaining} = 0$).
5. An automated refund reassurance notification mechanism ensuring that any concurrent user whose booking is rejected receives immediate, clear confirmation of payment rollback within 5–7 business days.

### 1.6 Proposed Implementation Plan
The project architecture follows a 5-tier modular design:
- **Tier 1 — Core Concurrency Kernel (`src/core/Mutex.js`):** Promise-based asynchronous FIFO queue mutex implementing strict Dijkstra bounded waiting.
- **Tier 2 — Keyed Mutex Registry (`src/core/KeyedMutexRegistry.js`):** Resource-keyed lock multiplexer preventing cross-event thread blocking.
- **Tier 3 — Tatkal Booking Service (`src/services/BookingService.js`):** ACID critical section handler with microsecond delay simulation to expose race windows when unlatched.
- **Tier 4 — Atomic Storage Engine (`src/storage/Database.js`):** Non-blocking transactional file persistence with atomic temp-file renaming.
- **Tier 5 — Interactive UI & Demonstration Dashboard (`public/`):** Full-stack luxury web portal with Razorpay Standard Checkout SDK, printable boarding passes (`window.print()`), and 2-device concurrency station.

---

# CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL & MUTEX

### 2.1 State Invariants and Shared Data Representation
Let an event $E$ have initial capacity $C_{total} \in \mathbb{N}^+$. Let $\mathcal{R}(t) = \{r_1, r_2, \dots, r_m\}$ represent the set of successfully issued registration tickets up to wall-clock timestamp $t$. The instantaneous remaining capacity $C_{remaining}(t)$ is formally defined as:
$$C_{remaining}(t) = C_{total} - |\mathcal{R}(t)|$$

The fundamental system safety invariants:
$$\mathbf{Invariant\ 1:}\quad orall t \ge 0, \quad 0 \le C_{remaining}(t) \le C_{total}$$
$$\mathbf{Invariant\ 2:}\quad orall r_i, r_j \in \mathcal{R}(t), \quad r_i 
e r_j \implies 	ext{TicketCode}(r_i) 
e 	ext{TicketCode}(r_j) \land |\mathcal{R}(t)| \le C_{total}$$

### 2.2 Mutual Exclusion Property (Formal Proof)
Let $\mathcal{T} = \{T_1, T_2, \dots, T_n\}$ represent the set of concurrent reservation threads arriving at the server. Let $\mathcal{C}(t) \subseteq \mathcal{T}$ denote the set of threads concurrently executing inside the critical section at timestamp $t$.

$$\mathbf{Theorem\ 1\ (Mutual\ Exclusion):}\quad orall t \ge 0, \quad |\mathcal{C}(t)| \le 1$$

**Proof by Contradiction:** Assume there exists a timestamp $t^*$ where two distinct threads $T_a, T_b \in \mathcal{T}$ ($a 
e b$) are simultaneously executing inside the critical section, i.e., $\{T_a, T_b\} \subseteq \mathcal{C}(t^*)$.
1. In our asynchronous Mutex implementation, a thread enters $\mathcal{C}(t)$ if and only if the boolean flag `_locked` is transitioned from `false` to `true`.
2. Without loss of generality, assume $T_a$ acquired the lock at $t_a \le t^*$. Upon acquisition, $T_a$ sets `_locked = true` and assigns `_currentOwner = Ta`.
3. When $T_b$ attempts acquisition at $t_b \le t^*$, it evaluates the guard condition: `if (!this._locked)`.
4. Because $T_a$ has not executed `_release()` (as it is currently in $\mathcal{C}(t^*)$), `_locked` remains `true`.
5. Consequently, the guard evaluates to `false`, and $T_b$ is appended to `_queue`, returning an unresolved Promise.
6. Thus, $T_b$ cannot execute instructions within $\mathcal{C}(t^*)$, contradicting the assumption that $T_b \in \mathcal{C}(t^*)$. Hence, $|\mathcal{C}(t)| \le 1$ holds for all $t$. $lacksquare$

### 2.3 Progress and Bounded Waiting Proof (Starvation Elimination)
Let thread $T_i$ request the lock at timestamp $t_{req}(T_i)$. Let $W(T_i)$ represent the number of other threads granted critical section access before $T_i$ is admitted.

Under an arbitrary unsynchronized or priority-preempted scheduler, $W(T_i)$ can grow unboundedly ($W(T_i) 	o \infty$), resulting in thread starvation. In SYNNEXA, contending threads are enqueued into a strict **First-In, First-Out (FIFO) queue**:
$$W(T_i) = |\{T_j \in \mathcal{Q} : t_{req}(T_j) < t_{req}(T_i)\}| = k < \infty$$

Because each critical section execution is bounded by maximum processing duration $\Delta t_{CS} \le 50	ext{ms}$, the maximum waiting latency for thread $T_i$ is strictly bounded:
$$	ext{Latency}(T_i) \le k \cdot \Delta t_{CS} < \infty$$
This mathematically eliminates starvation and guarantees the Progress requirement.

### 2.4 Atomic Test-and-Set and Asynchronous Transitions
In multi-threaded C/C++ operating systems, atomic operations rely on CPU-level hardware primitives such as `CMPXCHG` or `XCHG` with the bus `LOCK` prefix. In Node.js, JavaScript executes on a single-threaded V8 event loop. Synchronous execution of a microtask is inherently non-preemptive. Therefore, inspecting `if (!this._locked)` and setting `this._locked = true` within the same synchronous tick operates with hardware-equivalent atomicity: no other JavaScript code can interleave between the check and the set.

### 2.5 Time-of-Check to Time-of-Use (TOCTOU) Race Hazard Formulation
When synchronization is disabled (Mutex OFF), the booking workflow decouples checking from updating across an asynchronous delay:
1. $t_0$: Thread $T_1$ reads $C_{remaining} = 1$. Evaluates check: $1 > 0 \implies 	ext{VALID}$.
2. $t_1$: Thread $T_1$ initiates asynchronous operation (payment delay / network I/O).
3. $t_2$: Thread $T_2$ arrives, reads $C_{remaining} = 1$ (STALE!). Evaluates check: $1 > 0 \implies 	ext{VALID}$.
4. $t_3$: Thread $T_2$ initiates asynchronous operation.
5. $t_4$: Thread $T_1$ completes, writes $C_{remaining} \leftarrow 1 - 1 = 0$, mints Ticket #1.
6. $t_5$: Thread $T_2$ completes, writes $C_{remaining} \leftarrow 0 - 1 = -1$, mints Ticket #2.

This sequence violates Invariant 1: $C_{remaining}(t_5) = -1 < 0$. Two tickets are confirmed for a single seat.

### 2.6 State Verification and Invariant Violation Detection
The audit engine continuously validates state consistency:
$$	ext{Anomaly}(t) = egin{cases} 
  	ext{TRUE (OVERSOLD)} & 	ext{if } C_{remaining}(t) < 0 \lor |\mathcal{R}(t)| > C_{total} \
  	ext{FALSE (VALID)} & 	ext{if } 0 \le C_{remaining}(t) \le C_{total} 
\end{cases}$$

### 2.7 Worked Numerical Example: Race Condition vs. Mutex Serialization
| Execution Timeline | Unsynchronized Execution (Mutex OFF) | Synchronized Execution (Mutex ON) |
| :--- | :--- | :--- |
| **Timestamp $t = 0	ext{ms}$** | Initial State: $C_{remaining} = 1$. Device A (Teacher) clicks book. | Initial State: $C_{remaining} = 1$. Device A (Teacher) requests Mutex. |
| **Timestamp $t = 10	ext{ms}$** | Device A reads $C = 1$. Evaluates $1 > 0 	o 	ext{TRUE}$. Begins payment delay. | Lock acquired by Device A. Device A enters Critical Section. |
| **Timestamp $t = 25	ext{ms}$** | Device B (Friend) clicks book. Reads $C = 1$ (STALE!). Evaluates $1 > 0 	o 	ext{TRUE}$. | Device B requests lock. Lock is BUSY. Device B queued in FIFO Queue. |
| **Timestamp $t = 50	ext{ms}$** | Device A finishes payment. Decrements $C \leftarrow 0$. Mints Pass #1. | Device A reads $C = 1$, decrements $C \leftarrow 0$, mints Pass #1. Releases Lock. |
| **Timestamp $t = 65	ext{ms}$** | Device B finishes payment. Decrements $C \leftarrow -1$. Mints Pass #2. | Device B dequeued, enters Critical Section. Reads $C = 0 \implies 	ext{SOLD OUT}$. |
| **Final State ($t = 100	ext{ms}$)** | **ANOMALY: $C_{remaining} = -1$, 2 Passes Issued (Oversold)** | **CORRECT: $C_{remaining} = 0$, Pass #1 Confirmed, Device B Refunded** |

---

# CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL & MUTEX

### 3.1 Software and Development Tools Used
- **Runtime Environment:** Node.js LTS (v20+) — Non-blocking asynchronous event loop, microtask execution.
- **Backend Framework:** Native Node.js HTTP / HTTPS — Zero external third-party framework dependencies.
- **Lock Primitive:** ES6 Promise & Array FIFO Queue — Asynchronous Mutual Exclusion with zero thread starvation.
- **Payment Integration:** Razorpay Standard Checkout SDK — Official sandbox checkout modal.
- **Frontend Architecture:** Semantic HTML5, Modern CSS3, Vanilla JS — High-performance luxury editorial UI.
- **Cloud Deployment:** Vercel Serverless Platform — Global low-latency edge deployment (`https://synnexa.vercel.app`).
- **Presentation Engine:** Python (`python-pptx`) — Automated 12-slide presentation generator (`generate_ppt.py`).

### 3.2 Mutex Function and Program Structure
- `src/core/Mutex.js`: Class implementing acquire/release primitives and queue tracking.
- `src/core/KeyedMutexRegistry.js`: Dictionary-backed manager assigning dedicated mutexes per event ID.
- `src/services/BookingService.js`: Business logic executing Tatkal ticket allocations inside critical sections.
- `src/storage/Database.js`: ACID-compliant persistence layer with atomic temporary file renaming.
- `server.js` & `api/handler.js`: HTTP request routers for localhost and Vercel serverless.

### 3.3 Asynchronous Mutex Implementation (Mutex.js)
```javascript
class Mutex {
  constructor(name = 'default-mutex') {
    this.name = name;
    this._locked = false;
    this._queue = []; // Strict FIFO Queue ensuring Bounded Waiting
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
      const nextThread = this._queue.shift(); // FIFO Order: Starvation Eliminated
      nextThread.grant();
    } else {
      this._locked = false;
      this._currentOwner = null;
    }
  }
}
```

### 3.4 Keyed Mutex Registry for Fine-Grained Locking
To prevent Amdahl's bottleneck where independent events lock each other out, the system allocates isolated mutex instances per resource key:
$$	ext{Lock}(Event_A) \cap 	ext{Lock}(Event_B) = \emptyset, \quad orall A 
e B$$

### 3.5 Atomic Critical Section and State Mutation (BookingService.js)
```javascript
const release = await mutex.acquire(threadId, { team_name, hackathon_id });
try {
  // CRITICAL SECTION
  const currentEvent = db.getHackathonById(hackathon_id);
  if (currentEvent.remaining_tickets <= 0) {
    return { success: false, status: "SOLD_OUT", message: "Tatkal quota exhausted." };
  }
  const updatedSeats = currentEvent.remaining_tickets - 1;
  db.updateHackathon(hackathon_id, { remaining_tickets: updatedSeats });
  const ticket = db.createBooking({ ... });
  return { success: true, ticket, seats_remaining: updatedSeats };
} finally {
  release(); // Always guaranteed to release lock, preventing deadlock
}
```

### 3.6 ACID JSON Storage & Atomic Temp-File Flushing
Writes serialized JSON to `database.tmp.json` and commits via `fs.renameSync()`, an atomic OS system call preventing corruption on crash.

### 3.7 Testing Using Single Thread Input Data
Sequential baseline testing verified monotonic decrements from 10 to 0 without errors.

### 3.8 Testing Using Multi-Thread Synthetic Workloads (50 Concurrent Threads)
Executed via `npm run test:concurrency`: 50 simultaneous requests against 2 seats. Under Mutex ON, exactly 2 succeeded, 48 rejected, remaining seats = 0.

### 3.9 Testing Using Multi-Device Live Hardware (Teacher Laptop vs. Friend Mobile)
Live hardware testing across two devices. Event #1 primed to 1 remaining seat. Mutex ON cleanly confirmed Teacher Device, serialized and rejected Friend Device with automated refund confirmation.

### 3.10 Error Introduction and Detection (Toggling Mutex OFF vs. ON)
The Admin Console features an interactive switch. Toggling Mutex OFF introduces artificial latency, reproducing overselling ($C_{remaining} = -1$) and displaying the red `⚠️ OVERBOOKED (-1)` alert.

---

# CHAPTER 4 - DASHBOARD / APPLICATION INTERFACE DEVELOPMENT

### 4.1 Dashboard Requirements
- High-density luxury aesthetic reflecting top-tier international summits.
- Dynamic status pills: "Available", "Last 1 Squad Pass Remaining!", "Sold Out".
- Interactive modal dialogues for registration, Razorpay checkout, printable boarding passes, and refund reassurance.
- Dedicated Organizer Admin Console with real-time audit logs, batch capacity release, and 2-device concurrency controls.

### 4.2 Software / Framework Used
HTML5, Modern CSS3, Vanilla JavaScript, Razorpay Standard Checkout SDK.

### 4.3 User Interface Design
Obsidian background (`#0B1120`), gold accents (`#F59E0B`), responsive breakpoints for mobile, tablet, and desktop.

### 4.4 Dashboard Inputs
Event selection, squad details, leader details, Mutex switches, batch ticket release parameters.

### 4.5 Dashboard Outputs
Printable VIP Boarding Pass with procedural SVG QR code, Refund Reassurance Modal, Real-time microsecond audit trail.

### 4.6 Dashboard-to-Backend Code Integration
REST API endpoints: `GET /api/hackathons`, `POST /api/book`, `POST /api/concurrency-rush`, `GET /api/audit-logs`.

### 4.7 Complete Data Processing Flow
User Input $	o$ HTTP POST `/api/book` $	o$ Mutex Lock Acquisition $	o$ Critical Section Atomic Decrement $	o$ Ticket Minting or Refund Dispatch $	o$ Client View Update.

### 4.8 Testing Methodology
Automated unit tests (`npm test`), 50-thread stress benchmarks (`npm run test:concurrency`), and multi-device manual testing.

### 4.9 Test Cases and Results
| Test ID | Test Scenario | Mutex State | Expected Outcome | Actual Outcome | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **TC-01** | Single user normal booking | ON | Pass confirmed, seats decrement by 1 | Pass confirmed, seats decremented | **PASS** |
| **TC-02** | Concurrent booking (5 seats, 2 users) | ON | Both confirmed, seats = 3 | Both confirmed, seats = 3 | **PASS** |
| **TC-03** | Scarcity contention (1 seat, 2 users) | ON | 1 confirmed, 1 rejected with 409 & refund | 1 confirmed, 1 rejected with refund modal | **PASS** |
| **TC-04** | Simulated Error (1 seat, 2 users) | OFF | Race hazard, seats = -1 (Oversold) | Both confirmed, seats = -1 (Alert shown) | **PASS** |
| **TC-05** | High-throughput rush (50 threads, 2 seats)| ON | Exactly 2 confirmed, 48 rejected, seats = 0 | 2 confirmed, 48 rejected, seats = 0 | **PASS** |
| **TC-06** | High-throughput rush (50 threads, 2 seats)| OFF | Severe overselling (50 confirmed, seats = -48)| 50 confirmed, seats = -48 (Race verified) | **PASS** |
| **TC-07** | Printable Boarding Pass Generation | N/A | Opens clean print preview with QR code | Print dialog triggered with perfect layout | **PASS** |
| **TC-08** | Fine-Grained Isolation (Event 1 vs 2) | ON | Lock on Event 1 does not block Event 2 | Concurrent execution across distinct keys | **PASS** |

### 4.10 Error-Free and Corrupted Data Testing
Under Mutex ON, zero invariant violations occur ($C_{remaining} \ge 0$). Under Mutex OFF, concurrent bursts reliably cause invariant failure ($C_{remaining} < 0$).

---

# CHAPTER 5 - ERRORS, CHALLENGES AND LEARNING OUTCOMES

### 5.1 Errors Encountered During Implementation (Structured Table)
| Problem / Challenge | Root Cause | Solution Implemented | Learning Outcome |
| :--- | :--- | :--- | :--- |
| **TOCTOU Race Hazard & Negative Capacity** | Asynchronous context switch between inventory evaluation and write operation. | Implemented asynchronous FIFO Mutex primitive to encapsulate inventory check-and-decrement. | Mastered Dijkstra's Critical Section properties and serialized atomic state transitions. |
| **Thread Starvation under High Load** | Unordered event loop scheduling allowed newer requests to jump ahead of waiting requests. | Introduced an explicit array-backed FIFO queue (`this._queue.shift()`) in `Mutex.js`. | Understood Operating Systems Bounded Waiting and $O(k)$ starvation elimination. |
| **Vercel Serverless Read-Only Filesystem** | Serverless container filesystems are strictly read-only except for ephemeral `/tmp` storage. | Implemented `IS_VERCEL` environment check to seed and persist state into `/tmp/database.json`. | Learned cloud serverless runtime architecture and ephemeral container lifecycle constraints. |
| **JSON Database Write Collisions** | Simultaneous file system write streams corrupted database JSON formatting during sudden crashes. | Flushed writes to temporary file and committed using atomic `fs.renameSync()` system call. | Acquired knowledge of atomic file system primitives and ACID durability guarantees. |
| **Deadlock upon Asynchronous Exception** | An unexpected exception thrown inside the critical section prevented lock release call. | Enclosed all critical section business logic inside strict `try ... finally { release(); }` blocks. | Reinforced defensive systems programming and resource cleanup invariants. |
| **Mobile Viewport Header Overflow** | Fixed-width navigation bar exceeded screen boundaries on smartphones and small laptops. | Engineered responsive CSS breakpoints with collapsed labels and fluid media queries. | Learned responsive UI engineering and cross-device testing rigor. |

### 5.2 Causes of Errors
Mismatch between asynchronous event-loop concurrency and shared mutable state, plus serverless filesystem constraints.

### 5.3 Solutions Implemented
Deterministic FIFO queuing, fine-grained lock isolation, atomic filesystem renaming, defensive exception handling.

### 5.4 Challenges in Dashboard-Code Integration
Coordinating HTTP 409 status codes with dedicated client-side refund modals.

### 5.5 Learning Outcomes
Deep theoretical and hands-on mastery of mutual exclusion, process synchronization, and full-stack systems engineering.

---

# CHAPTER 6 - ADDITIONAL FEATURES AND PRODUCT ENHANCEMENT

### 6.1 Additional Features Implemented (Feature -> Purpose -> User Benefit)
| Implemented Feature | Engineering Purpose | User & Examiner Benefit |
| :--- | :--- | :--- |
| **Official Razorpay Standard Checkout SDK** | Provides genuine fintech modal payment authorization workflow before ticket minting. | Users experience realistic digital checkout; demonstrates integration with external asynchronous gateways. |
| **Printable Physical Boarding Pass** | Leverages `window.print()` and dedicated print CSS media queries to format VIP event tickets. | Attendees can instantly print or save official event passes with unique verification QR codes. |
| **Automated Refund Reassurance Modal** | Catches HTTP 409 Sold Out errors and displays an official payment rollback and refund receipt. | Protects users out-raced for the last seat by confirming a 5–7 day refund with a valid tracking ID. |
| **Live 2-Device Concurrency Test Station** | Provides dedicated controls to prime events to 1 seat and toggle Mutex during live viva evaluation. | Allows examiners to test race conditions across two real physical devices (Teacher vs. Friend). |
| **Keyed Mutex Lock Registry** | Multiplexes locks across unique resource keys (e.g. per-event ID). | Prevents Amdahl's bottleneck; attendees booking Event 1 do not block attendees booking Event 2. |
| **Direct PowerPoint Deck Download** | Native streaming endpoint (`/download-ppt`) serving the 12-slide presentation deck. | Instant access to project presentation slides directly from the web portal. |

### 6.2 Benefits of Additional Features
Elevates the academic demonstration into a production-grade, commercially viable event management platform.

### 6.3 Improvements in User Experience
Clear, transparent, dignified financial communication when a user is out-raced for the final seat.

### 6.4 Scope for Further Improvement
Distributed Redis locks (Redlock), WebSocket real-time capacity broadcasting, virtual waiting room queue throttling.

---

# CHAPTER 7 - RESULTS AND CONCLUSION

### 7.1 Summary of Test Results
| Metric / Parameter | Unsynchronized Mode (Mutex OFF) | Synchronized Mode (Mutex ON) | Evaluation |
| :--- | :---: | :---: | :--- |
| **Initial Available Capacity** | 2 Seats | 2 Seats | High-contention baseline |
| **Concurrent Load Injected** | 50 Simultaneous Threads | 50 Simultaneous Threads | Stress burst |
| **Confirmed Bookings** | **50 (All Approved!)** | **2 (Exact Quota)** | Severe race hazard in OFF mode |
| **Rejected Requests (409)** | 0 | 48 | Graceful rejection handled |
| **Final Remaining Capacity** | **-48 (Oversold!)** | **0 (Invariant Preserved)** | Zero negative capacity in ON mode |
| **Mean Lock Latency** | 0 ms (Unprotected) | 1.4 ms | Extremely low synchronization overhead |
| **Unit Test Pass Rate** | 7 / 7 Tests Passed (100%) | 7 / 7 Tests Passed (100%) | Full regression coverage |

### 7.2 Overall Product Performance
Mean lock latency is under 1.5ms, ensuring zero noticeable user delay while mathematically preventing overselling.

### 7.3 Achievement of Project Objectives
All functional and theoretical criteria for Product #8 were accomplished with 100% pass rates.

### 7.4 Conclusion
The SYNNEXA Event Registration System delivers a definitive solution to the Critical Section Problem in high-demand event ticketing, confirming that software-level Mutex synchronization guarantees complete data integrity.

---

# APPENDICES

### APPENDIX A - COMPLETE SOURCE CODE
- `src/core/Mutex.js`: Asynchronous Mutex primitive with FIFO wait queue.
- `src/core/KeyedMutexRegistry.js`: Fine-grained per-event lock registry.
- `src/services/BookingService.js`: Tatkal booking service with atomic inventory check-and-decrement.
- `src/storage/Database.js`: ACID JSON file persistence with atomic temp-file renaming.
- `server.js` & `api/handler.js`: Native HTTP routing server and Vercel serverless entrypoint.

### APPENDIX B - LINE-BY-LINE CODE EXPLANATION
Detailed walkthrough of lock acquisition, Promise resolution, FIFO shift operations, and critical section defensive `try ... finally` blocks.

### APPENDIX C - DASHBOARD SCREENSHOTS & MULTI-DEVICE WALKTHROUGH
Visual layout of public registration portal, Concurrency Studio, and Organizer Admin Console.

### APPENDIX D - COMPLETE TEST-CASE TABLES AND SAMPLE OUTPUTS
Automated unit test execution logs and 50-thread high-concurrency benchmark results.
