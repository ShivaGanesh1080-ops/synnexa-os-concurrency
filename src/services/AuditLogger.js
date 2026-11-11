const { EventEmitter } = require('events');

/**
 * Real-Time Concurrency Audit Logger
 * Tracks state transitions of threads, locks, critical sections, and capacity mutations.
 * Inherits from EventEmitter to support real-time SSE streaming.
 */
class AuditLogger extends EventEmitter {
  constructor(maxSize = 300) {
    super();
    this.logs = [];
    this.maxSize = maxSize;
  }

  log(entry) {
    const logItem = {
      id: `log-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      timestamp: new Date().toISOString(),
      millis: Date.now(),
      eventId: entry.eventId || 'system',
      requesterId: entry.requesterId || 'thread-anonymous',
      action: entry.action, // e.g. LOCK_WAIT, LOCK_ACQUIRED, CRITICAL_SECTION, COMMITTED, RELEASED, REJECTED
      status: entry.status || 'INFO', // INFO, SUCCESS, WARN, ERROR, CRITICAL
      message: entry.message,
      remainingCapacity: entry.remainingCapacity !== undefined ? entry.remainingCapacity : null,
      details: entry.details || null
    };

    this.logs.unshift(logItem); // newest first
    if (this.logs.length > this.maxSize) {
      this.logs.pop();
    }

    // Push real-time event to SSE subscribers
    this.emit('log', logItem);

    return logItem;
  }

  getLogs(eventId = null, limit = 50) {
    let filtered = this.logs;
    if (eventId) {
      filtered = filtered.filter(l => String(l.eventId) === String(eventId));
    }
    return filtered.slice(0, limit);
  }

  clear(eventId = null) {
    if (eventId) {
      this.logs = this.logs.filter(l => String(l.eventId) !== String(eventId));
    } else {
      this.logs = [];
    }
  }
}

module.exports = new AuditLogger();
