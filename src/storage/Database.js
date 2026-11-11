const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', '..', 'data');
const DB_FILE = path.join(DATA_DIR, 'database.json');

const INITIAL_PLATFORM_SETTINGS = {
  razorpay_key_id: "rzp_test_1DP5mmOlF5G5ag", // Configurable in Platform Admin
  razorpay_key_secret: "mock_secret_test_key_sync_reg",
  payment_mode: "test",
  platform_name: "SyncReg IRCTC-Grade Tatkal Concurrency Platform",
  currency: "INR",
  platform_fee_percent: 2.5
};

const INITIAL_HACKATHONS = [
  {
    id: 1,
    title: "Global AI HackSphere 2026: Foundation Models & Agents",
    tagline: "Build, train, and deploy real-time LLM agents and multi-modal systems",
    organizer: "SRU CSE & Silicon Valley AI Research Collective",
    venue: "Moscone Center, San Francisco & Virtual Hub",
    city: "San Francisco, USA",
    dates: "Nov 24–26, 2026",
    total_tickets: 10,
    tatkal_quota: 4,
    remaining_tickets: 2, // Exactly 2 seats left to demonstrate concurrency rush!
    ticket_price: 499,
    mutex_enabled: true,
    status: "ACTIVE",
    badge: "2 Seats Left (Flash Quota)",
    category: "AI & Machine Learning",
    image_url: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1000&q=80"
  },
  {
    id: 2,
    title: "Tokyo CyberCon 48h: Zero-Trust Security & CTF Warfare",
    tagline: "Offensive security, reverse engineering, and cloud kernel defense",
    organizer: "Shibuya Cyber Defense Lab & Global InfoSec Alliance",
    venue: "Shibuya Stream Hall, Tokyo, Japan",
    city: "Tokyo, Japan",
    dates: "Dec 02–04, 2026",
    total_tickets: 8,
    tatkal_quota: 3,
    remaining_tickets: 1, // Exactly 1 seat left!
    ticket_price: 299,
    mutex_enabled: true,
    status: "ACTIVE",
    badge: "Last 1 Seat Remaining!",
    category: "Cybersecurity & CTF",
    image_url: "https://images.unsplash.com/photo-1515187029135-18ee286d815b?auto=format&fit=crop&w=1000&q=80"
  },
  {
    id: 3,
    title: "London CloudScale: High-Throughput Distributed Systems",
    tagline: "Architect resilient lock managers, raft consensus, and streaming backends",
    organizer: "SRU Cloud Computing Lab & UK Tech Council",
    venue: "ExCeL London International Arena",
    city: "London, UK",
    dates: "Dec 12–14, 2026",
    total_tickets: 8,
    tatkal_quota: 3,
    remaining_tickets: 2,
    ticket_price: 399,
    mutex_enabled: true,
    status: "ACTIVE",
    badge: "2 Seats Left",
    category: "Cloud & Systems",
    image_url: "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&w=1000&q=80"
  },
  {
    id: 4,
    title: "Bengaluru TechSummit 2026: Web3 & High-Scale FinTech",
    tagline: "Building zero-knowledge transaction pipelines and real-time settlement engines",
    organizer: "Indiranagar Tech Guild & SRU Innovation",
    venue: "Bengaluru International Exhibition Centre",
    city: "Bengaluru, India",
    dates: "Dec 18–20, 2026",
    total_tickets: 12,
    tatkal_quota: 4,
    remaining_tickets: 3,
    ticket_price: 499,
    mutex_enabled: true,
    status: "ACTIVE",
    badge: "Popular Batch",
    category: "Web3 & FinTech",
    image_url: "https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=1000&q=80"
  },
  {
    id: 5,
    title: "Berlin Quantum & Neural Computing Hackathon",
    tagline: "Hybrid quantum algorithms, tensor processing, and next-gen silicon compute",
    organizer: "European Quantum Consortium & KiteKraft",
    venue: "Arena Berlin, Eichenstraße, Germany",
    city: "Berlin, Germany",
    dates: "Jan 08–10, 2027",
    total_tickets: 6,
    tatkal_quota: 2,
    remaining_tickets: 2,
    ticket_price: 349,
    mutex_enabled: true,
    status: "ACTIVE",
    badge: "Exclusive Pass",
    category: "Quantum & Compute",
    image_url: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1000&q=80"
  },
  {
    id: 6,
    title: "Zurich Autonomous Robotics & Embedded Systems Sprint",
    tagline: "ROS 2 navigation, computer vision sensor fusion, and real-time kinematics",
    organizer: "Swiss Robotics Innovation Labs",
    venue: "ETH Zurich Innovation Campus, Switzerland",
    city: "Zurich, Switzerland",
    dates: "Jan 18–20, 2027",
    total_tickets: 6,
    tatkal_quota: 2,
    remaining_tickets: 1,
    ticket_price: 599,
    mutex_enabled: true,
    status: "ACTIVE",
    badge: "1 Seat Remaining",
    category: "Robotics & IoT",
    image_url: "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1000&q=80"
  }
];

