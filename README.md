# SYNNEXA OS: High-Throughput Event & Tatkal Concurrency Platform
> **Product #8 • Operating Systems Concurrency Project • SR University**  
> **Core OS Concepts:** Critical Section, Asynchronous Mutex (Mutual Exclusion Lock), Concurrency Control, TOCTOU Race Condition Mitigation, FIFO Bounded Waiting

[![Live Deployment](https://img.shields.io/badge/Vercel-Live%20Platform-000000?style=for-the-badge&logo=vercel)](https://synnexa.vercel.app)
[![Admin Console](https://img.shields.io/badge/Admin-Organizer%20Console-0284C7?style=for-the-badge)](https://synnexa.vercel.app/admin)
[![Slide Deck](https://img.shields.io/badge/Download-Viva%20Deck%20(.pptx)-4F46E5?style=for-the-badge)](https://synnexa.vercel.app/download-ppt)

---

## 👥 Engineering Team (SR University, CSE Core — Ascending Order)

| S.No | Hall Ticket No | Student Name | Role & Module Ownership |
| :---: | :---: | :--- | :--- |
| 1 | `2503A51108` | **Ch. Naveen Reddy** | Systems Core, Mutex Primitive & FIFO Bounded Waiting Queue |
| 2 | `2503A51109` | **K. Shiva Saketh** | Razorpay Standard Checkout SDK Integration & Payment Verification |
| 3 | `2503A51110` | **A. Shiva Ganesh (Team Leader)** | System Architecture, Full-Stack Engine, TOCTOU Simulator & Technical Documentation |
| 4 | `2503A51111` | **V. Saicharan** | Database Atomic Operations, Temp-File Flushing & State Invariant Auditing |
| 5 | `2503A1112` | **T. Geethika** | Commercial Luxury Editorial UI/UX, Cinematic Portal & Responsive Breakpoints |
| 6 | `2503A51113` | **G. Vishwas** | Concurrency Benchmarking, 50-Thread Stress Testing & Live Multi-Device QA |

---

## 📌 Problem Statement & Core Scenario

> **"Several users attempt to register when only one or two places remain. How can the remaining capacity be updated correctly?"**

In high-demand event ticketing, railway Tatkal bookings, and university registration portals, shared state—specifically **remaining seat capacity**—is concurrently accessed and updated by multiple threads or distributed client requests.

### The Race Condition (Without Mutex / Unsynchronized)
When capacity is low (e.g., only 1 seat remaining), and two users click "Book Team Pass" at roughly the same time (e.g. Teacher on Laptop vs Friend on Mobile), a classic **Time-of-Check to Time-of-Use (TOCTOU)** race hazard occurs:

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

**Result:**
- Both users receive confirmed boarding passes.
- Remaining capacity drops below zero ($C_{remaining} = -1$).
- Physical venue / quota capacity is violated.

---

## 🛡️ The Operating System Solution

To prevent race conditions, the check, payment validation, duplicate detection, and decrement are enclosed in an **atomic, indivisible operation inside a Critical Section**, protected by an **OS Mutex (Mutual Exclusion Lock)**.

### Classical OS Critical Section Properties Satisfied:
1. **Mutual Exclusion:** Only one thread executes inside the critical section for an event at any given time ($\forall t, |\mathcal{C}(t)| \le 1$).
2. **Progress:** If no thread is inside the critical section, waiting threads are scheduled immediately without deadlock.
3. **Bounded Waiting:** A First-Come, First-Served (FIFO) wait queue ensures every competing thread has a deterministic upper bound on wait time ($O(k)$ starvation elimination).

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

**System Invariant Maintained:**
$$\forall t, \quad 0 \le C_{remaining}(t) \le C_{total}$$

---

## 📱 Live 2-Device Physical Demonstration (Viva Walkthrough)

The platform includes a dedicated **Real-Device Concurrency Test Station** inside `/admin` to demonstrate live in front of evaluators:

### Test 1: Mutex OFF (Race Condition Occurs)
1. Open `https://synnexa.vercel.app/admin`.
2. For Event #1, set Mutex to **OFF**.
3. Click **`⚡ Prime Event #1 to Exactly 1 Seat`**.
4. Open `https://synnexa.vercel.app` on **Device 1 (Teacher's Laptop)** and **Device 2 (Friend's Mobile)**.
5. Both devices click **"Book Team Pass →"** and click **"Pay with Razorpay"** roughly at the same time.
6. **Result:** Both devices get confirmed tickets! Remaining capacity drops to **`-1`** and flashes **`⚠️ OVERBOOKED (-1)`** in Admin!

### Test 2: Mutex ON (Mutual Exclusion Enforced)
1. In `/admin`, toggle Mutex to **ON** for Event #1.
2. Click **`⚡ Prime Event #1 to Exactly 1 Seat`**.
3. Both devices click **"Book Team Pass →"** and checkout simultaneously.
4. **Result:** Whichever transaction completes first secures the pass (seats -> 0). The second device is serialized and rejected with **`SOLD OUT: Tatkal quota completely exhausted`**!

---

## 🌟 Key Features

1. **Official Razorpay Standard Checkout SDK:** Authentic modal popup supporting sandbox UPI, Card, and NetBanking payments.
2. **Printable Boarding Pass (`window.print()`):** Print-optimized stylesheet (`@media print`) rendering a physical summit credential with procedural QR code and attendee roster.
3. **Keyed Mutex Registry:** Fine-grained per-event lock multiplexing ensuring concurrent registrations for Event A do not block Event B.
4. **Unified Organizer Admin Console:** Real-time capacity manager, 1-click demo primer, attendee roster with CSV export, gateway credential settings, and microsecond audit log stream.
5. **Zero External Runtime Dependencies:** Built entirely with native Node.js standard libraries (`http`, `fs`, `path`, `crypto`).

---

## 🚀 Quick Start (Local Development)

```bash
# Clone the repository
git clone https://github.com/ShivaGanesh1080-ops/synnexa-os-concurrency.git
cd synnexa-os-concurrency

# Run unit tests
npm test

# Run 50-thread high-concurrency stress benchmark
npm run test:concurrency

# Start local server
npm start
```
* **Local Web Dashboard:** `http://localhost:3000`
* **Local Admin Console:** `http://localhost:3000/admin`
* **Local Wi-Fi Network Access (Mobile):** `http://<your-lan-ip>:3000`

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/hackathons` | Lists all events with live capacity and Mutex status |
| `GET` | `/api/hackathons/:id` | Returns single event details and registered teams |
| `PUT` | `/api/hackathons/:id` | Updates event details / sets remaining capacity |
| `POST` | `/api/hackathons/:id/toggle-mutex` | Toggles Mutex protection ON / OFF for specific event |
| `POST` | `/api/book` | Books squad pass (Mutex protected or unprotected based on setting) |
| `POST` | `/api/hackathons/checkin` | Verifies attendee ticket code at the door |
| `GET` | `/api/platform/settings` | Returns Razorpay sandbox credentials and platform fee |
| `POST` | `/api/platform/settings` | Updates gateway credentials and fee schedule |
| `GET` | `/api/platform/stats` | Telemetry stats (active events, volume, locks, contentions) |
| `GET` | `/api/audit-logs` | Microsecond critical section audit trail |
| `POST` | `/api/reset` | Resets all event capacities and locks to baseline state |
| `GET` | `/download-ppt` | Downloads official Viva Presentation deck (.pptx) |

---

## 🎓 Academic Presentation Metadata

| Attribute | Specification |
| :--- | :--- |
| **Product** | Event / Workshop Registration System (Product #8) |
| **Institution** | SR University, Warangal, Telangana |
| **Course** | Operating Systems Laboratory (Academic Year 2025–2026) |
| **Main OS Concept** | Critical Section, Mutex (Mutual Exclusion Lock) |
| **Problem Solved** | Multi-device race condition when only 1 or 2 seats remain |
| **Production Cloud** | [https://synnexa.vercel.app](https://synnexa.vercel.app) |
| **Admin Console** | [https://synnexa.vercel.app/admin](https://synnexa.vercel.app/admin) |
