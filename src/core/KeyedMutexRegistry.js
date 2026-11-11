/**
 * KeyedMutexRegistry - Fine-grained lock management per Hackathon / Resource
 * 
 * Ensures bookings for Hackathon A don't lock or block Hackathon B,
 * but all concurrent bookings within the same Hackathon queue up in strict FIFO order.
 */

const Mutex = require('./Mutex');

class KeyedMutexRegistry {
  constructor() {
    this._registry = new Map();
  }

  /**
   * Retrieve or instantiate a named Mutex for a specific event/resource
   * @param {string|number} key - Identifier (e.g. hackathon-1)
   * @returns {Mutex}
   */
  get(key) {
    const keyStr = String(key);
    if (!this._registry.has(keyStr)) {
      const mutex = new Mutex(`mutex-${keyStr}`);
      this._registry.set(keyStr, mutex);
    }
    return this._registry.get(keyStr);
  }

  getLock(key) {
    return this.get(key);
  }

  /**
   * Execute an asynchronous task inside the Critical Section of a keyed Mutex
   * @param {string|number} key - Identifier
   * @param {Function} task - Async callback
   * @param {string} requesterId - Requester identity
   * @param {string} teamName - Human-readable team name
   */
  async runExclusive(key, task, requesterId, teamName) {
    const mutex = this.get(key);
    const release = await mutex.acquire(requesterId, teamName);
    try {
      return await task();
    } finally {
      release();
    }
  }

  /**
   * Get snapshots of all active mutexes for real-time dashboard visualization
   */
  getAllSnapshots() {
    const result = {};
    for (const [key, mutex] of this._registry.entries()) {
      result[key] = mutex.getSnapshot();
    }
    return result;
  }

  /**
   * Reset all mutexes
   */
  resetAll() {
    for (const mutex of this._registry.values()) {
      mutex.reset();
    }
  }
}

const defaultRegistry = new KeyedMutexRegistry();
module.exports = { KeyedMutexRegistry, defaultRegistry };
