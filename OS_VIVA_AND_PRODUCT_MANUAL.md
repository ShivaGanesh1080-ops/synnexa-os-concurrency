# Product 8: Event / Workshop Registration System
## Operating Systems Concurrency Project — Comprehensive Viva & Technical Manual

> **Course:** Operating Systems Lab / Concurrency Engineering  
> **Student:** Shiva Ganesh Akku | B.Tech CSE Core (2nd Year), SR University  
> **Project Directory:** `C:\Users\DELL\.gemini\antigravity\scratch\event-registration-mutex-system`  
> **Server Entry:** `node server.js` (Runs on `http://localhost:3000`)

---

## 1. Problem Statement & Classical OS Mapping

| Parameter | Specification |
| :--- | :--- |
| **Product #** | **Product 8 — Event / Workshop Registration System** |
| **Core Prompt** | *"Several users attempt to register when only one or two places remain. How can the remaining capacity be updated correctly?"* |
| **Main OS Concept** | **Critical Section Problem, Mutual Exclusion (Mutex)** |
| **Main Problem Solved** | Concurrency hazard & overbooking during high-contention flash registration (TOCTOU race condition). |
| **Unique Features** | Event listing, atomic registration, cancellation with seat restoration, dynamic capacity tracking, and duplicate-registration prevention. |

---

## 2. Core OS Concepts & Mathematical Formalization

### 2.1 The Race Condition (Without Mutex)
When multiple threads read and write shared memory concurrently without synchronization, the final outcome depends on the non-deterministic interleaving of instructions by the OS CPU scheduler.

In our system, updating capacity consists of three non-atomic machine-level operations:
1. **READ:** Read `remainingCapacity` from memory into CPU register.
2. **EVALUATE & MODIFY:** Check `remainingCapacity > 0` and decrement register by 1.
3. **WRITE:** Store updated register back into memory.

#### The TOCTOU (Time-of-Check to Time-of-Use) Vulnerability:
Suppose only **1 seat remains** ($C = 1$), and Thread $T_1$ (User A) and Thread $T_2$ (User B) arrive simultaneously:

```text
Time   Thread 1 (User A)                  Thread 2 (User B)                  Memory State
-----------------------------------------------------------------------------------------
t0     READ capacity (1)                  .                                  C = 1
t1     .                                  READ capacity (1)                  C = 1 (Stale!)
t2     CHECK (1 > 0) -> TRUE              .                                  C = 1
t3     .                                  CHECK (1 > 0) -> TRUE              C = 1 (Stale check!)
t4     DECREMENT (1 - 1 = 0)              .                                  Reg_T1 = 0
t5     .                                  DECREMENT (1 - 1 = 0)              Reg_T2 = 0
t6     WRITE back (0)                     .                                  C = 0
t7     .                                  WRITE back (0 - 1 = -1)            C = -1 [OVERBOOKED!]
t8     CONFIRM Ticket A                   CONFIRM Ticket B                   2 tickets for 1 seat!
```

### 2.2 The OS Solution: Critical Section & Mutex
A **Critical Section** is a code segment that accesses shared modifiable resources. To preserve data consistency, the access must be serialized using a **Mutex (Mutual Exclusion lock)**.

#### The 3 Classical Criteria of Dijkstra's Critical Section Problem:
1. **Mutual Exclusion:** If process $P_i$ is executing in its critical section, no other processes can be executing in their critical sections for that shared resource.
2. **Progress:** If no process is executing in its critical section and some processes wish to enter, only those processes not executing in their remainder sections can participate in deciding who enters next, and this selection cannot be postponed indefinitely.
3. **Bounded Waiting:** There must exist a bound on the number of times that other processes are allowed to enter their critical sections after a process has made a request to enter and before that request is granted (prevents starvation).

#### Invariant Maintained:
$$\forall t, \quad 0 \le C_{remaining}(t) \le C_{total}$$
$$C_{remaining}(t) + |\{\text{Valid Confirmed Registrations}\}| = C_{total}$$

---

## 3. Key Terms Glossary (Examiner-Grade Definitions)

1. **Race Condition:**  
   A flaw in concurrent execution where the system's output or final state is dependent on the uncontrollable order, timing, or interleaving of threads/processes.

2. **Critical Section (CS):**  
   The portion of program instructions where shared resources (e.g., global variables, memory buffers, files, databases) are accessed and mutated, requiring synchronization to prevent data corruption.

3. **Mutex (Mutual Exclusion Lock):**  
   A locking mechanism used to synchronize access to a resource. It is owned by only one thread at a time. Only the thread that acquired the mutex has the authority to release it.

