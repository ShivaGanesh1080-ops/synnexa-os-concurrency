/**
 * BookingService - Real-Time Concurrency & Tatkal Booking Engine
 * 
 * Simulates high-throughput IRCTC Tatkal ticket booking contention:
 * 1. Mutex Protected Mode: Strict atomic critical section guarantees ZERO overselling.
 * 2. Mutex Disabled Mode: Bypasses synchronization to demonstrate Time-Of-Check to Time-Of-Use
 *    (TOCTOU) race conditions, resulting in oversold tickets (negative remaining capacity).
 */

const db = require('../storage/Database');
const { defaultRegistry } = require('../core/KeyedMutexRegistry');

// Processing delay simulating network I/O, Razorpay verification & cryptographic ticket signing
const SIMULATED_IO_DELAY_MS = 40;
// Extended TOCTOU window for manual multi-device live demonstrations (Teacher vs Friend)
const MANUAL_RACE_WINDOW_MS = 2500;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

class BookingService {
  /**
   * Book a Tatkal Ticket for a Team.
   * 
   * @param {Object} params
   * @param {number|string} params.hackathon_id - Target event ID
   * @param {string} params.team_name - Registered team name
   * @param {string} params.leader_name - Team leader name
   * @param {string} params.leader_email - Team leader email
   * @param {Array} params.members - Array of team members
   * @param {Object} params.payment_details - Razorpay test payment info
   * @param {boolean} [params.force_no_mutex] - Override to deliberately simulate race condition
   */
  async bookTatkalTicket({
    hackathon_id,
    team_name,
    leader_name,
    leader_email,
    members = [],
    payment_details = {},
    force_no_mutex = false,
    delay_ms = null
  }) {
    const threadId = `th-${Date.now().toString().slice(-4)}-${Math.floor(Math.random() * 900 + 100)}`;
    const event = db.getHackathonById(hackathon_id);

    if (!event) {
      throw new Error(`Hackathon with ID ${hackathon_id} not found.`);
    }

    const useMutex = force_no_mutex ? false : event.mutex_enabled;
    const mutex = defaultRegistry.get(hackathon_id);
    const effectiveDelay = delay_ms !== null 
      ? delay_ms 
      : (useMutex ? SIMULATED_IO_DELAY_MS : MANUAL_RACE_WINDOW_MS);

    // -------------------------------------------------------------
    // PATH A: MUTEX PROTECTED (Atomic Critical Section - ACID)
    // -------------------------------------------------------------
    if (useMutex) {
      db.addAuditLog({
        event_id: hackathon_id,
        action: "LOCK_REQUESTED",
        thread_id: threadId,
        team_name,
        lock_state: "WAITING",
        seats_remaining: event.remaining_tickets,
        message: `Team '${team_name}' queued for Tatkal lock.`
      });

      const startTime = Date.now();
      const releaseLock = await mutex.acquire(threadId, team_name);

      try {
        const waitDuration = Date.now() - startTime;
        db.addAuditLog({
          event_id: hackathon_id,
          action: "CRITICAL_SECTION_ENTER",
          thread_id: threadId,
          team_name,
          lock_state: "LOCKED",
          wait_duration_ms: waitDuration,
          seats_remaining: event.remaining_tickets,
          message: `Lock granted. Team '${team_name}' entered Critical Section (Waited ${waitDuration}ms).`
        });

        // 1. READ: Query latest real-time inventory
        const currentEvent = db.getHackathonById(hackathon_id);

        // 2. Realistic Processing Delay (Payment Verification & Cryptographic Token Generation)
        await sleep(effectiveDelay);

        // 3. EVALUATE & MODIFY: Atomic Inventory Check
        if (currentEvent.remaining_tickets <= 0) {
          db.addAuditLog({
            event_id: hackathon_id,
            action: "TATKAL_QUOTA_EXHAUSTED",
            thread_id: threadId,
            team_name,
            lock_state: "LOCKED",
            seats_remaining: currentEvent.remaining_tickets,
            message: `Booking REJECTED. Tatkal quota exhausted (0 seats left).`
          });

          return {
            success: false,
            status: "SOLD_OUT",
            message: "Tatkal quota completely exhausted. No seats remaining.",
            threadId,
            seats_remaining: currentEvent.remaining_tickets
          };
        }

        // Decrement remaining seats atomically inside Critical Section
        const updatedSeats = currentEvent.remaining_tickets - 1;
        db.updateHackathon(hackathon_id, {
          remaining_tickets: updatedSeats,
          badge: updatedSeats === 0 ? "SOLD OUT" : `${updatedSeats} Seats Left`
        });

        // Create confirmed team booking
        const teamBooking = db.createTeamBooking({
          hackathon_id,
          team_name,
          leader_name,
          leader_email,
          members,
          payment_status: payment_details.payment_id ? "PAID_RAZORPAY_TEST" : "CONFIRMED",
          payment_id: payment_details.payment_id || `rzp_mock_${Date.now()}`
        });

        db.addAuditLog({
          event_id: hackathon_id,
          action: "BOOKING_SUCCESS",
          thread_id: threadId,
          team_name,
          lock_state: "LOCKED",
          ticket_code: teamBooking.ticket_code,
          seats_remaining: updatedSeats,
          message: `Ticket ${teamBooking.ticket_code} issued to '${team_name}'. Seats remaining: ${updatedSeats}.`
        });

        return {
          success: true,
          status: "CONFIRMED",
          message: "Tatkal ticket successfully booked under Mutex protection!",
          ticket: teamBooking,
          booking: teamBooking,
          threadId,
          seats_remaining: updatedSeats
        };

      } finally {
        db.addAuditLog({
          event_id: hackathon_id,
          action: "CRITICAL_SECTION_EXIT",
          thread_id: threadId,
          team_name,
          lock_state: "UNLOCKED",
          message: `Lock released by '${team_name}'. Next waiter alerted.`
        });
        releaseLock();
      }
    }

    // -------------------------------------------------------------
    // PATH B: MUTEX DISABLED (Vulnerable TOCTOU Race Condition)
    // -------------------------------------------------------------
    else {
      db.addAuditLog({
        event_id: hackathon_id,
        action: "MUTEX_BYPASSED",
        thread_id: threadId,
        team_name,
        lock_state: "UNPROTECTED",
        seats_remaining: event.remaining_tickets,
        message: `[RACE CONDITION RISK] Team '${team_name}' accessing shared state without lock.`
      });

      // 1. NON-ATOMIC SNAPSHOT READ (simulates SELECT remaining_tickets into local variable)
      const cachedSeatsAtCheck = event.remaining_tickets;

      // 2. Interleaved Asynchronous Window:
      // While this thread pauses, other concurrent threads also read the identical remaining_tickets!
      await sleep(effectiveDelay);

      // 3. TOCTOU DIRTY EVALUATE:
      // Thread evaluates cached variable or outdated local state
      if (cachedSeatsAtCheck <= 0) {
        db.addAuditLog({
          event_id: hackathon_id,
          action: "REJECTED_DIRTY_READ",
          thread_id: threadId,
          team_name,
          lock_state: "UNPROTECTED",
          seats_remaining: cachedSeatsAtCheck,
          message: `Booking failed due to zero seats on dirty check.`
        });
        return {
          success: false,
          status: "SOLD_OUT",
          message: "Seats unavailable.",
          threadId,
          seats_remaining: cachedSeatsAtCheck
        };
      }

      // 4. OVERWRITING WRITE: Decrements regardless of interleaved concurrent writes
      // Re-fetching latest DB object simulates blind dirty write
      const liveLatest = db.getHackathonById(hackathon_id);
      const updatedSeats = liveLatest.remaining_tickets - 1; // Drops below zero!

      db.updateHackathon(hackathon_id, {
        remaining_tickets: updatedSeats,
        badge: updatedSeats < 0 ? `⚠️ OVERBOOKED (${updatedSeats})` : `${updatedSeats} Seats Left`
      });

      const teamBooking = db.createTeamBooking({
        hackathon_id,
        team_name,
        leader_name,
        leader_email,
        members,
        payment_status: "RACE_CONDITION_DIRTY_WRITE",
        payment_id: payment_details.payment_id || `rzp_mock_${Date.now()}`
      });

      db.addAuditLog({
        event_id: hackathon_id,
        action: updatedSeats < 0 ? "RACE_CONDITION_OVERSOLD" : "DIRTY_WRITE_SUCCESS",
        thread_id: threadId,
        team_name,
        lock_state: "UNPROTECTED",
        ticket_code: teamBooking.ticket_code,
        seats_remaining: updatedSeats,
        message: updatedSeats < 0
          ? `🚨 RACE HAZARD! '${team_name}' booked ticket beyond capacity! Seats are now ${updatedSeats}.`
          : `Ticket issued without lock to '${team_name}'. Seats remaining: ${updatedSeats}.`
      });

      return {
        success: true,
        status: updatedSeats < 0 ? "OVERSOLD" : "CONFIRMED_UNPROTECTED",
        message: updatedSeats < 0
          ? `WARNING: Ticket booked but system is OVERBOOKED (${updatedSeats} seats)! Race condition confirmed.`
          : `Booked without mutex protection.`,
        ticket: teamBooking,
        booking: teamBooking,
        threadId,
        seats_remaining: updatedSeats
      };
    }
  }

