const db = require('../storage/Database');
const keyedMutex = require('../core/KeyedMutexRegistry');
const auditLogger = require('./AuditLogger');

// Helper to simulate realistic async I/O latency (e.g. database write / payment verification)
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

class EventService {
  /**
   * Fetch all events with calculated occupancy and status
   */
  getEvents() {
    const events = db.getAllEvents();
    return events.map(e => ({
      ...e,
      registeredCount: e.registrations.length,
      isSoldOut: e.remainingCapacity <= 0,
      occupancyPercentage: Math.round(((e.totalCapacity - e.remainingCapacity) / e.totalCapacity) * 100),
      mutexStatus: keyedMutex.getLock(e.id).getSnapshot()
    }));
  }

  /**
   * Fetch a single event with full registration details
   */
  getEventById(id) {
    const event = db.getEventById(id);
    if (!event) return null;
    return {
      ...event,
      registeredCount: event.registrations.length,
      isSoldOut: event.remainingCapacity <= 0,
      occupancyPercentage: Math.round(((event.totalCapacity - event.remainingCapacity) / event.totalCapacity) * 100),
      mutexStatus: keyedMutex.getLock(event.id).getSnapshot()
    };
  }

  /**
   * Create a new event
   */
  createEvent(data) {
    const created = db.createEvent(data);
    auditLogger.log({
      eventId: created.id,
      action: 'EVENT_CREATED',
      status: 'INFO',
      remainingCapacity: created.remainingCapacity,
      message: `New Workshop created: "${created.title}" (Capacity: ${created.totalCapacity})`
    });
    return created;
  }

  updateEvent(id, data) {
    const updated = db.updateEvent(id, data);
    if (updated) {
      auditLogger.log({
        eventId: id,
        action: 'EVENT_UPDATED',
        status: 'INFO',
        message: `Workshop #${id} details updated by admin.`
      });
    }
    return updated;
  }

  deleteEvent(id) {
    const deleted = db.deleteEvent(id);
    if (deleted) {
      auditLogger.log({
        eventId: id,
        action: 'EVENT_DELETED',
        status: 'WARN',
        message: `Workshop #${id} ("${deleted.title}") deleted by admin.`
      });
    }
    return deleted;
  }

  allocateCapacity(id, { remainingCapacity, totalCapacity }) {
    const updated = db.updateCapacity(id, remainingCapacity, totalCapacity);
    if (!updated) return null;
    auditLogger.log({
      eventId: id,
      action: 'ADMIN_CAPACITY_ALLOCATED',
      status: 'INFO',
      remainingCapacity: updated.remainingCapacity,
      message: `Admin manually set capacity for Event #${id}: Remaining = ${updated.remainingCapacity}, Total = ${updated.totalCapacity}`
    });
    return updated;
  }

