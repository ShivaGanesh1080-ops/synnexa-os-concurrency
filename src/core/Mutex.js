/**
 * OS Synchronization Primitive: Industrial-Grade Asynchronous Mutex
 * 
 * Implements the 3 Classical Operating System Critical Section Properties:
 * 1. Mutual Exclusion: At most one execution thread/request can hold the critical section.
 * 2. Progress: If no thread is in the critical section, pending threads acquire the lock without delay.
 * 3. Bounded Waiting: Waiting threads are queued in strict First-Come, First-Served (FIFO) order,
 *    preventing thread starvation under high contention (e.g. IRCTC Tatkal booking rush).
 */

const { EventEmitter } = require('events');

class Mutex extends EventEmitter {
  constructor(name = 'default-mutex') {
    super();
    this.name = name;
    this._locked = false;
    this._queue = []; // FIFO Queue for Bounded Waiting
    this._currentOwner = null;
    this._acquiredAt = null;

    // Concurrency Metrics
    this.metrics = {
      totalAcquisitions: 0,
      totalContentions: 0,
      currentQueueLength: 0,
      maxQueueLength: 0,
      totalHoldDurationMs: 0
    };
  }

  get isLocked() {
    return this._locked;
  }

  get queueLength() {
    return this._queue.length;
  }

  get currentOwner() {
    return this._currentOwner;
  }

  get holdTimeMs() {
    if (!this._locked || !this._acquiredAt) return 0;
    return Date.now() - this._acquiredAt;
  }

  /**
   * Acquire the Mutex.
   * If free, grants lock immediately.
   * If busy, enqueues request into FIFO queue and suspends caller until released.
   * 
   * @param {string} requesterId - Unique identifier of the thread or team requesting access
   * @param {string} teamName - Optional team name for visual telemetry
   * @returns {Promise<Function>} - Resolves to a release callback when lock is granted
   */
  acquire(requesterId = `req-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`, teamName = '') {
    const enqueueTime = Date.now();
    this.emit('lock_requested', {
      name: this.name,
      requesterId,
      teamName,
      queueLength: this._queue.length + (this._locked ? 1 : 0),
      timestamp: new Date().toISOString()
    });

    if (!this._locked) {
      // Fast path: Mutex is unheld
      this._locked = true;
      this._currentOwner = { id: requesterId, teamName, acquiredAt: enqueueTime };
      this._acquiredAt = enqueueTime;
      this.metrics.totalAcquisitions++;

      this.emit('lock_acquired', {
        name: this.name,
        requesterId,
        teamName,
        waitTimeMs: 0,
        queueLength: this._queue.length,
        timestamp: new Date().toISOString()
      });

      let released = false;
      const release = () => {
        if (released) return;
        released = true;
        this._release(requesterId, teamName);
      };

      return Promise.resolve(release);
    }

    // Contention path: Mutex is held, enqueue into FIFO waiting line
    this.metrics.totalContentions++;
    this.metrics.currentQueueLength++;
    if (this.metrics.currentQueueLength > this.metrics.maxQueueLength) {
      this.metrics.maxQueueLength = this.metrics.currentQueueLength;
    }

    return new Promise((resolve) => {
      this._queue.push({
        requesterId,
        teamName,
        enqueueTime,
        grant: () => {
          this._locked = true;
          this._currentOwner = { id: requesterId, teamName, acquiredAt: Date.now() };
          this._acquiredAt = Date.now();
          this.metrics.totalAcquisitions++;
          this.metrics.currentQueueLength = Math.max(0, this.metrics.currentQueueLength - 1);

          const waitTimeMs = Date.now() - enqueueTime;
          this.emit('lock_acquired', {
            name: this.name,
            requesterId,
            teamName,
            waitTimeMs,
            queueLength: this._queue.length,
            timestamp: new Date().toISOString()
          });

          let released = false;
          const release = () => {
            if (released) return;
            released = true;
            this._release(requesterId, teamName);
          };

          resolve(release);
        }
      });
    });
  }

  /**
   * Execute an asynchronous callback exclusively under this Mutex
   * @param {Function} task - Async callback
   * @param {string} requesterId - Requester identity
   * @param {string} teamName - Human-readable team name
   * @returns {Promise<any>}
   */
  async runExclusive(task, requesterId = `req-${Date.now()}`, teamName = '') {
    const release = await this.acquire(requesterId, teamName);
    try {
      return await task();
    } finally {
      release();
    }
  }

  /**
   * Internal release handler.
   * Hands off lock to next waiting context in FIFO queue.
   */
  _release(requesterId, teamName) {
    const holdDurationMs = this._acquiredAt ? (Date.now() - this._acquiredAt) : 0;
    this.metrics.totalHoldDurationMs += holdDurationMs;

    this.emit('lock_released', {
      name: this.name,
      requesterId,
      teamName,
      holdDurationMs,
      queueLength: this._queue.length,
      timestamp: new Date().toISOString()
    });

    if (this._queue.length > 0) {
      // FIFO Handoff to next in line (guarantees Progress & Bounded Waiting)
      const nextTask = this._queue.shift();
      nextTask.grant();
    } else {
      this._locked = false;
      this._currentOwner = null;
      this._acquiredAt = null;
    }
  }

  /**
   * Snapshot of current mutex state for live telemetry
   */
  getSnapshot() {
    return {
      name: this.name,
      isLocked: this._locked,
      currentOwner: this._currentOwner ? this._currentOwner.teamName || this._currentOwner.id : null,
      holdTimeMs: this.holdTimeMs,
      queueLength: this._queue.length,
      waiters: this._queue.map(q => q.teamName || q.requesterId),
      metrics: { ...this.metrics }
    };
  }

  /**
   * Reset the mutex to clean state
   */
  reset() {
    this._locked = false;
    this._queue = [];
    this._currentOwner = null;
    this._acquiredAt = null;
    this.metrics = {
      totalAcquisitions: 0,
      totalContentions: 0,
      currentQueueLength: 0,
      maxQueueLength: 0,
      totalHoldDurationMs: 0
    };
  }
}

module.exports = Mutex;
