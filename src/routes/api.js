const db = require('../storage/Database');
const bookingService = require('../services/BookingService');
const { defaultRegistry } = require('../core/KeyedMutexRegistry');

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=UTF-8',
    'Cache-Control': 'no-store, no-cache, must-revalidate'
  });
  res.end(JSON.stringify(data));
}

async function handleApiRequest(req, res, pathname, queryParams, body) {
  const method = req.method;

  try {
    // 1. Hackathons List & Create
    if (pathname === '/api/hackathons') {
      if (method === 'GET') {
        const hackathons = db.getHackathons();
        // Append current live mutex snapshot to each event
        const enriched = hackathons.map(h => {
          const mutex = defaultRegistry.get(h.id);
          const tatkalRemaining = h.remaining_tickets !== undefined ? h.remaining_tickets : (h.tatkal_remaining || 0);
          const tatkalQuota = h.tatkal_quota !== undefined ? h.tatkal_quota : (h.tatkal_seats || 4);
          const totalSeats = h.total_tickets !== undefined ? h.total_tickets : (h.total_seats || 10);
          return {
            ...h,
            tatkal_remaining: tatkalRemaining,
            tatkal_seats: tatkalQuota,
            total_seats: totalSeats,
            remaining_tickets: tatkalRemaining,
            mutex_snapshot: mutex.getSnapshot()
          };
        });
        return sendJson(res, 200, { success: true, hackathons: enriched });
      }

      if (method === 'POST') {
        // Hackathon Admin Creates Event / Releases Ticket Batch
        const newEvent = db.createHackathon(body);
        return sendJson(res, 201, {
          success: true,
          message: "Hackathon & Tatkal Ticket Batch released successfully!",
          hackathon: newEvent
        });
      }
    }

    // 2. Specific Hackathon Details, Update, Mutex Toggle
    const hackathonMatch = pathname.match(/^\/api\/hackathons\/(\d+)$/);
    if (hackathonMatch) {
      const eventId = Number(hackathonMatch[1]);
      if (method === 'GET') {
        const event = db.getHackathonById(eventId);
        if (!event) return sendJson(res, 404, { success: false, error: "Hackathon not found" });
        const mutex = defaultRegistry.get(eventId);
        return sendJson(res, 200, {
          success: true,
          hackathon: event,
          teams: db.getTeamsByHackathon(eventId),
          mutex_snapshot: mutex.getSnapshot()
        });
      }

      if (method === 'PUT') {
        const updated = db.updateHackathon(eventId, body);
        return sendJson(res, 200, { success: true, hackathon: updated });
      }
    }

    // Toggle Mutex for Hackathon
    const toggleMatch = pathname.match(/^\/api\/hackathons\/(\d+)\/toggle-mutex$/);
    if (toggleMatch && method === 'POST') {
      const eventId = Number(toggleMatch[1]);
      const event = db.toggleMutex(eventId);
      if (!event) return sendJson(res, 404, { success: false, error: "Hackathon not found" });
      return sendJson(res, 200, {
        success: true,
        message: `Mutex protection is now ${event.mutex_enabled ? 'ENABLED' : 'DISABLED'} for ${event.title}`,
        event
      });
    }

    // Teams / Roster for a Hackathon
    const teamsMatch = pathname.match(/^\/api\/hackathons\/(\d+)\/teams$/);
    if (teamsMatch && method === 'GET') {
      const eventId = Number(teamsMatch[1]);
      const teams = db.getTeamsByHackathon(eventId);
      return sendJson(res, 200, { success: true, count: teams.length, teams });
    }

    // Ticket Check-In
    if (pathname === '/api/hackathons/checkin' && method === 'POST') {
      const { ticket_code } = body;
      if (!ticket_code) {
        return sendJson(res, 400, { success: false, error: "ticket_code is required" });
      }
      const result = db.checkInTicket(ticket_code);
      return sendJson(res, result.success ? 200 : 400, result);
    }

    // 3. User Tatkal Ticket Booking
    if (pathname === '/api/book' && method === 'POST') {
      const {
        hackathon_id,
        team_name,
        leader_name,
        leader_email,
        members,
        payment_details,
        force_no_mutex
      } = body;

      if (!hackathon_id || !team_name || !leader_name || !leader_email) {
        return sendJson(res, 400, {
          success: false,
          error: "Missing required fields: hackathon_id, team_name, leader_name, leader_email"
        });
      }

      const result = await bookingService.bookTatkalTicket({
        hackathon_id,
        team_name,
        leader_name,
        leader_email,
        members: members || [],
        payment_details: payment_details || {},
        force_no_mutex: Boolean(force_no_mutex)
      });

      const statusCode = result.success ? 200 : (result.status === "SOLD_OUT" ? 409 : 400);
      return sendJson(res, statusCode, result);
    }

    // 4. Live Concurrency Rush Simulation
    if ((pathname === '/api/concurrency-rush' || pathname === '/api/simulate-rush') && method === 'POST') {
      const {
        hackathon_id = 1,
        num_teams = 6,
        num_requests,
        with_mutex = true
      } = body;

      const teamsCount = Number(num_requests || num_teams || 6);

      const summary = await bookingService.runConcurrentRush({
        hackathon_id: Number(hackathon_id),
        num_teams: teamsCount,
        with_mutex: Boolean(with_mutex)
      });

      return sendJson(res, 200, {
        success: true,
        summary,
        ...summary
      });
    }

    // 5. Platform Admin Settings (Razorpay Test Keys)
    if ((pathname === '/api/platform/settings' || pathname === '/api/settings')) {
      if (method === 'GET') {
        const settings = db.getSettings();
        return sendJson(res, 200, { success: true, settings });
      }

      if (method === 'POST') {
        const updated = db.updateSettings(body);
        return sendJson(res, 200, {
          success: true,
          message: "Platform settings & Razorpay test credentials updated successfully!",
          settings: updated
        });
      }
    }

    // 6. Platform Overview Stats & Teams
    if (pathname === '/api/teams' && method === 'GET') {
      const teams = db.getAllTeams();
      return sendJson(res, 200, { success: true, count: teams.length, teams });
    }

    if (pathname === '/api/platform/stats' && method === 'GET') {
      const hackathons = db.getHackathons();
      const teams = db.getAllTeams();
      const logs = db.getAuditLogs(200);

      const totalRevenue = teams.reduce((acc, team) => {
        const h = hackathons.find(x => x.id === team.hackathon_id);
        return acc + (h ? h.ticket_price : 0);
      }, 0);

      const mutexSnapshots = defaultRegistry.getAllSnapshots();
      let totalContentions = 0;
      let totalAcquisitions = 0;
      for (const s of Object.values(mutexSnapshots)) {
        totalContentions += (s.metrics ? s.metrics.totalContentions : 0);
        totalAcquisitions += (s.metrics ? s.metrics.totalAcquisitions : 0);
      }

      return sendJson(res, 200, {
        success: true,
        stats: {
          total_events: hackathons.length,
          total_teams_registered: teams.length,
          total_revenue_inr: totalRevenue,
          total_lock_acquisitions: totalAcquisitions,
          total_contentions_handled: totalContentions,
          total_audit_records: logs.length
        }
      });
    }

    // 7. Audit Logs & Live State
    if (pathname === '/api/audit-logs' && method === 'GET') {
      const limit = queryParams.get('limit') ? Number(queryParams.get('limit')) : 50;
      const logs = db.getAuditLogs(limit);
      return sendJson(res, 200, { success: true, logs });
    }

    if ((pathname === '/api/audit-logs/clear' || pathname === '/api/audit-logs') && (method === 'POST' || method === 'DELETE')) {
      db.clearAuditLogs();
      return sendJson(res, 200, { success: true, message: "Critical section audit trail cleared successfully." });
    }

    if (pathname === '/api/mutex-state' && method === 'GET') {
      const snapshots = defaultRegistry.getAllSnapshots();
      return sendJson(res, 200, { success: true, snapshots });
    }

    // 8. Reset to baseline (For demonstrations)
    if ((pathname === '/api/reset' || pathname === '/api/reset-all') && method === 'POST') {
      defaultRegistry.resetAll();
      const resetData = db.resetAll();
      return sendJson(res, 200, {
        success: true,
        message: "System reset to baseline state (2 Tatkal seats remaining, clean mutex locks).",
        data: resetData
      });
    }

    // Fallback for unknown API routes
    return sendJson(res, 404, { success: false, error: "API Endpoint Not Found" });

  } catch (err) {
    console.error(`[API Error] ${method} ${pathname}:`, err);
    return sendJson(res, 500, {
      success: false,
      error: "INTERNAL_SERVER_ERROR",
      message: err.message
    });
  }
}

module.exports = { handleApiRequest };