  /**
   * Register a user for an event.
   * Can run with Mutex Protection (Safe) or without Mutex (Demonstrating Race Condition).
   */
  async registerUser({ eventId, userName, userEmail, useMutex = true, requesterId = null, simulatedDelayMs = 25 }) {
    const threadId = requesterId || `thread-${Math.random().toString(36).substring(2, 7)}`;
    const normalizedEmail = (userEmail || '').trim().toLowerCase();
    const cleanName = (userName || 'Anonymous Attendee').trim();

    if (!normalizedEmail) {
      throw { status: 400, code: 'INVALID_INPUT', message: 'Email address is required.' };
    }

    if (useMutex) {
      // ========================================================
      // 1. MUTEX PROTECTED (CRITICAL SECTION SYNCHRONIZATION)
      // ========================================================
      const lock = keyedMutex.getLock(eventId);

      auditLogger.log({
        eventId,
        requesterId: threadId,
        action: 'MUTEX_ACQUIRE_REQUEST',
        status: 'INFO',
        message: `Thread ${threadId} requested Mutex lock for Event #${eventId}. Queue size: ${lock.queueLength}`
      });

      const releaseLock = await lock.acquire(threadId);

      try {
        auditLogger.log({
          eventId,
          requesterId: threadId,
          action: 'MUTEX_ACQUIRED',
          status: 'SUCCESS',
          message: `Thread ${threadId} acquired Mutex lock. ENTERING CRITICAL SECTION.`
        });

        const event = db.getEventRef(eventId);
        if (!event) {
          throw { status: 404, code: 'EVENT_NOT_FOUND', message: `Event with ID #${eventId} not found.` };
        }

        // --- CRITICAL SECTION BEGIN ---
        auditLogger.log({
          eventId,
          requesterId: threadId,
          action: 'CRITICAL_SECTION_CHECK',
          status: 'INFO',
          remainingCapacity: event.remainingCapacity,
          message: `Inside Critical Section: Inspecting duplicate status and remaining capacity (${event.remainingCapacity}/${event.totalCapacity})`
        });

        // 1. Duplicate-registration prevention
        const existingReg = event.registrations.find(r => r.userEmail.toLowerCase() === normalizedEmail);
        if (existingReg) {
          auditLogger.log({
            eventId,
            requesterId: threadId,
            action: 'DUPLICATE_REJECTED',
            status: 'WARN',
            message: `Duplicate registration rejected for ${normalizedEmail}. Existing Ticket: ${existingReg.id}`
          });
          throw {
            status: 409,
            code: 'DUPLICATE_REGISTRATION',
            message: `User with email "${normalizedEmail}" is already registered (Ticket #${existingReg.id}).`
          };
        }

        // 2. Capacity tracking and verification
        if (event.remainingCapacity <= 0) {
          auditLogger.log({
            eventId,
            requesterId: threadId,
            action: 'SOLD_OUT_REJECTED',
            status: 'WARN',
            remainingCapacity: event.remainingCapacity,
            message: `Capacity check failed: Event is full (Remaining: ${event.remainingCapacity}). Registration rejected.`
          });
          throw {
            status: 409,
            code: 'SOLD_OUT',
            message: `Registration failed: Workshop is completely sold out.`
          };
        }

        // Simulate small atomic operation processing time
        if (simulatedDelayMs > 0) {
          await sleep(simulatedDelayMs);
        }

        // 3. Atomic State Mutation
        event.remainingCapacity -= 1;
        const newTicket = {
          id: `TKT-${event.id}-${Date.now().toString().slice(-4)}-${Math.random().toString(36).substring(2, 5).toUpperCase()}`,
          userName: cleanName,
          userEmail: normalizedEmail,
          registeredAt: new Date().toISOString(),
          ticketStatus: 'CONFIRMED'
        };
        event.registrations.push(newTicket);
        db.persist();

        auditLogger.log({
          eventId,
          requesterId: threadId,
          action: 'REGISTRATION_COMMITTED',
          status: 'SUCCESS',
          remainingCapacity: event.remainingCapacity,
          message: `Registration committed for ${cleanName} (${normalizedEmail}). Seat allocated: ${newTicket.id}. Remaining: ${event.remainingCapacity}`
        });

        return {
          success: true,
          ticket: newTicket,
          remainingCapacity: event.remainingCapacity,
          totalCapacity: event.totalCapacity,
          mode: 'MUTEX_SAFE'
        };
        // --- CRITICAL SECTION END ---

      } finally {
        releaseLock();
        auditLogger.log({
          eventId,
          requesterId: threadId,
          action: 'MUTEX_RELEASED',
          status: 'INFO',
          message: `Thread ${threadId} released Mutex lock. EXITED CRITICAL SECTION.`
        });
      }

    } else {
      // ========================================================
      // 2. UNSAFE MODE (NO MUTEX - DEMONSTRATING RACE CONDITION)
      // ========================================================
      // Notice: Multiple threads execute simultaneously without acquiring a lock.
      // They read capacity > 0 during the check, sleep briefly (context switch / I/O),
      // and then both decrement the capacity, causing OVERBOOKING!
      const event = db.getEventRef(eventId);
      if (!event) {
        throw { status: 404, code: 'EVENT_NOT_FOUND', message: `Event #${eventId} not found.` };
      }

      auditLogger.log({
        eventId,
        requesterId: threadId,
        action: 'UNSAFE_CHECK_WITHOUT_LOCK',
        status: 'WARN',
        remainingCapacity: event.remainingCapacity,
        message: `Thread ${threadId} (NO MUTEX) reading capacity: ${event.remainingCapacity}`
      });

      // Duplicate check without synchronization
      const existingReg = event.registrations.find(r => r.userEmail.toLowerCase() === normalizedEmail);
      if (existingReg) {
        throw {
          status: 409,
          code: 'DUPLICATE_REGISTRATION',
          message: `User with email "${normalizedEmail}" is already registered.`
        };
      }

      // Check-then-act vulnerability (TOCTOU)
      if (event.remainingCapacity <= 0) {
        throw {
          status: 409,
          code: 'SOLD_OUT',
          message: `Registration failed: Workshop is completely sold out.`
        };
      }

      // VULNERABILITY WINDOW: The thread delays here before writing, allowing
      // other threads to pass the condition check with stale capacity values!
      await sleep(simulatedDelayMs || 25);

      // Decrement without mutual exclusion
      event.remainingCapacity -= 1;
      const newTicket = {
        id: `TKT-UNSAFE-${Date.now().toString().slice(-4)}-${Math.random().toString(36).substring(2, 5).toUpperCase()}`,
        userName: cleanName,
        userEmail: normalizedEmail,
        registeredAt: new Date().toISOString(),
        ticketStatus: event.remainingCapacity < 0 ? 'OVERBOOKED' : 'CONFIRMED'
      };
      event.registrations.push(newTicket);
      db.persist();

      const isOverbooked = event.remainingCapacity < 0;
      auditLogger.log({
        eventId,
        requesterId: threadId,
        action: isOverbooked ? 'RACE_HAZARD_OVERBOOKING' : 'UNSAFE_WRITE',
        status: isOverbooked ? 'CRITICAL' : 'WARN',
        remainingCapacity: event.remainingCapacity,
        message: isOverbooked
          ? `RACE CONDITION DETECTED! Thread ${threadId} overbooked event! Capacity is now ${event.remainingCapacity}`
          : `Thread ${threadId} wrote registration without lock. Remaining: ${event.remainingCapacity}`
      });

      return {
        success: true,
        ticket: newTicket,
        remainingCapacity: event.remainingCapacity,
        totalCapacity: event.totalCapacity,
        isOverbooked,
        mode: 'UNSAFE_RACE_CONDITION'
      };
    }
  }