const INITIAL_TEAMS = [
  {
    id: "TEAM-101",
    hackathon_id: 1,
    team_name: "ByteBusters",
    leader_name: "Rahul Sharma",
    leader_email: "rahul.sharma@sru.edu.in",
    members: [
      { name: "Rahul Sharma", email: "rahul.sharma@sru.edu.in", role: "Team Leader", htno: "2503A51001" },
      { name: "Ananya Iyer", email: "ananya.i@sru.edu.in", role: "Frontend Dev", htno: "2503A51002" },
      { name: "Karthik Raja", email: "karthik.r@sru.edu.in", role: "Backend Dev", htno: "2503A51003" }
    ],
    ticket_code: "TKT-TATKAL-89211",
    payment_status: "PAID_TEST_MODE",
    payment_id: "pay_test_01928374",
    booked_at: "2026-11-09T10:14:00.000Z",
    is_checked_in: false,
    checked_in_at: null
  },
  {
    id: "TEAM-102",
    hackathon_id: 1,
    team_name: "NullPointers",
    leader_name: "Priya Varma",
    leader_email: "priya.v@sru.edu.in",
    members: [
      { name: "Priya Varma", email: "priya.v@sru.edu.in", role: "Team Leader", htno: "2503A51010" },
      { name: "Vikram Sen", email: "vikram.s@sru.edu.in", role: "ML Engineer", htno: "2503A51011" }
    ],
    ticket_code: "TKT-TATKAL-89212",
    payment_status: "PAID_TEST_MODE",
    payment_id: "pay_test_01928375",
    booked_at: "2026-11-09T11:22:00.000Z",
    is_checked_in: true,
    checked_in_at: "2026-11-09T14:30:00.000Z"
  }
];

class Database {
  constructor() {
    this._data = {
      platform_settings: { ...INITIAL_PLATFORM_SETTINGS },
      hackathons: JSON.parse(JSON.stringify(INITIAL_HACKATHONS)),
      teams: JSON.parse(JSON.stringify(INITIAL_TEAMS)),
      audit_logs: []
    };
    this._init();
  }

  _init() {
    if (!fs.existsSync(DATA_DIR)) {
      fs.mkdirSync(DATA_DIR, { recursive: true });
    }

    if (fs.existsSync(DB_FILE)) {
      try {
        const raw = fs.readFileSync(DB_FILE, 'utf-8');
        const parsed = JSON.parse(raw);
        if (parsed.hackathons && parsed.teams) {
          this._data = parsed;
          if (!this._data.platform_settings) {
            this._data.platform_settings = { ...INITIAL_PLATFORM_SETTINGS };
          }
          if (!this._data.audit_logs) {
            this._data.audit_logs = [];
          }
        }
      } catch (err) {
        console.warn('[Database] Failed to read existing db. Reverting to initial data.', err.message);
        this.save();
      }
    } else {
      this.save();
    }
  }

  save() {
    try {
      fs.writeFileSync(DB_FILE, JSON.stringify(this._data, null, 2), 'utf-8');
    } catch (err) {
      console.error('[Database] Failed to persist data:', err.message);
    }
  }

  // --- Platform Settings ---
  getSettings() {
    return { ...this._data.platform_settings };
  }

  updateSettings(updates) {
    this._data.platform_settings = {
      ...this._data.platform_settings,
      ...updates
    };
    this.save();
    return this.getSettings();
  }

  // --- Hackathons ---
  getHackathons() {
    return this._data.hackathons.map(h => ({ ...h }));
  }

  getHackathonById(id) {
    const numId = Number(id);
    return this._data.hackathons.find(h => h.id === numId) || null;
  }

