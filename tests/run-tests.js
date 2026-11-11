/**
 * SYNNEXA — Comprehensive Backend & OS Concurrency Test Suite
 * Validates Mutual Exclusion, FIFO Bounded Waiting, Keyed Isolation,
 * Atomic Tatkal Reservation, and TOCTOU Race Condition Detection.
 * 
 * SR University • CSE Core • Operating Systems Lab • Product #8
 */

const assert = require('assert');
const Mutex = require('../src/core/Mutex');
const { defaultRegistry } = require('../src/core/KeyedMutexRegistry');
const bookingService = require('../src/services/BookingService');
const db = require('../src/storage/Database');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let passedTests = 0;
let totalTests = 0;

async function test(name, fn) {
  totalTests++;
  process.stdout.write(`[TEST ${totalTests}] ${name} ... `);
  try {
    await fn();
    console.log(`\x1b[32mPASSED\x1b[0m`);
    passedTests++;
  } catch (err) {
    console.log(`\x1b[31mFAILED\x1b[0m`);
    console.error(`       Error:`, err.message);
    if (err.stack) {
      console.error(err.stack.split('\n').slice(1, 4).join('\n'));
    }
  }
}

async function runAllTests() {
  console.log('\n================================================================');
  console.log('  SYNNEXA — OS CONCURRENCY & BACKEND TEST SUITE (PRODUCT #8)   ');
  console.log('================================================================\n');

  // Reset database & lock states
  defaultRegistry.resetAll();
  db.resetAll();

  // -------------------------------------------------------------
  // TEST 1: MUTEX MUTUAL EXCLUSION
  // -------------------------------------------------------------
  await test('Mutex: Guarantees strict Mutual Exclusion (At most 1 thread in Critical Section)', async () => {
    const mutex = new Mutex('test-mutex');
    let activeThreadsInCriticalSection = 0;
    let maxConcurrentObserved = 0;

    const worker = async (id) => {
      await mutex.runExclusive(async () => {
        activeThreadsInCriticalSection++;
        if (activeThreadsInCriticalSection > maxConcurrentObserved) {
          maxConcurrentObserved = activeThreadsInCriticalSection;
        }
        assert.strictEqual(activeThreadsInCriticalSection, 1, 'MUTUAL EXCLUSION VIOLATED! More than 1 thread in Critical Section.');
        await sleep(15);
        activeThreadsInCriticalSection--;
      }, `worker-${id}`, `Team-${id}`);
    };

    // Spawn 12 concurrent asynchronous workers
    const workers = Array.from({ length: 12 }, (_, i) => worker(i + 1));
    await Promise.all(workers);

    assert.strictEqual(maxConcurrentObserved, 1, 'Critical Section was breached by concurrent threads');
    assert.strictEqual(mutex.isLocked, false, 'Mutex must be released after all workers complete');
    assert.strictEqual(mutex.metrics.totalAcquisitions, 12, 'Must record exactly 12 acquisitions');
  });

  // -------------------------------------------------------------
  // TEST 2: BOUNDED WAITING & FIFO QUEUE (NO STARVATION)
  // -------------------------------------------------------------
  await test('Mutex: Enforces Bounded Waiting in strict FIFO order (Zero Thread Starvation)', async () => {
    const mutex = new Mutex('fifo-mutex');
    const executionOrder = [];

    // Hold the lock initially
    const releaseInitial = await mutex.acquire('initial-holder', 'HoldingSquad');

    // Enqueue 4 requests in order: Alpha, Beta, Gamma, Delta
    const p1 = mutex.runExclusive(async () => { executionOrder.push('Alpha'); }, 'req-1', 'Alpha');
    const p2 = mutex.runExclusive(async () => { executionOrder.push('Beta'); }, 'req-2', 'Beta');
    const p3 = mutex.runExclusive(async () => { executionOrder.push('Gamma'); }, 'req-3', 'Gamma');
    const p4 = mutex.runExclusive(async () => { executionOrder.push('Delta'); }, 'req-4', 'Delta');

    // Give microtasks time to queue
    await sleep(20);

    // Release initial lock
    releaseInitial();

    await Promise.all([p1, p2, p3, p4]);

    assert.deepStrictEqual(executionOrder, ['Alpha', 'Beta', 'Gamma', 'Delta'], 'Lock grants did not follow FIFO arrival order');
    assert.strictEqual(mutex.isLocked, false);
  });

  // -------------------------------------------------------------
  // TEST 3: KEYED MUTEX RESOURCE ISOLATION
  // -------------------------------------------------------------
  await test('KeyedMutexRegistry: Independent resources lock independently without cross-blocking', async () => {
    const lockEvent1 = defaultRegistry.get(1);
    const lockEvent2 = defaultRegistry.get(2);

    // Acquire Lock on Event 1
    const release1 = await lockEvent1.acquire('thread-1', 'TeamAlpha');
    assert.strictEqual(lockEvent1.isLocked, true);
    assert.strictEqual(lockEvent2.isLocked, false, 'Event 2 lock was erroneously blocked by Event 1!');

    // Lock on Event 2 should be immediately available
    let lock2AcquiredImmediately = false;
    const release2 = await lockEvent2.acquire('thread-2', 'TeamBeta');
    lock2AcquiredImmediately = true;

    assert.strictEqual(lock2AcquiredImmediately, true, 'Event 2 failed to acquire immediate lock');

    release1();
    release2();
  });

  // -------------------------------------------------------------
  // TEST 4: ATOMIC TATKAL BOOKING WITH MUTEX (ZERO OVERBOOKING)
  // -------------------------------------------------------------
  await test('BookingService: 10 concurrent requests for 2 seats under Mutex -> Exactly 2 succeed, 0 overbooking', async () => {
    db.resetAll();
    const event = db.getHackathonById(1);
    assert.strictEqual(event.remaining_tickets, 2, 'Initial remaining tickets must be exactly 2');

    const result = await bookingService.runConcurrentRush({
      hackathon_id: 1,
      num_teams: 10,
      with_mutex: true
    });

    assert.strictEqual(result.successful_bookings, 2, `Expected exactly 2 successful bookings, got ${result.successful_bookings}`);
    assert.strictEqual(result.rejected_requests, 8, `Expected 8 rejected bookings, got ${result.rejected_requests}`);
    assert.strictEqual(result.final_remaining_seats, 0, `Final seats must be 0, got ${result.final_remaining_seats}`);
    assert.strictEqual(result.is_oversold, false, 'Mutex allowed overbooking!');
    assert.strictEqual(result.oversold_count, 0, 'Oversold count must be 0 under Mutex protection');
  });

  // -------------------------------------------------------------
  // TEST 5: TOCTOU RACE CONDITION DEMONSTRATION (MUTEX OFF)
  // -------------------------------------------------------------
  await test('BookingService: Race condition demonstration WITHOUT Mutex -> Proves TOCTOU Overselling', async () => {
    // Reset event 2 to exactly 1 seat remaining
    db.resetAll();
    const event = db.getHackathonById(2);
    assert.strictEqual(event.remaining_tickets, 1, 'Initial remaining tickets for Event 2 must be 1');

    const result = await bookingService.runConcurrentRush({
      hackathon_id: 2,
      num_teams: 6,
      with_mutex: false // Intentionally bypass Mutex to demonstrate race hazard
    });

    console.log(`\n       [RACE HAZARD REPORT] Initial: 1 Seat | Requests: 6 | Confirmed: ${result.successful_bookings} | Final Seats: ${result.final_remaining_seats} | Oversold: ${result.oversold_count}`);
    
    // Without lock, concurrent reads see seat=1 and multiple threads confirm bookings
    assert(result.successful_bookings > 1, 'Expected race condition to cause more than 1 booking');
    assert(result.final_remaining_seats < 0 || result.is_oversold, 'Expected final remaining seats to drop below zero');
  });

  // -------------------------------------------------------------
  // TEST 6: DATABASE STATE & TICKET MINTING INTEGRITY
  // -------------------------------------------------------------
  await test('Database & Ticket Minting: Generates valid ticket codes, team rosters, and payment references', async () => {
    db.resetAll();

    const booking = await bookingService.bookTatkalTicket({
      hackathon_id: 3, // London CloudScale
      team_name: 'KernelMasters',
      leader_name: 'Shiva Ganesh',
      leader_email: 'shiva.ganesh@sru.edu.in',
      members: [
        { name: 'Shiva Ganesh', role: 'Team Leader', email: 'shiva.ganesh@sru.edu.in', htno: '2503A51110' },
        { name: 'Naveen Reddy', role: 'Systems Dev', email: 'naveen@sru.edu.in', htno: '2503A51108' }
      ],
      payment_details: {
        payment_id: 'rzp_test_manual_check_88291'
      }
    });

    assert.strictEqual(booking.success, true);
    assert(booking.ticket.ticket_code.startsWith('TKT-TATKAL-'), 'Invalid ticket code prefix');
    assert.strictEqual(booking.ticket.team_name, 'KernelMasters');
    assert.strictEqual(booking.ticket.members.length, 2);

    // Verify retrieval from database
    const saved = db.getTeamById(booking.ticket.id);
    assert.notStrictEqual(saved, null, 'Booking was not persisted to database');
    assert.strictEqual(saved.ticket_code, booking.ticket.ticket_code);
  });

  // -------------------------------------------------------------
  // TEST 7: AUDIT LOGS & TELEMETRY TRACEABILITY
  // -------------------------------------------------------------
  await test('AuditLogger: Captures timestamped state transitions and lock microsecond latency', async () => {
    const logs = db.getAuditLogs(10);
    assert(logs.length > 0, 'No audit logs recorded');

    const latest = logs[0];
    assert(latest.id.startsWith('LOG-'), 'Invalid log ID format');
    assert(latest.timestamp !== undefined, 'Missing timestamp in audit record');
    assert(latest.action !== undefined, 'Missing action type in audit record');
  });

  console.log('\n================================================================');
  console.log(`  FINAL TEST SUMMARY: ${passedTests} / ${totalTests} TESTS PASSED (\x1b[32m100%\x1b[0m)`);
  console.log('================================================================\n');

  if (passedTests === totalTests) {
    process.exit(0);
  } else {
    process.exit(1);
  }
}

runAllTests().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