  /**
   * Cancel a registration and safely restore capacity
   */
  async cancelRegistration({ eventId, ticketId, userEmail }) {
    const lock = keyedMutex.getLock(eventId);
    const threadId = `cancel-${Date.now().toString().slice(-4)}`;

    return lock.runExclusive(async () => {
      const event = db.getEventRef(eventId);
      if (!event) {
        throw { status: 404, code: 'EVENT_NOT_FOUND', message: `Event #${eventId} not found.` };
      }

      const regIndex = event.registrations.findIndex(r => 
        (ticketId && r.id === ticketId) || 
        (userEmail && r.userEmail.toLowerCase() === userEmail.trim().toLowerCase())
      );

      if (regIndex === -1) {
        throw { status: 404, code: 'REGISTRATION_NOT_FOUND', message: 'No matching registration found to cancel.' };
      }

      const [removed] = event.registrations.splice(regIndex, 1);
      
      // Restore capacity safely up to total capacity
      if (event.remainingCapacity < event.totalCapacity) {
        event.remainingCapacity += 1;
      }
      db.persist();

      auditLogger.log({
        eventId,
        requesterId: threadId,
        action: 'REGISTRATION_CANCELLED',
        status: 'SUCCESS',
        remainingCapacity: event.remainingCapacity,
        message: `Registration ${removed.id} for ${removed.userEmail} was cancelled. Seat restored to pool. Capacity: ${event.remainingCapacity}`
      });

      return {
        success: true,
        cancelledTicket: removed,
        remainingCapacity: event.remainingCapacity,
        totalCapacity: event.totalCapacity
      };
    }, threadId);
  }