  /**
   * Run a Live Concurrency Rush Simulation
   * Directly launches N simultaneous asynchronous booking promises at the exact same millisecond.
   */
  async runConcurrentRush({
    hackathon_id,
    num_teams = 6,
    with_mutex = true
  }) {
    const event = db.getHackathonById(hackathon_id);
    if (!event) throw new Error("Hackathon not found");

    const initialSeats = event.remaining_tickets;
    const teamNames = [
      "AlphaKernels",
      "ByteBusters",
      "CipherStorm",
      "DevDynamos",
      "EchoTracer",
      "ForkBombSquad",
      "GhostThreads",
      "HexHacks",
      "IronCladLocks",
      "JavaJVMWarriors"
    ];

    const teamsToTest = teamNames.slice(0, num_teams).map((name, idx) => ({
      hackathon_id,
      team_name: name,
      leader_name: `Leader ${name}`,
      leader_email: `${name.toLowerCase()}@hack.org`,
      members: [
        { name: `Leader ${name}`, role: "Captain", email: `${name.toLowerCase()}@hack.org`, htno: `2503A511${idx}` },
        { name: `Hacker ${name} 2`, role: "Developer", email: `dev.${name.toLowerCase()}@hack.org`, htno: `2503A512${idx}` }
      ],
      payment_details: { payment_id: `rzp_rush_${Date.now()}_${idx}` },
      force_no_mutex: !with_mutex,
      delay_ms: 30
    }));

    db.addAuditLog({
      event_id: hackathon_id,
      action: "CONCURRENCY_RUSH_START",
      thread_id: "SIMULATOR",
      team_name: "BATCH_RUNNER",
      lock_state: with_mutex ? "MUTEX_ENABLED" : "MUTEX_DISABLED",
      seats_remaining: initialSeats,
      message: `🚀 Launching ${num_teams} simultaneous requests against ${initialSeats} remaining seats (Mutex: ${with_mutex ? 'ON' : 'OFF'}).`
    });

    const startTime = Date.now();
    // Execute all bookings at the exact same instant
    const results = await Promise.all(
      teamsToTest.map(t => this.bookTatkalTicket(t))
    );
    const durationMs = Date.now() - startTime;

    const finalEvent = db.getHackathonById(hackathon_id);
    const successful = results.filter(r => r.success);
    const rejected = results.filter(r => !r.success);
    const isOversold = finalEvent.remaining_tickets < 0;
    const oversoldCount = isOversold ? Math.abs(finalEvent.remaining_tickets) : 0;

    const summary = {
      hackathon_id,
      mode: with_mutex ? "MUTEX_PROTECTED (ACID / IRCTC)" : "VULNERABLE (RACE CONDITION)",
      initial_seats: initialSeats,
      requests_fired: num_teams,
      successful_bookings: successful.length,
      rejected_requests: rejected.length,
      final_remaining_seats: finalEvent.remaining_tickets,
      is_oversold: isOversold,
      oversold_count: oversoldCount,
      duration_ms: durationMs,
      results
    };

    db.addAuditLog({
      event_id: hackathon_id,
      action: "CONCURRENCY_RUSH_COMPLETE",
      thread_id: "SIMULATOR",
      team_name: "BATCH_RUNNER",
      lock_state: with_mutex ? "MUTEX_ENABLED" : "MUTEX_DISABLED",
      seats_remaining: finalEvent.remaining_tickets,
      message: with_mutex
        ? `✅ Rush Complete in ${durationMs}ms: Zero overselling. ${successful.length} confirmed, ${rejected.length} rejected.`
        : `⚠️ Rush Complete in ${durationMs}ms: RACE CONDITION PROVED! ${oversoldCount} excess tickets oversold.`
    });

    return summary;
  }
}

const bookingServiceInstance = new BookingService();
module.exports = bookingServiceInstance;
