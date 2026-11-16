/**
 * BookingService - Real-Time Concurrency & Tatkal Booking Engine
 * 
 * Simulates high-throughput IRCTC Tatkal ticket booking contention:
 * 1. Mutex Protected Mode: Strict atomic critical section with Distributed Lock Manager
 *    guarantees ZERO overselling across multiple devices and serverless containers.
 * 2. Mutex Disabled Mode: Bypasses synchronization to demonstrate Time-Of-Check to Time-Of-Use
 *    (TOCTOU) race conditions, resulting in oversold tickets (negative remaining capacity).
 */

const db = require('../storage/Database');
const { defaultRegistry } = require('../core/KeyedMutexRegistry');
const dlm = require('../core/DistributedLockManager');

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

    // Query global distributed state to guarantee synchronization across separate serverless containers & devices
    const globalState = await dlm.getGlobalEventState(hackathon_id);
    const mutexEnabled = (globalState && globalState.mutex_enabled !== undefined)
      ? globalState.mutex_enabled
      : event.mutex_enabled;

    const useMutex = force_no_mutex ? false : mutexEnabled;
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
        seats_remaining: globalState && globalState.remaining !== undefined ? globalState.remaining : event.remaining_tickets,
        message: `Team '${team_name}' queued for Tatkal lock.`
      });

      const startTime = Date.now();
      // Acquire both local in-memory Mutex and cross-instance Distributed Lock
      const releaseLock = await dlm.acquire(hackathon_id, threadId, team_name);

      try {
        const waitDuration = Date.now() - startTime;
        const currentEvent = db.getHackathonById(hackathon_id);

        db.addAuditLog({
          event_id: hackathon_id,
          action: "CRITICAL_SECTION_ENTER",
          thread_id: threadId,
          team_name,
          lock_state: "LOCKED",
          wait_duration_ms: waitDuration,
          seats_remaining: currentEvent.remaining_tickets,
          message: `Lock granted. Team '${team_name}' entered Critical Section (Waited ${waitDuration}ms).`
        });

        // 1. Realistic Processing Delay (Payment Verification & Cryptographic Token Generation)
        await sleep(effectiveDelay);

        // 2. ATOMIC SEAT RESERVATION VIA DISTRIBUTED LOCK MANAGER
        const reservation = await dlm.atomicallyReserveSeat(hackathon_id, threadId, team_name);

        // If distributed lock manager reports SOLD_OUT, or if fallback local inventory <= 0:
        if (reservation.status === "SOLD_OUT" || (!reservation.fallback && !reservation.success)) {
          db.updateHackathon(hackathon_id, {
            remaining_tickets: 0,
            badge: "SOLD OUT"
          });

          db.addAuditLog({
            event_id: hackathon_id,
            action: "TATKAL_QUOTA_EXHAUSTED",
            thread_id: threadId,
            team_name,
            lock_state: "LOCKED",
            seats_remaining: 0,
            message: `Booking REJECTED. Tatkal quota exhausted (0 seats left).`
          });

          return {
            success: false,
            status: "SOLD_OUT",
            message: "Tatkal quota completely exhausted. No seats remaining.",
            threadId,
            seats_remaining: 0
          };
        }

        // Local fallback check if remote was unavailable
        if (reservation.fallback && currentEvent.remaining_tickets <= 0) {
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
        const updatedSeats = reservation.remaining !== undefined
          ? reservation.remaining
          : currentEvent.remaining_tickets - 1;

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
        await releaseLock();
      }
    }

    // -------------------------------------------------------------
    // PATH B: MUTEX DISABLED (Vulnerable TOCTOU Race Condition)
    // -------------------------------------------------------------
    else {
      const currentGlobal = await dlm.getGlobalEventState(hackathon_id);
      const cachedSeatsAtCheck = (currentGlobal && currentGlobal.remaining !== undefined)
        ? currentGlobal.remaining
        : event.remaining_tickets;

      db.addAuditLog({
        event_id: hackathon_id,
        action: "MUTEX_BYPASSED",
        thread_id: threadId,
        team_name,
        lock_state: "UNPROTECTED",
        seats_remaining: cachedSeatsAtCheck,
        message: `[RACE CONDITION RISK] Team '${team_name}' accessing shared state without lock.`
      });

      // 1. NON-ATOMIC SNAPSHOT READ (simulates SELECT remaining_tickets into local variable)
      // 2. Interleaved Asynchronous Window:
      // While this thread pauses, other concurrent threads also read the identical remaining_tickets!
      await sleep(effectiveDelay);

      // 3. TOCTOU DIRTY EVALUATE:
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
      const reservation = await dlm.dirtyReserveSeat(hackathon_id, threadId, team_name);
      const liveLatest = db.getHackathonById(hackathon_id);
      const updatedSeats = reservation.remaining !== undefined
        ? reservation.remaining
        : liveLatest.remaining_tickets - 1; // Drops below zero!

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
    hackathon_id = 1,
    num_teams = 6,
    with_mutex = true
  }) {
    const event = db.getHackathonById(hackathon_id);
    if (!event) throw new Error("Hackathon not found");

    const initialSeats = event.remaining_tickets;
    const initialBadge = event.badge;

    // Reset event remaining tickets to baseline for clean repeatable demonstration
    const baselineSeats = initialSeats <= 0 ? 2 : initialSeats;
    db.updateHackathon(hackathon_id, { remaining_tickets: baselineSeats, mutex_enabled: with_mutex });
    await dlm.setGlobalEventCapacity(hackathon_id, baselineSeats);

    db.addAuditLog({
      event_id: hackathon_id,
      action: "CONCURRENCY_RUSH_START",
      thread_id: "SIM-RUNNER",
      team_name: "ORCHESTRATOR",
      lock_state: with_mutex ? "MUTEX_ENABLED" : "MUTEX_DISABLED",
      seats_remaining: baselineSeats,
      message: `🚀 Launching ${num_teams} concurrent checkout threads (Mutex: ${with_mutex ? 'ON' : 'OFF'}).`
    });

    const squadNames = [
      "AlphaKnights", "ByteBandits", "CyberSpartans",
      "DevDynamos", "EchoEnigmas", "FluxFounders",
      "GigaGlitch", "HyperHackers", "InfraInovators"
    ];

    const teamPromises = [];

    for (let i = 0; i < num_teams; i++) {
      const name = squadNames[i] || `Squad_${i + 1}`;
      teamPromises.push(
        this.bookTatkalTicket({
          hackathon_id,
          team_name: name,
          leader_name: `Leader ${name}`,
          leader_email: `${name.toLowerCase()}@sru.edu.in`,
          members: [
            { name: `Dev 1 (${name})`, email: `dev1.${name.toLowerCase()}@sru.edu.in`, role: "Coder" }
          ],
          payment_details: { payment_id: `sim_pay_${Date.now()}_${i}` },
          force_no_mutex: !with_mutex,
          delay_ms: with_mutex ? SIMULATED_IO_DELAY_MS : 80 // Tight overlap window for simulated rush
        })
      );
    }

    // Fire all N requests simultaneously at the exact same tick
    const results = await Promise.all(teamPromises);

    const successful = results.filter(r => r.success && r.status !== "OVERSOLD");
    const oversold = results.filter(r => r.status === "OVERSOLD");
    const rejected = results.filter(r => !r.success || r.status === "SOLD_OUT");

    const finalEvent = db.getHackathonById(hackathon_id);
    const finalSeats = finalEvent.remaining_tickets;

    // Invariant Verification: 0 <= remaining_tickets <= total_tickets
    const invariantPreserved = finalSeats >= 0 && oversold.length === 0;

    const summary = {
      timestamp: new Date().toISOString(),
      hackathon_id,
      event_title: event.title,
      with_mutex,
      num_requests: num_teams,
      initial_seats: baselineSeats,
      final_remaining_seats: finalSeats,
      tickets_confirmed: successful.length,
      oversold_tickets: oversold.length,
      requests_rejected: rejected.length,
      invariant_preserved: invariantPreserved,
      race_condition_detected: !invariantPreserved,
      results
    };

    db.addAuditLog({
      event_id: hackathon_id,
      action: "CONCURRENCY_RUSH_COMPLETE",
      thread_id: "SIM-RUNNER",
      team_name: "ORCHESTRATOR",
      lock_state: with_mutex ? "MUTEX_ENABLED" : "MUTEX_DISABLED",
      seats_remaining: finalSeats,
      message: invariantPreserved
        ? `✅ System Invariant PRESERVED: Capacity bounded [0, ${event.total_tickets}]. Confirmed: ${successful.length}, Rejected: ${rejected.length}.`
        : `🚨 RACE CONDITION CONFIRMED: System oversold by ${Math.abs(finalSeats)} tickets! Invariant VIOLATED.`
    });

    return summary;
  }
}

const bookingService = new BookingService();
module.exports = bookingService;
