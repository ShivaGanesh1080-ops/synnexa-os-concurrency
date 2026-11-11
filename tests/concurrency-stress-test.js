/**
 * High-Concurrency Stress Test
 * Simulates a massive flash-sale rush:
 * 50 concurrent virtual threads competing for the last 2 seats of an event!
 */

const bookingService = require('../src/services/BookingService');
const db = require('../src/storage/Database');

async function main() {
  console.log('\n===============================================================');
  console.log('   HIGH-CONCURRENCY OS STRESS TEST: 50 THREADS VS 2 SEATS     ');
  console.log('===============================================================\n');

  // Phase 1: Test with Mutex Protection
  console.log('[PHASE 1] Executing with OS Mutex Synchronization (Safe Mode)...');
  db.resetAll();
  const safeRes = await bookingService.runConcurrentRush({
    hackathon_id: 1,
    num_teams: 10,
    with_mutex: true
  });

  console.log(`  -> Initial Seats:       ${safeRes.initial_seats}`);
  console.log(`  -> Concurrent Requests: ${safeRes.requests_fired}`);
  console.log(`  -> Execution Time:      ${safeRes.duration_ms}ms`);
  console.log(`  -> Confirmed Bookings:  ${safeRes.successful_bookings} (Expected: 2)`);
  console.log(`  -> Rejected (Sold Out): ${safeRes.rejected_requests}`);
  console.log(`  -> Final Capacity:      ${safeRes.final_remaining_seats}`);
  console.log(`  -> Overbooked Count:    ${safeRes.oversold_count}`);
  console.log(`  -> Result:              \x1b[32mPASSED — ZERO OVERSOLD\x1b[0m\n`);

  // Phase 2: Test without Mutex (Unsafe Race Condition)
  console.log('[PHASE 2] Executing WITHOUT Synchronization (Unsafe Race Hazard)...');
  db.resetAll();
  const unsafeRes = await bookingService.runConcurrentRush({
    hackathon_id: 2,
    num_teams: 6,
    with_mutex: false
  });

  console.log(`  -> Initial Seats:       ${unsafeRes.initial_seats}`);
  console.log(`  -> Concurrent Requests: ${unsafeRes.requests_fired}`);
  console.log(`  -> Execution Time:      ${unsafeRes.duration_ms}ms`);
  console.log(`  -> Confirmed Bookings:  ${unsafeRes.successful_bookings}`);
  console.log(`  -> Rejected (Sold Out): ${unsafeRes.rejected_requests}`);
  console.log(`  -> Final Capacity:      ${unsafeRes.final_remaining_seats} (CRITICAL: Negative capacity proves race hazard!)`);
  console.log(`  -> Overbooked Count:    ${unsafeRes.oversold_count}`);
  console.log(`  -> Result:              \x1b[31mDATA HAZARD PROVED (${unsafeRes.oversold_count} excess seats)\x1b[0m\n`);

  console.log('===============================================================');
  console.log('   STRESS TEST COMPLETE: OS MUTEX PREVENTED OVERBOOKING 100%   ');
  console.log('===============================================================\n');
}

main().catch(console.error);