  createHackathon(eventData) {
    const nextId = this._data.hackathons.reduce((max, h) => Math.max(max, h.id), 0) + 1;
    const newEvent = {
      id: nextId,
      title: eventData.title || `Hackathon #${nextId}`,
      tagline: eventData.tagline || "Real-time Flash Registration",
      organizer: eventData.organizer || "SR University Organizer",
      venue: eventData.venue || "Campus Lab / Hybrid",
      dates: eventData.dates || "Dec 2026",
      total_tickets: Number(eventData.total_tickets) || 10,
      tatkal_quota: Number(eventData.tatkal_quota) || 5,
      remaining_tickets: Number(eventData.remaining_tickets || eventData.tatkal_quota || 5),
      ticket_price: Number(eventData.ticket_price) || 0,
      mutex_enabled: eventData.mutex_enabled !== undefined ? Boolean(eventData.mutex_enabled) : true,
      status: "ACTIVE",
      badge: `${eventData.remaining_tickets || 5} Seats Left`,
      category: eventData.category || "General Hackathon"
    };
    this._data.hackathons.push(newEvent);
    this.save();
    return newEvent;
  }

  updateHackathon(id, updates) {
    const event = this.getHackathonById(id);
    if (!event) return null;
    Object.assign(event, updates);
    this.save();
    return event;
  }

  toggleMutex(id) {
    const event = this.getHackathonById(id);
    if (!event) return null;
    event.mutex_enabled = !event.mutex_enabled;
    this.save();
    return event;
  }

  // --- Teams & Registrations ---
  getTeamsByHackathon(hackathonId) {
    const numId = Number(hackathonId);
    return this._data.teams.filter(t => t.hackathon_id === numId);
  }

  getAllTeams() {
    return [...this._data.teams];
  }

  getTeamById(id) {
    return this._data.teams.find(t => t.id === id) || null;
  }

  createTeamBooking(bookingData) {
    const teamId = `TEAM-${Date.now().toString().slice(-5)}-${Math.floor(Math.random() * 900 + 100)}`;
    const ticketCode = `TKT-TATKAL-${Math.floor(Math.random() * 90000 + 10000)}`;

    const newTeam = {
      id: teamId,
      hackathon_id: Number(bookingData.hackathon_id),
      team_name: bookingData.team_name,
      leader_name: bookingData.leader_name,
      leader_email: bookingData.leader_email,
      members: Array.isArray(bookingData.members) ? bookingData.members : [],
      ticket_code: ticketCode,
      payment_status: bookingData.payment_status || "PAID_TEST_MODE",
      payment_id: bookingData.payment_id || `pay_test_${Math.random().toString(36).substring(2, 10)}`,
      booked_at: new Date().toISOString(),
      is_checked_in: false,
      checked_in_at: null
    };

    this._data.teams.push(newTeam);
    this.save();
    return newTeam;
  }

  checkInTicket(ticketCode) {
    const team = this._data.teams.find(t => t.ticket_code === ticketCode);
    if (!team) return { success: false, message: "Ticket code not found." };
    if (team.is_checked_in) {
      return { success: false, message: "Ticket already checked in!", team };
    }
    team.is_checked_in = true;
    team.checked_in_at = new Date().toISOString();
    this.save();
    return { success: true, message: "Check-in successful! Welcome team.", team };
  }

  // --- Audit Logs ---
  addAuditLog(entry) {
    const logEntry = {
      id: `LOG-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      timestamp: new Date().toISOString(),
      ...entry
    };
    this._data.audit_logs.unshift(logEntry);
    if (this._data.audit_logs.length > 500) {
      this._data.audit_logs = this._data.audit_logs.slice(0, 500);
    }
    this.save();
    return logEntry;
  }

  getAuditLogs(limit = 100) {
    return this._data.audit_logs.slice(0, limit);
  }

  clearAuditLogs() {
    this._data.audit_logs = [];
    this.save();
  }

  // --- Reset to Baseline for Viva Demonstrations ---
  resetAll() {
    this._data.hackathons = JSON.parse(JSON.stringify(INITIAL_HACKATHONS));
    this._data.teams = JSON.parse(JSON.stringify(INITIAL_TEAMS));
    this._data.audit_logs = [];
    this.save();
    return {
      hackathons: this._data.hackathons,
      teams: this._data.teams
    };
  }
}

const dbInstance = new Database();
module.exports = dbInstance;