  /**
   * Reset an event back to test baseline
   */
  resetEvent(id) {
    const reset = db.resetEventToInitial(id);
    if (!reset) return null;
    auditLogger.log({
      eventId: id,
      action: 'EVENT_RESET',
      status: 'INFO',
      remainingCapacity: reset.remainingCapacity,
      message: `Event #${id} was reset to baseline with ${reset.remainingCapacity} available places.`
    });
    return reset;
  }

  /**
   * Reset all events
   */
  resetAll() {
    auditLogger.clear();
    return db.resetAll();
  }

  /**
   * Automated Concurrency Stress Simulation
   * Fires N simultaneous registration requests in parallel.
   */
  async simulateConcurrentRush({ eventId, userCount = 10, useMutex = true, artificialDelayMs = 20 }) {
    const event = db.getEventById(eventId);
    if (!event) {
      throw { status: 404, code: 'EVENT_NOT_FOUND', message: `Event #${eventId} not found.` };
    }

    const initialCapacity = event.remainingCapacity;
    const initialRegistrationsCount = event.registrations.length;
    const startTime = Date.now();

    auditLogger.log({
      eventId,
      action: 'SIMULATION_STARTED',
      status: 'INFO',
      message: `Beginning concurrency benchmark with ${userCount} simultaneous users competing for ${initialCapacity} remaining seats (Mode: ${useMutex ? 'MUTEX_SAFE' : 'UNSAFE_RACE'}).`
    });

    // Generate N distinct virtual attendees
    const requests = Array.from({ length: userCount }, (_, i) => {
      const attendeeNum = i + 1;
      return this.registerUser({
        eventId,
        userName: `Virtual Attendee #${attendeeNum}`,
        userEmail: `simulated.user.${attendeeNum}.${Date.now().toString().slice(-4)}@benchmark.test`,
        useMutex,
        requesterId: `sim-thread-${attendeeNum.toString().padStart(2, '0')}`,
        simulatedDelayMs: artificialDelayMs
      });
    });

    // Execute simultaneously
    const results = await Promise.allSettled(requests);
    const durationMs = Date.now() - startTime;

    const finalEvent = db.getEventById(eventId);
    const finalCapacity = finalEvent.remainingCapacity;

    const successful = results.filter(r => r.status === 'fulfilled').map(r => r.value);
    const rejected = results.filter(r => r.status === 'rejected').map(r => r.reason);

    const soldOutRejections = rejected.filter(r => r && r.code === 'SOLD_OUT').length;
    const duplicateRejections = rejected.filter(r => r && r.code === 'DUPLICATE_REGISTRATION').length;
    const otherFailures = rejected.length - soldOutRejections - duplicateRejections;

    // Check if race condition caused overbooking
    const overbookedCount = Math.max(0, -finalCapacity);
    const hasRaceHazard = !useMutex && (overbookedCount > 0 || successful.length > initialCapacity);

    return {
      simulationMeta: {
        eventId,
        eventTitle: event.title,
        mode: useMutex ? 'MUTEX_PROTECTED (CRITICAL SECTION ACTIVE)' : 'UNSAFE_CONCURRENCY (NO MUTEX)',
        simulatedUsers: userCount,
        durationMs,
        initialCapacity,
        finalCapacity,
        expectedSuccessfulRegistrations: Math.min(userCount, Math.max(0, initialCapacity)),
        actualSuccessfulRegistrations: successful.length,
        soldOutRejections,
        duplicateRejections,
        otherFailures,
        overbookedCount,
        hasRaceHazard,
        safetyVerdict: hasRaceHazard 
          ? 'FAILURE: Race Condition resulted in overbooking! Capacity integrity violated.' 
          : 'SUCCESS: Mutual exclusion preserved data integrity. No overbooking.'
      },
      successfulRegistrations: successful,
      rejectedRegistrations: rejected
    };
  }