4. **Binary Semaphore vs. Mutex:**  
   - **Ownership:** A mutex has the concept of ownership (only the acquiring thread can unlock it). A semaphore has no ownership; any thread can signal (`V()`) or wait (`P()`).
   - **Purpose:** Mutex is strictly for mutual exclusion. Semaphores can be used for both mutual exclusion and inter-thread signaling / synchronization.

5. **Counting Semaphore:**  
   A synchronization primitive initialized to an integer $N$ representing the number of available units of a shared resource. Threads decrement the counter via `wait()` and increment it via `signal()`. If the counter reaches 0, subsequent calling threads block.

6. **Starvation (Indefinite Blocking):**  
   A condition where a thread is perpetually denied the necessary resources or CPU time to make progress because other threads are repeatedly prioritized.

7. **Bounded Waiting:**  
   An OS guarantee that limits how many times other threads can bypass a waiting thread before that thread gets access to the critical section. Our project guarantees this using a **FIFO wait queue**.

8. **Deadlock:**  
   A situation where two or more threads are permanently blocked because each thread holds a resource that the other thread requires, satisfying all four Coffman conditions: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.

9. **Lock Granularity (Coarse vs. Fine-Grained):**  
   - **Coarse-Grained Locking:** Locking the entire application or entire database with a single lock. Simple, but severely limits concurrency.
   - **Fine-Grained Locking:** Locking individual items (e.g., locking Event #1 separately from Event #2). Maximizes parallel throughput across non-conflicting resources. (Implemented via `KeyedMutexRegistry`).

10. **Atomic Operation:**  
    An operation that executes as a single, indivisible unit of work from the perspective of all other threads. It either completes entirely or leaves state completely untouched; it cannot be observed in an intermediate or partially executed state.

11. **TOCTOU (Time of Check to Time of Use):**  
    A concurrency bug where a system checks the state of a resource (e.g., `remainingCapacity > 0`) but the state changes before the system acts on that check, invalidating the decision.

12. **Spinlock vs. Sleep-Lock:**  
    - **Spinlock:** Uses busy-waiting (`while(locked);`) in user space. Consumes CPU cycles; suitable only for very short wait times in multi-core kernel code.
    - **Sleep-Lock (Yield/Blocking Lock):** Puts the waiting thread into a blocked/sleeping queue and yields the CPU to other tasks until awoken by the lock owner. (Our project uses asynchronous sleep-locks via Promises/Event Loop).

---

## 4. Code Architecture & Implementation Mapping

### 4.1 Mutex Implementation (`src/core/Mutex.js`)
```javascript
// FIFO Queue ensures Bounded Waiting (Zero Starvation)
acquire(requesterId) {
  if (!this._locked) {
    this._locked = true;
    this._currentOwner = requesterId;
    return Promise.resolve(() => this._release(requesterId));
  }
  // Lock contended: Enqueue with resolver
  return new Promise(resolve => {
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
```

### 4.2 Fine-Grained Locking (`src/core/KeyedMutexRegistry.js`)
Instead of a single global lock that would make registration for Python Workshop block registrations for Cloud Workshop, `KeyedMutexRegistry` instantiates an independent `Mutex` instance for each unique `eventId`:
```javascript
getLock(key) {
  if (!this._locks.has(key)) {
    this._locks.set(key, new Mutex(`event-${key}`));
  }
  return this._locks.get(key);
}
```

### 4.3 Atomic Critical Section (`src/services/EventService.js`)
Inside `registerUser`:
1. **Acquire:** `const release = await lock.acquire(threadId);`
2. **Execute Critical Section:**
   - Verify event exists.
   - **Duplicate Check:** Check if `userEmail` already registered. Reject with `409 DUPLICATE_REGISTRATION` if found.
   - **Capacity Check:** Check if `remainingCapacity <= 0`. Reject with `409 SOLD_OUT` if zero.
   - **Atomic State Mutation:** Decrement `remainingCapacity -= 1`, create ticket, push to attendee array, flush to disk.
3. **Release (Finally Block):** `release();` guarantees unlock even if exceptions occur, preventing deadlocks.

---

## 5. Comprehensive Viva Voce Questions & Answers

### Category 1: Fundamental OS Concepts

#### Q1: What is a Critical Section, and why does it need protection?
**Answer:**  
A Critical Section is any segment of code where shared resources (memory variables, files, tables) are accessed and updated concurrently by multiple execution contexts. If multiple threads interleave their reads and writes inside the critical section without synchronization, a Race Condition occurs, causing unpredictable state corruption, lost updates, or inconsistent data.

#### Q2: What are the three requirements an OS synchronization mechanism must satisfy to solve the Critical Section Problem?
**Answer:**  
Formulated by Edsger Dijkstra:
1. **Mutual Exclusion:** At most one process can execute in the critical section at any given moment.
2. **Progress:** If the critical section is empty and some processes want to enter, only processes not in their remainder section can participate in selecting who enters next, and this choice cannot be delayed indefinitely.
3. **Bounded Waiting:** There is a defined limit on the number of times other processes are allowed to enter the critical section after a process has requested entry, guaranteeing no process starves forever.

#### Q3: What is the fundamental difference between a Mutex and a Binary Semaphore?
**Answer:**  
- **Ownership:** A Mutex has an owner. Only the thread that locked the Mutex is legally permitted to unlock it. A Semaphore has no concept of ownership; one thread can wait (`P()`) and a completely different thread or interrupt service routine can signal (`V()`).
- **Use Case:** A Mutex is designed strictly for mutual exclusion. Semaphores are designed for both mutual exclusion and signaling (producer-consumer synchronization).
- **Priority Inversion:** Mutex implementations can support Priority Inheritance protocols to mitigate Priority Inversion; standard semaphores cannot.

#### Q4: What is the difference between Busy Waiting (Spinlock) and Blocking Synchronization?
**Answer:**  
- **Busy Waiting (Spinlock):** A thread repeatedly tests a condition in a loop (`while (test_and_set(&lock));`), consuming CPU cycles while waiting. Efficient only when lock hold times are extremely short (less than two context-switch times) and on multi-processor systems.
- **Blocking (Sleep-Lock):** When a thread cannot obtain the lock, the OS kernel transitions its state from RUNNING to BLOCKED/WAITING, enqueues it in a wait queue, and schedules another ready thread. When the lock is released, the sleeping thread is moved back to the READY queue.

---

### Category 2: Problem Scenario & Race Condition Analysis

#### Q5: Explain the exact race condition that occurs when 2 users try to register for an event with only 1 place remaining without synchronization.
**Answer:**  
This is a classic Check-Then-Act (TOCTOU) race condition:
1. Thread A reads `remainingCapacity = 1`.
2. Before Thread A decrements the value, CPU context-switches to Thread B.
3. Thread B reads `remainingCapacity = 1` (stale read).
4. Both threads evaluate `remainingCapacity > 0` as `TRUE`.
5. Thread A decrements capacity to 0 and issues Ticket A.
6. Thread B decrements capacity to -1 and issues Ticket B.  
**Result:** Overbooking. 2 tickets issued for 1 physical seat, and capacity drops below zero, violating the system invariant $C_{remaining} \ge 0$.

#### Q6: How does your project prevent this overbooking?
**Answer:**  
By enclosing the read, validation, duplicate check, and decrement operations inside an atomic Critical Section guarded by an asynchronous Mutex:
1. Thread A requests the lock, acquires it, and enters the Critical Section.
2. Thread B requests the lock, finds it held by Thread A, and is placed into a FIFO wait queue.
3. Thread A checks capacity (1 > 0), decrements capacity to 0, generates Ticket A, and releases the lock.
4. The mutex scheduler pops Thread B from the FIFO queue and grants the lock.
5. Thread B enters the Critical Section, reads the updated `remainingCapacity = 0`, evaluates the check as `FALSE`, and is safely rejected with `409 SOLD_OUT`. Remaining capacity never drops below 0.

#### Q7: How does your project satisfy Bounded Waiting?
**Answer:**  
Inside `src/core/Mutex.js`, waiting requests are stored in a JavaScript array operated as a strict **First-In, First-Out (FIFO) queue** (`this._queue.push(...)` and `this._queue.shift()`). When a lock is released, the lock is passed directly to the caller at the front of the queue. If there are $k$ requests ahead of a thread, that thread is guaranteed to acquire the lock after exactly $k$ releases, establishing an absolute upper bound of $O(k)$ wait cycles and completely eliminating starvation.

---

### Category 3: System Design & Implementation Architecture

#### Q8: Why did you implement fine-grained locking (`KeyedMutexRegistry`) instead of a single global Mutex?
**Answer:**  
A single global lock creates unnecessary lock contention and serializes independent operations. If User 1 registers for "OS Workshop" (Event #1) and User 2 registers for "Cloud Workshop" (Event #2), their shared resources are completely disjoint.  
With coarse-grained locking, User 2 would be blocked waiting for User 1's disk write.  
Our `KeyedMutexRegistry` maintains an isolated `Mutex` per event ID. Concurrency across different events runs in parallel at maximum throughput, while concurrency within the same event is strictly serialized.

#### Q9: How is duplicate registration handled under high concurrency?
**Answer:**  
Checking for duplicate emails must also occur *inside* the critical section. If two requests with the same email `shiva@example.com` arrive simultaneously:
- If duplicate checks were outside the lock, both threads would see "not registered" and both would book seats.
- Inside our critical section, Thread 1 adds the email to the attendee list. When Thread 2 enters, it inspects the array, finds `shiva@example.com` already registered, and immediately aborts with `409 DUPLICATE_REGISTRATION` without decrementing capacity.

#### Q10: How does cancellation work, and why must it also be synchronized?
**Answer:**  
Cancellation releases a previously booked seat and increments `remainingCapacity` back up to `totalCapacity`. This is also a shared-memory read-modify-write operation (`capacity += 1` and array splice). If a user cancels at the exact millisecond another user registers, unsynchronized execution could overwrite the increment or corrupt the registration array. Hence, `cancelRegistration()` also acquires the event mutex via `lock.runExclusive()`.

#### Q11: How do you prevent deadlocks in your system?
**Answer:**  
Deadlocks require four conditions (Coffman conditions): Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.
1. **No Multiple Locks Held:** Each registration or cancellation transaction requests only a single lock (the lock for that specific `eventId`). A thread never holds Event Lock A while requesting Event Lock B.
2. **Guaranteed Release via `finally`:** All lock acquisitions use a `try...finally` block. Even if an unhandled error, database failure, or exception is thrown inside the critical section, `release()` is executed in the `finally` block, preventing orphaned held locks.

---

### Category 4: Advanced Systems & Distributed Scenarios

#### Q12: How would you scale this Mutex implementation from a single Node.js process to a distributed cluster of servers?
**Answer:**  
An in-memory Mutex is bound to a single OS process/JVM/V8 instance. When running across multiple servers behind a load balancer, threads run on different physical machines with separate RAM.  
To scale to a distributed system, we would replace the in-memory Mutex with:
1. **Distributed Lock Manager (DLM):** Using Redis with the **Redlock algorithm** or atomic Lua scripts (`SET resource_name my_random_value NX PX 30000`).
2. **Database Row-Level Locking:** In PostgreSQL/MySQL, using `SELECT remaining_capacity FROM events WHERE id = 1 FOR UPDATE;` inside an ACID transaction.
3. **Optimistic Concurrency Control (OCC):** Using version numbers (`UPDATE events SET remaining = remaining - 1, version = version + 1 WHERE id = 1 AND version = current_version;`).

#### Q13: What is Priority Inversion, and how do real-time operating systems solve it?
**Answer:**  
Priority Inversion occurs when a lower-priority task $L$ holds a resource required by a high-priority task $H$, but task $L$ cannot complete and release the lock because it is preempted by a medium-priority task $M$. Thus, $M$ indirectly delays $H$.  
**Solution:**
- **Priority Inheritance Protocol:** When $H$ blocks waiting for a lock held by $L$, task $L$ temporarily inherits the higher priority of $H$ until it releases the lock, preventing medium-priority tasks from preempting it.
- **Priority Ceiling Protocol:** Each lock is assigned a priority ceiling equal to the highest priority task that may ever lock it.

#### Q14: What hardware instructions enable atomic synchronization primitives in modern CPUs?
**Answer:**  
CPUs provide atomic read-modify-write instructions:
- **Test-and-Set (TAS):** Atomically writes 1 to a memory location and returns its old value.
- **Compare-And-Swap (CAS):** Atomically compares the contents of a memory location to a given value, and only if they are equal, modifies it to a new given value (e.g., `cmpxchg` on x86).
- **Load-Linked / Store-Conditional (LL/SC):** Used in ARM and RISC-V architectures to implement lock-free synchronization.

---

## 6. Project Verification & Demonstration Guide

### How to Run in Front of Evaluators:
1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd C:\Users\DELL\.gemini\antigravity\scratch\event-registration-mutex-system
   ```

2. Run the automated test suite:
   ```powershell
   node tests/run-tests.js
   ```
   *Points to show examiner:* 7/7 tests pass, including proof of Mutual Exclusion, FIFO Bounded Waiting, Duplicate Rejection, and the live Race Condition demonstration.

3. Run the high-concurrency stress test (50 threads vs 2 seats):
   ```powershell
   node tests/concurrency-stress-test.js
   ```
   *Points to show examiner:* 50 simultaneous threads compete for 2 seats. Under Mutex, exactly 2 succeed, 48 are cleanly rejected, and capacity is exactly 0. Under Unsafe mode, overbooking drops capacity to -18.

4. Start the live interactive web platform:
   ```powershell
   node server.js
   ```
   *Access URLs:*
   - **Interactive Dashboard & Concurrency Lab:** [http://localhost:3000](http://localhost:3000)
   - **Live Academic Presentation Deck:** [http://localhost:3000/presentation](http://localhost:3000/presentation)
   - **Academic Lab Report:** [http://localhost:3000/report](http://localhost:3000/report)
   - **Admin Management Portal:** [http://localhost:3000/admin](http://localhost:3000/admin)