  /**
   * Head-to-Head 1-Seat Dual Contender Clash
   * Two named users compete for the final remaining seat at the exact same microsecond.
   */
  async executeDuel({ eventId, userA, userB, useMutex = true }) {
    const event = db.getEventById(eventId);
    if (!event) {
      throw { status: 404, code: 'EVENT_NOT_FOUND', message: `Event #${eventId} not found.` };
    }

    const nameA = (userA && userA.name) || 'User A (Rahul)';
    const emailA = (userA && userA.email) || `rahul.${Date.now().toString().slice(-4)}@campus.edu`;
    const nameB = (userB && userB.name) || 'User B (Priya)';
    const emailB = (userB && userB.email) || `priya.${Date.now().toString().slice(-4)}@campus.edu`;

    const initialSeats = event.remainingCapacity;
    const startTime = Date.now();

    // Fire both requests concurrently
    const pA = this.registerUser({
      eventId,
      userName: nameA,
      userEmail: emailA,
      useMutex,
      requesterId: 'contender-A',
      simulatedDelayMs: 25
    });

    const pB = this.registerUser({
      eventId,
      userName: nameB,
      userEmail: emailB,
      useMutex,
      requesterId: 'contender-B',
      simulatedDelayMs: 25
    });

    const [resA, resB] = await Promise.allSettled([pA, pB]);
    const durationMs = Date.now() - startTime;
    const finalEvent = db.getEventById(eventId);

    const winnerA = resA.status === 'fulfilled';
    const winnerB = resB.status === 'fulfilled';

    let verdict = '';
    if (useMutex) {
      verdict = (winnerA && !winnerB) 
        ? `${nameA} acquired the Mutex lock first and secured the final seat. ${nameB} was placed in the FIFO queue and cleanly rejected with 'Sold Out'. Zero overbooking!`
        : (winnerB && !winnerA)
        ? `${nameB} acquired the Mutex lock first and secured the final seat. ${nameA} was placed in the FIFO queue and cleanly rejected with 'Sold Out'. Zero overbooking!`
        : `Both contenders were rejected as event had 0 seats available.`;
    } else {
      verdict = (winnerA && winnerB)
        ? `RACE CONDITION TRIGGERED: Both ${nameA} and ${nameB} booked the same final seat! Overbooking occurred (Capacity: ${finalEvent.remainingCapacity}).`
        : `Unsynchronized execution completed.`;
    }

    return {
      eventId,
      eventTitle: event.title,
      useMutex,
      initialSeats,
      finalSeats: finalEvent.remainingCapacity,
      durationMs,
      verdict,
      contenderA: {
        name: nameA,
        status: resA.status === 'fulfilled' ? 'WINNER_BOOKED' : 'REJECTED_SOLD_OUT',
        ticket: resA.status === 'fulfilled' ? resA.value.ticket : null,
        message: resA.status === 'fulfilled' ? 'Allocated the final seat' : (resA.reason && resA.reason.message) || 'Sold Out'
      },
      contenderB: {
        name: nameB,
        status: resB.status === 'fulfilled' ? 'WINNER_BOOKED' : 'REJECTED_SOLD_OUT',
        ticket: resB.status === 'fulfilled' ? resB.value.ticket : null,
        message: resB.status === 'fulfilled' ? 'Allocated the final seat' : (resB.reason && resB.reason.message) || 'Sold Out'
      },
      algorithmTrace: [
        { step: 1, code: 'lock.acquire(threadId)', explanation: useMutex ? 'First arrival grabs lock; second arrival waits in FIFO queue' : 'SKIPPED (No lock, threads run un-synchronized)' },
        { step: 2, code: 'if (remainingCapacity <= 0) throw SoldOut()', explanation: useMutex ? 'Evaluates False for first thread (1 > 0); evaluates True for second thread (0 <= 0)' : 'Both threads evaluate False simultaneously on stale memory!' },
        { step: 3, code: 'remainingCapacity -= 1', explanation: useMutex ? 'Decremented atomically to 0 by winner' : 'Both threads decrement, driving capacity to -1 (Anomaly)' },
        { step: 4, code: 'saveTicket(user)', explanation: useMutex ? 'Ticket issued only to winner' : 'Two tickets issued for a single seat!' },
        { step: 5, code: 'lock.release()', explanation: useMutex ? 'Lock passed to next in queue or freed' : 'No lock to release' }
      ]
    };
  }
}

module.exports = new EventService();
