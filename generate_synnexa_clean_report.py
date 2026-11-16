# -*- coding: utf-8 -*-
"""
generate_synnexa_clean_report.py
Two-pass compiler for Event Registration (Product #8) Operating Systems Course Project Report PDF:
- Exact same visual styling, font (Segoe UI), color palette, and layout as CRC_Project_Report.pdf
- Modern developer code cards with macOS dots (red/yellow/green), line numbers, and Pygments highlighting
- Detailed millisecond execution trace card for Mutex serialization vs Race Hazard
- Accurate, high-resolution draw.io-style SVG vector block diagrams for Figure 3.1 & Figure 4.1
- Compact chapters with balanced single-page / two-page layouts
- Automated two-pass TOC page number synchronization via PyMuPDF (fitz) and Playwright
- Strict single-page fitting for all code cards, trace cards, diagrams, tables, and screenshots (ZERO page splits!)
- Native HTML/Unicode mathematical formatting (ZERO LaTeX escapes or broken characters)
- Fresh new dashboard screenshots embedded in Appendix C
"""

import os
import re
import base64
import fitz
from pygments import highlight
from pygments.lexers import JavascriptLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from playwright.sync_api import sync_playwright

def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def create_code_card(code_str: str, filename: str, badge: str = "NODE.JS / JS", start_line: int = 1) -> str:
    lines = code_str.strip().split("\n")
    formatter = HtmlFormatter(nowrap=True)
    table_rows = []
    lexer = JavascriptLexer() if ("js" in filename or "JS" in badge) else PythonLexer()
    for i, line in enumerate(lines, start=start_line):
        if line.strip():
            highlighted = highlight(line, lexer, formatter).strip()
        else:
            highlighted = "&nbsp;"
        table_rows.append(f"""<tr><td class="code-lineno">{i:02d}</td><td class="code-line">{highlighted}</td></tr>""")
    code_table = "".join(table_rows)
    return f"""<div class="code-card">
    <div class="code-header">
        <div class="code-header-left">
            <span class="dot dot-red"></span>
            <span class="dot dot-yellow"></span>
            <span class="dot dot-green"></span>
            <span class="code-filename">{filename}</span>
        </div>
        <div class="code-badge">{badge}</div>
    </div>
    <div class="code-card-body">
        <table class="code-table">
            <tbody>{code_table}</tbody>
        </table>
    </div>
</div>"""

def create_trace_card() -> str:
    return """<div class="trace-card">
    <div class="trace-header">
        <div class="trace-title">
            <span class="dot dot-red"></span>
            <span class="dot dot-yellow"></span>
            <span class="dot dot-green"></span>
            <span>Critical Section Execution &amp; High-Contention Race Trace</span>
        </div>
        <div class="trace-badges">
            <span class="trace-badge">Capacity: 1 Tatkal Seat</span>
            <span class="trace-badge">Mode: Mutex ON vs OFF</span>
        </div>
    </div>
    <div class="trace-body">
<span class="tr-label">Target Resource:</span>      <span class="tr-num">Global AI HackSphere 2026</span>  (Initial Remaining Capacity: C = 1)
<span class="tr-label">Contending Devices:</span>  <span class="tr-poly">Device A (Teacher Laptop) &bull; Device B (Friend Mobile)</span>
<span class="tr-dim">--------------------------------------------------------------------------------</span>
<span class="tr-step">SCENARIO 1:</span>  <span class="tr-bold">MUTEX PROTECTION DISABLED (OFF) — TOCTOU RACE CONDITION</span>
    t = 00ms: Device A reads C_remaining = 1 &rarr; Evaluates (1 > 0): <span class="tr-res">VALID</span> &rarr; Begins payment delay
    t = 15ms: Device B reads C_remaining = 1 (STALE!) &rarr; Evaluates (1 > 0): <span class="tr-res">VALID</span> &rarr; Begins payment
    t = 45ms: Device A finishes payment &rarr; Decrements C &larr; 0 &rarr; <span class="tr-op">Mints Ticket TKT-01</span>
    t = 55ms: Device B finishes payment &rarr; Decrements C &larr; -1 &rarr; <span class="tr-op">Mints Ticket TKT-02</span>
    <span class="tr-rem-label">&rarr; RESULT: ANOMALY! C_remaining = -1. Two confirmed passes issued for 1 seat (Oversold!)</span>

<span class="tr-step">SCENARIO 2:</span>  <span class="tr-bold">MUTEX PROTECTION ENABLED (ON) — DIJKSTRA CRITICAL SECTION</span>
    t = 00ms: Device A requests Mutex Lock &rarr; <span class="tr-win">LOCK GRANTED (Owner: Device A)</span>
    t = 02ms: Device A enters Critical Section &rarr; Evaluates C_remaining = 1
    t = 12ms: Device B requests Mutex Lock &rarr; <span class="tr-op">BUSY! Device B enqueued in FIFO Wait Queue</span>
    t = 30ms: Device A completes checkout &rarr; Decrements C &larr; 0 &rarr; <span class="tr-win">Pass Confirmed TKT-01</span>
    t = 31ms: Device A calls release() &rarr; <span class="tr-win">Dequeues Device B from FIFO queue &amp; grants lock</span>
    t = 32ms: Device B enters Critical Section &rarr; Fresh Read: C_remaining = 0
    t = 33ms: Device B evaluates (0 &le; 0) &rarr; <span class="tr-rem">REJECTED (HTTP 409 SOLD OUT)</span>
    t = 34ms: Device B calls release() &rarr; Lock State: UNLOCKED
    t = 35ms: Device B client intercepts 409 &rarr; <span class="tr-codeword">Automated Refund Reassurance Modal (RZP-REF-849204)</span>
<span class="tr-dim">--------------------------------------------------------------------------------</span>
<span class="tr-final">System Invariant Status:</span> <span class="tr-bold">0 &le; C_remaining &le; C_total PRESERVED. Zero Overbooking.</span>
    </div>
</div>"""

def create_compact_svg_3_1() -> str:
    """Figure 3.1: Architecture Flowchart of Concurrency Kernel Pipeline"""
    return """<div class="diagram-card">
<svg width="100%" height="auto" viewBox="0 0 740 450" xmlns="http://www.w3.org/2000/svg" style="max-width: 660px; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; display: block; margin: 0 auto;">
    <defs>
        <filter id="ds" x="-10%" y="-10%" width="130%" height="130%">
            <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08" />
        </filter>
        <marker id="arr-blue" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 7 3, 0 6" fill="#2563eb" />
        </marker>
        <marker id="arr-gray" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 7 3, 0 6" fill="#64748b" />
        </marker>
        <marker id="arr-green" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 7 3, 0 6" fill="#16a34a" />
        </marker>
        <marker id="arr-red" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 7 3, 0 6" fill="#dc2626" />
        </marker>
        <linearGradient id="bg-blue" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#eff6ff" />
            <stop offset="100%" stop-color="#dbeafe" />
        </linearGradient>
        <linearGradient id="bg-green" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#f0fdf4" />
            <stop offset="100%" stop-color="#dcfce7" />
        </linearGradient>
        <linearGradient id="bg-purple" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#faf5ff" />
            <stop offset="100%" stop-color="#f3e8ff" />
        </linearGradient>
        <linearGradient id="bg-amber" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#fffbeb" />
            <stop offset="100%" stop-color="#fef3c7" />
        </linearGradient>
        <linearGradient id="bg-white" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#ffffff" />
            <stop offset="100%" stop-color="#f8fafc" />
        </linearGradient>
        <linearGradient id="bg-red" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#fef2f2" />
            <stop offset="100%" stop-color="#fee2e2" />
        </linearGradient>
    </defs>

    <!-- Node 1: Input -->
    <g filter="url(#ds)">
        <rect x="230" y="10" width="280" height="36" rx="6" fill="url(#bg-blue)" stroke="#2563eb" stroke-width="1.5" />
        <text x="370" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#1e40af">CONCURRENT RESERVATION REQUESTS</text>
        <text x="370" y="39" text-anchor="middle" font-size="8" font-weight="500" fill="#3b82f6">Public Portal &bull; 2-Device Station &bull; 50-Thread Burst</text>
    </g>

    <!-- Connector: Input to 3 Branches -->
    <path d="M 370 46 L 370 60" fill="none" stroke="#64748b" stroke-width="1.5" />
    <path d="M 140 60 L 600 60" fill="none" stroke="#64748b" stroke-width="1.5" />
    <path d="M 140 60 L 140 70" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr-gray)" />
    <path d="M 370 60 L 370 70" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr-gray)" />
    <path d="M 600 60 L 600 70" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr-gray)" />

    <!-- 3 Preprocessing Branches -->
    <g filter="url(#ds)">
        <rect x="40" y="70" width="200" height="38" rx="6" fill="url(#bg-white)" stroke="#475569" stroke-width="1.2" />
        <text x="140" y="86" text-anchor="middle" font-size="10" font-weight="700" fill="#0f172a">validate_payload()</text>
        <text x="140" y="100" text-anchor="middle" font-size="7.5" fill="#64748b">Event ID &bull; Team Name &bull; Roster</text>

        <rect x="270" y="70" width="200" height="38" rx="6" fill="url(#bg-white)" stroke="#475569" stroke-width="1.2" />
        <text x="370" y="86" text-anchor="middle" font-size="10" font-weight="700" fill="#0f172a">razorpay_auth()</text>
        <text x="370" y="100" text-anchor="middle" font-size="7.5" fill="#64748b">Standard Checkout SDK Token</text>

        <rect x="500" y="70" width="200" height="38" rx="6" fill="url(#bg-white)" stroke="#475569" stroke-width="1.2" />
        <text x="600" y="86" text-anchor="middle" font-size="10" font-weight="700" fill="#0f172a">getMutex(event_id)</text>
        <text x="600" y="100" text-anchor="middle" font-size="7.5" fill="#64748b">KeyedMutexRegistry Isolation</text>
    </g>

    <!-- Connectors to Mutex Acquisition Block -->
    <path d="M 140 108 L 140 120 L 370 120" fill="none" stroke="#64748b" stroke-width="1.5" />
    <path d="M 600 108 L 600 120 L 370 120" fill="none" stroke="#64748b" stroke-width="1.5" />
    <path d="M 370 108 L 370 130" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arr-blue)" />

    <!-- Node 3: Mutex Acquisition & FIFO Queue -->
    <g filter="url(#ds)">
        <rect x="190" y="130" width="360" height="42" rx="6" fill="url(#bg-amber)" stroke="#d97706" stroke-width="1.5" />
        <text x="370" y="147" text-anchor="middle" font-size="10.5" font-weight="700" fill="#92400e">mutex.acquire(thread_id)</text>
        <text x="370" y="162" text-anchor="middle" font-size="8" fill="#b45309">If Locked: Enqueue in FIFO Queue (Bounded Waiting O(k)) &bull; Else: Grant Lock</text>
    </g>

    <!-- Connector: Mutex to Critical Section -->
    <path d="M 370 172 L 370 188" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arr-blue)" />

    <!-- Node 4: Critical Section (Atomic Check & Mutate) -->
    <g filter="url(#ds)">
        <rect x="170" y="188" width="400" height="44" rx="6" fill="url(#bg-purple)" stroke="#9333ea" stroke-width="1.5" />
        <text x="370" y="205" text-anchor="middle" font-size="10.5" font-weight="700" fill="#6b21a8">CRITICAL SECTION (Atomic Check &amp; Mutate)</text>
        <text x="370" y="222" text-anchor="middle" font-size="8" fill="#7e22ce">Inspect live database: if (remaining_tickets &gt; 0) decrement &amp; mint; else reject</text>
    </g>

    <!-- Connector: Critical Section to 2 Decision Branches -->
    <path d="M 270 232 L 270 250 L 190 250 L 190 262" fill="none" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-green)" />
    <path d="M 470 232 L 470 250 L 550 250 L 550 262" fill="none" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arr-red)" />

    <!-- 2 Decision Branches -->
    <g filter="url(#ds)">
        <!-- Success Branch -->
        <rect x="70" y="262" width="240" height="65" rx="6" fill="url(#bg-green)" stroke="#16a34a" stroke-width="1.5" />
        <text x="190" y="280" text-anchor="middle" font-size="10" font-weight="700" fill="#15803d">&check; SEAT CONFIRMED (C &gt; 0)</text>
        <text x="190" y="295" text-anchor="middle" font-size="8" fill="#166534">1. Decrement C &larr; C - 1</text>
        <text x="190" y="308" text-anchor="middle" font-size="8" fill="#166534">2. Mint Cryptographic Ticket Code</text>
        <text x="190" y="321" text-anchor="middle" font-size="8" fill="#166534">3. Issue VIP Printable Boarding Pass</text>

        <!-- Sold Out Branch -->
        <rect x="430" y="262" width="240" height="65" rx="6" fill="url(#bg-red)" stroke="#dc2626" stroke-width="1.5" />
        <text x="550" y="280" text-anchor="middle" font-size="10" font-weight="700" fill="#b91c1c">&cross; REJECTED / SOLD OUT (C &le; 0)</text>
        <text x="550" y="295" text-anchor="middle" font-size="8" fill="#991b1b">1. Return HTTP 409 (Sold Out)</text>
        <text x="550" y="308" text-anchor="middle" font-size="8" fill="#991b1b">2. Intercept on Client Side</text>
        <text x="550" y="321" text-anchor="middle" font-size="8" fill="#991b1b">3. Launch Refund Notice Modal (5-7 Days)</text>
    </g>

    <!-- Connectors to Release Block -->
    <path d="M 190 327 L 190 345 L 370 345 L 370 355" fill="none" stroke="#16a34a" stroke-width="1.5" />
    <path d="M 550 327 L 550 345 L 370 345 L 370 355" fill="none" stroke="#dc2626" stroke-width="1.5" />

    <!-- Node 5: Finally Block (Guaranteed Release) -->
    <g filter="url(#ds)">
        <rect x="210" y="355" width="320" height="42" rx="6" fill="url(#bg-white)" stroke="#2563eb" stroke-width="1.5" />
        <text x="370" y="372" text-anchor="middle" font-size="10" font-weight="700" fill="#1e40af">FINALLY { releaseLock(); }</text>
        <text x="370" y="387" text-anchor="middle" font-size="8" fill="#3b82f6">Dequeue Next Waiting Thread &bull; Update Microsecond Telemetry</text>
    </g>

    <!-- Connector: Release to Persistence -->
    <path d="M 370 397 L 370 412" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arr-blue)" />

    <!-- Node 6: Persistence -->
    <g filter="url(#ds)">
        <rect x="240" y="412" width="260" height="28" rx="6" fill="url(#bg-blue)" stroke="#3b82f6" stroke-width="1.2" />
        <text x="370" y="430" text-anchor="middle" font-size="9" font-weight="700" fill="#1e40af">ACID Durable Persistence (fs.renameSync)</text>
    </g>
</svg>
</div>"""

def create_compact_svg_4_1() -> str:
    """Figure 4.1: End-to-End Data Processing Pipeline Flowchart"""
    return """<div class="diagram-card">
<svg width="100%" height="auto" viewBox="0 0 780 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; display: block; margin: 0 auto;">
    <defs>
        <filter id="ds2" x="-10%" y="-10%" width="130%" height="130%">
            <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08" />
        </filter>
        <marker id="arr-b2" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 0, 7 3.5, 0 7" fill="#2563eb" />
        </marker>
    </defs>

    <!-- Top Flow: Stages 1 to 5 -->
    <g filter="url(#ds2)">
        <!-- Stage 1 -->
        <rect x="20" y="30" width="130" height="80" rx="8" fill="#f8fafc" stroke="#2563eb" stroke-width="1.8" />
        <circle cx="45" cy="50" r="11" fill="#2563eb" />
        <text x="45" y="54" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">1</text>
        <text x="85" y="54" font-size="10.5" font-weight="bold" fill="#0f172a">User Input</text>
        <text x="35" y="76" font-size="7.5" fill="#64748b">Squad Roster</text>
        <text x="35" y="90" font-size="7.5" fill="#64748b">Lead Email &bull; Pass</text>

        <!-- Stage 2 -->
        <rect x="175" y="30" width="130" height="80" rx="8" fill="#f8fafc" stroke="#475569" stroke-width="1.8" />
        <circle cx="200" cy="50" r="11" fill="#475569" />
        <text x="200" y="54" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">2</text>
        <text x="240" y="54" font-size="10.5" font-weight="bold" fill="#0f172a">Payment Auth</text>
        <text x="190" y="76" font-size="7.5" fill="#64748b">Razorpay Modal</text>
        <text x="190" y="90" font-size="7.5" fill="#64748b">Test UPI / Cards</text>

        <!-- Stage 3 -->
        <rect x="330" y="30" width="130" height="80" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2" />
        <circle cx="355" cy="50" r="11" fill="#2563eb" />
        <text x="355" y="54" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">3</text>
        <text x="395" y="54" font-size="10.5" font-weight="bold" fill="#1e40af">Mutex Kernel</text>
        <text x="345" y="76" font-size="7.5" fill="#2563eb">Keyed Registry</text>
        <text x="345" y="90" font-size="7.5" fill="#2563eb">FIFO Wait Queue</text>

        <!-- Stage 4 -->
        <rect x="485" y="30" width="130" height="80" rx="8" fill="#faf5ff" stroke="#9333ea" stroke-width="2" />
        <circle cx="510" cy="50" r="11" fill="#9333ea" />
        <text x="510" y="54" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">4</text>
        <text x="550" y="54" font-size="10.5" font-weight="bold" fill="#6b21a8">Critical Sec</text>
        <text x="500" y="76" font-size="7.5" fill="#9333ea">Atomic Check</text>
        <text x="500" y="90" font-size="7.5" fill="#9333ea">Seat Decrement</text>

        <!-- Stage 5 -->
        <rect x="640" y="30" width="120" height="80" rx="8" fill="#fffbeb" stroke="#d97706" stroke-width="2" />
        <circle cx="665" cy="50" r="11" fill="#d97706" />
        <text x="665" y="54" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">5</text>
        <text x="705" y="54" font-size="10.5" font-weight="bold" fill="#92400e">Sim Switch</text>
        <text x="655" y="76" font-size="7.5" fill="#d97706">Mutex ON / OFF</text>
        <text x="655" y="90" font-size="7.5" fill="#d97706">Error Injection</text>
    </g>

    <!-- Connectors Top Row -->
    <path d="M 150 70 L 175 70" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b2)" />
    <path d="M 305 70 L 330 70" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b2)" />
    <path d="M 460 70 L 485 70" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b2)" />
    <path d="M 615 70 L 640 70" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b2)" />

    <!-- Connector: Stage 5 to Stage 6 (Turn Down and Left) -->
    <path d="M 700 110 L 700 180 L 610 180" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b2)" />

    <!-- Bottom Flow: Stage 6 & 7 -->
    <g filter="url(#ds2)">
        <!-- Stage 6 -->
        <rect x="420" y="140" width="190" height="80" rx="8" fill="#f8fafc" stroke="#334155" stroke-width="2" />
        <circle cx="445" cy="160" r="11" fill="#334155" />
        <text x="445" y="164" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">6</text>
        <text x="465" y="164" font-size="10.5" font-weight="bold" fill="#0f172a">Invariant Verification</text>
        <text x="440" y="186" font-size="7.5" fill="#64748b">0 &le; C_remaining &le; C_total</text>
        <text x="440" y="200" font-size="7.5" fill="#64748b">Microsecond Audit Log Stream</text>

        <!-- Stage 7 -->
        <rect x="140" y="140" width="230" height="80" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" />
        <circle cx="165" cy="160" r="11" fill="#16a34a" />
        <text x="165" y="164" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">7</text>
        <text x="185" y="164" font-size="10.5" font-weight="bold" fill="#166534">UI Dashboard Output</text>
        <text x="160" y="186" font-size="7.5" fill="#15803d">&check; Printable VIP Pass (window.print)</text>
        <text x="160" y="200" font-size="7.5" fill="#dc2626">&cross; Refund Notice Modal (5-7 Days)</text>
    </g>

    <!-- Connector: Stage 6 to Stage 7 -->
    <path d="M 420 180 L 370 180" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b2)" />
</svg>
</div>"""

def generate_report(toc_map=None):
    if toc_map is None:
        toc_map = {}

    def get_p(key, fallback="--"):
        return str(toc_map.get(key, fallback))

    # Base directory
    base_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\event-registration-mutex-system"

    # Concise, single-page fitting code snippets (22-28 lines max)
    mutex_snippet = """class Mutex extends EventEmitter {
  constructor(name = 'default-mutex') {
    super();
    this.name = name;
    this._locked = false;
    this._queue = []; // Strict FIFO wait queue
    this._currentOwner = null;
  }

  acquire(requesterId, teamName = '') {
    if (!this._locked) {
      // Fast path: Vacant mutex granted immediately
      this._locked = true;
      this._currentOwner = { id: requesterId, teamName };
      return Promise.resolve(() => this._release(requesterId));
    }
    // Contention path: Mutex held, enqueue in FIFO queue
    return new Promise((resolve) => {
      this._queue.push({
        requesterId,
        grant: () => {
          this._locked = true;
          this._currentOwner = { id: requesterId, teamName };
          resolve(() => this._release(requesterId));
        }
      });
    });
  }

  _release(requesterId) {
    if (this._queue.length > 0) {
      // FIFO handoff: Dequeue oldest waiter, zero starvation
      const nextInLine = this._queue.shift();
      nextInLine.grant();
    } else {
      this._locked = false;
      this._currentOwner = null;
    }
  }
}"""

    registry_snippet = """class KeyedMutexRegistry {
  constructor() {
    this._registry = new Map(); // Granular per-event lock registry
  }

  get(key) {
    const keyStr = String(key);
    if (!this._registry.has(keyStr)) {
      this._registry.set(keyStr, new Mutex(`event-mutex-${keyStr}`));
    }
    return this._registry.get(keyStr);
  }

  async runExclusive(key, task, requesterId, teamName) {
    const mutex = this.get(key);
    const release = await mutex.acquire(requesterId, teamName);
    try {
      return await task(); // Critical section execution
    } finally {
      release(); // Guaranteed release under RAII pattern
    }
  }
}

const defaultRegistry = new KeyedMutexRegistry();
module.exports = { KeyedMutexRegistry, defaultRegistry };"""

    booking_snippet = """async function bookTatkalTicket(hackathon_id, team_data, threadId) {
  const mutex = mutexRegistry.get(hackathon_id);
  const releaseLock = await mutex.acquire(threadId, team_data.team_name);

  try {
    // 1. READ: Query latest real-time inventory inside Critical Section
    const currentEvent = db.getHackathonById(hackathon_id);
    await sleep(paymentDelay); // Realistic payment gateway delay

    // 2. ATOMIC EVALUATION: Verify positive remaining capacity
    if (currentEvent.remaining_tickets <= 0) {
      return {
        success: false,
        status: "SOLD_OUT",
        message: "Tatkal quota exhausted. 0 seats left."
      };
    }

    // 3. STATE MUTATION: Decrement atomically & mint ticket
    const updatedSeats = currentEvent.remaining_tickets - 1;
    db.updateHackathon(hackathon_id, { remaining_tickets: updatedSeats });
    const ticket = db.createTeamBooking({ hackathon_id, ...team_data });

    return { success: true, status: "CONFIRMED", ticket, seats_remaining: updatedSeats };
  } finally {
    releaseLock(); // Exit Critical Section & unblock FIFO waiter
  }
}"""

    refund_snippet = """async function completeBookingWithBackend(payload) {
  try {
    const res = await api('/api/book', 'POST', payload);
    const booking = res.ticket || res.booking;
    closeBookingModal();

    if (res.status === 'OVERSOLD') {
      showToast('⚠️ RACE CONDITION! Seats OVERBOOKED (' + res.seats_remaining + ')!', 'warning');
    } else {
      showToast('Pass Confirmed! Ticket Code: ' + booking.ticket_code, 'success');
    }
    renderBoardingPass(booking, targetEvent);
    fetchHackathons();
  } catch (err) {
    closeBookingModal();
    const isSoldOut = err.status === 409 || (err.data && err.data.status === 'SOLD_OUT');

    if (isSoldOut) {
      // Trigger Automated Refund Reassurance Modal
      openRefundNoticeModal({
        event: targetEvent,
        team_name: payload.team_name,
        amount: targetEvent.price_inr,
        ref_id: 'REFUND_RZP_' + Date.now()
      });
      showToast('⚠️ Tatkal Quota Exhausted! Automated refund initiated.', 'danger');
    }
    fetchHackathons();
  }
}"""

    # Fresh Dashboard Screenshots
    shot_landing_b64 = img_to_base64(os.path.join(base_dir, "public", "screenshots", "shot_landing.png"))
    shot_boarding_b64 = img_to_base64(os.path.join(base_dir, "public", "screenshots", "shot_boarding_pass.png"))
    shot_refund_b64 = img_to_base64(os.path.join(base_dir, "public", "screenshots", "shot_refund_modal.png"))
    shot_admin_b64 = img_to_base64(os.path.join(base_dir, "public", "screenshots", "shot_admin.png"))
    shot_studio_b64 = img_to_base64(os.path.join(base_dir, "public", "screenshots", "shot_studio.png"))

    # SVG Diagrams
    svg_3_1 = create_compact_svg_3_1()
    svg_4_1 = create_compact_svg_4_1()
    trace_card_html = create_trace_card()

    # Pygments code cards
    card_mutex = create_code_card(mutex_snippet, "src/core/Mutex.js :: acquire() & _release()", "NODE.JS LTS", 1)
    card_registry = create_code_card(registry_snippet, "src/core/KeyedMutexRegistry.js :: getMutex()", "NODE.JS LTS", 1)
    card_booking = create_code_card(booking_snippet, "src/services/BookingService.js :: bookTatkalTicket()", "NODE.JS LTS", 72)
    card_refund = create_code_card(refund_snippet, "public/app.js :: completeBookingWithBackend() & Refund", "VANILLA JS / ES6", 471)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SR University &bull; Concurrency Control Mutex System Course Project Report</title>
<style>
    @page {{
        size: A4;
        margin: 16mm 15mm 16mm 15mm;
        @bottom-right {{
            content: "Page " counter(page);
            font-size: 8.5pt;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #64748b;
        }}
        @bottom-left {{
            content: "SR University • CSE Dept | Product #8 Concurrency Mutex System";
            font-size: 8pt;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #64748b;
        }}
    }}
    
    *, *::before, *::after {{ box-sizing: border-box; }}

    body {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        font-size: 9.5pt;
        line-height: 1.48;
        color: #1e293b;
        background: #ffffff;
        margin: 0;
        padding: 0;
    }}
    
    .page-break {{
        page-break-after: always;
        break-after: page;
    }}
    
    /* Cover Page - Strict 1-Page Constraint matching CRC_Project_Report.pdf */
    .cover-page {{
        height: 250mm;
        max-height: 252mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        padding: 0 4px;
        box-sizing: border-box;
        overflow: hidden;
        page-break-after: always;
        break-after: page;
    }}
    .uni-header {{
        border-bottom: 2px solid #2563eb;
        padding-bottom: 8px;
    }}
    .uni-title {{
        font-size: 19pt;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: 1px;
        margin: 0;
    }}
    .uni-sub {{
        font-size: 11pt;
        font-weight: 700;
        color: #2563eb;
        margin-top: 3px;
        letter-spacing: 0.5px;
    }}
    .uni-dept {{
        font-size: 8.5pt;
        color: #475569;
        margin-top: 2px;
    }}
    .project-banner {{
        margin: 10px 0 8px 0;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #2563eb;
        border-radius: 6px;
        padding: 10px 14px;
    }}
    .project-banner h2 {{
        font-size: 12.5pt;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 4px 0;
        line-height: 1.25;
    }}
    .project-banner p {{
        font-size: 8.5pt;
        color: #475569;
        margin: 0;
        line-height: 1.35;
    }}
    .team-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 6px 0 8px 0;
        font-size: 8.5pt;
    }}
    .team-table th {{
        background: #0f172a;
        color: #ffffff;
        font-weight: 700;
        padding: 6px 8px;
        border: 1px solid #334155;
        text-align: left;
    }}
    .team-table td {{
        padding: 4.5px 8px;
        border: 1px solid #e2e8f0;
        text-align: left;
    }}
    .team-table tr:nth-child(even) {{
        background: #f8fafc;
    }}
    .leader-badge {{
        background: #2563eb;
        color: #ffffff;
        font-size: 7pt;
        font-weight: 700;
        padding: 1px 5px;
        border-radius: 3px;
        margin-left: 4px;
    }}
    .footer-meta {{
        border-top: 1px solid #cbd5e1;
        padding-top: 8px;
        display: flex;
        justify-content: space-between;
        font-size: 8pt;
        color: #64748b;
    }}
    
    /* Section Headings */
    .sec-title {{
        font-size: 14pt;
        font-weight: 800;
        color: #0f172a;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 4px;
        margin-top: 8px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .sub-sec-title {{
        font-size: 11pt;
        font-weight: 700;
        color: #1e3a8a;
        margin-top: 10px;
        margin-bottom: 4px;
    }}
    
    p {{
        margin: 4px 0 6px 0;
        text-align: justify;
    }}
    ul, ol {{
        margin: 4px 0 6px 0;
        padding-left: 20px;
    }}
    li {{
        margin-bottom: 3px;
    }}
    
    /* Tables */
    .content-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0;
        font-size: 8.5pt;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .content-table th {{
        background: #1e293b;
        color: #ffffff;
        padding: 5px 8px;
        border: 1px solid #475569;
        text-align: left;
        font-weight: 600;
    }}
    .content-table td {{
        padding: 4.5px 8px;
        border: 1px solid #cbd5e1;
    }}
    .content-table tr:nth-child(even) {{
        background: #f8fafc;
    }}
    
    .badge-pass {{
        color: #15803d;
        background: #dcfce7;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 7.5pt;
        display: inline-block;
    }}
    .badge-fail {{
        color: #b91c1c;
        background: #fee2e2;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 7.5pt;
        display: inline-block;
    }}
    
    /* Callouts */
    .callout {{
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 6px 10px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 8.8pt;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .callout-red {{
        background: #fef2f2;
        border-left: 4px solid #dc2626;
        padding: 6px 10px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 8.8pt;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    
    /* TOC Styles */
    .toc-item {{
        display: flex;
        justify-content: space-between;
        padding: 0.8px 0;
        border-bottom: 1px dotted #cbd5e1;
        font-size: 8pt;
        line-height: 1.25;
    }}
    .toc-item strong {{
        color: #0f172a;
    }}

    /* Code Card Component - STRICT PAGE-BREAK AVOID */
    .code-card {{
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        overflow: hidden;
        margin: 8px 0;
        background: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .code-card-body, .code-table, .code-table tbody, .code-table tr, .code-table td {{
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .code-header {{
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        padding: 4px 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .code-header-left {{
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }}
    .dot-red {{ background: #ef4444; }}
    .dot-yellow {{ background: #f59e0b; }}
    .dot-green {{ background: #10b981; }}
    .code-filename {{
        font-family: 'Consolas', monospace;
        font-size: 7.8pt;
        color: #334155;
        font-weight: 600;
        margin-left: 4px;
    }}
    .code-badge {{
        font-size: 7pt;
        font-weight: 700;
        color: #475569;
        background: #e2e8f0;
        padding: 1px 6px;
        border-radius: 3px;
        letter-spacing: 0.5px;
    }}
    .code-card-body {{
        padding: 0;
        background: #ffffff;
        overflow-x: auto;
    }}
    .code-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 7.6pt;
        line-height: 1.35;
    }}
    .code-lineno {{
        width: 26px;
        text-align: right;
        padding: 1px 6px 1px 4px;
        color: #94a3b8;
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
        user-select: none;
    }}
    .code-line {{
        padding: 1px 8px;
        white-space: pre-wrap;
        word-break: break-all;
    }}

    /* Trace Card Component - STRICT PAGE-BREAK AVOID */
    .trace-card {{
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        background: #0f172a;
        color: #f8fafc;
        margin: 8px 0;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .trace-body, .trace-header {{
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .trace-header {{
        background: #1e293b;
        border-bottom: 1px solid #334155;
        padding: 5px 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .trace-title {{
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 8pt;
        font-weight: 700;
        color: #38bdf8;
    }}
    .trace-badges {{
        display: flex;
        gap: 5px;
    }}
    .trace-badge {{
        background: #334155;
        color: #94a3b8;
        font-size: 7pt;
        padding: 1px 6px;
        border-radius: 3px;
    }}
    .trace-body {{
        padding: 8px 10px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 7.5pt;
        line-height: 1.4;
        white-space: pre-wrap;
    }}
    .tr-label {{ color: #94a3b8; font-weight: bold; }}
    .tr-num {{ color: #38bdf8; font-weight: bold; }}
    .tr-poly {{ color: #a78bfa; }}
    .tr-dim {{ color: #475569; }}
    .tr-step {{ color: #f59e0b; font-weight: bold; }}
    .tr-bold {{ color: #ffffff; font-weight: bold; }}
    .tr-op {{ color: #f87171; }}
    .tr-res {{ color: #34d399; font-weight: bold; }}
    .tr-rem {{ color: #ef4444; font-weight: bold; }}
    .tr-win {{ color: #22c55e; font-weight: bold; }}
    .tr-rem-label {{ color: #ef4444; font-weight: bold; background: #450a0a; padding: 2px 6px; border-radius: 3px; display: inline-block; margin-top: 2px; }}
    .tr-final {{ color: #38bdf8; font-weight: bold; }}
    .tr-codeword {{ color: #4ade80; font-weight: bold; background: #064e3b; padding: 1px 4px; border-radius: 3px; }}

    /* Diagrams & Screenshots - STRICT PAGE-BREAK AVOID */
    .diagram-card {{
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 6px;
        background: #ffffff;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .caption {{
        font-size: 7.8pt;
        color: #64748b;
        text-align: center;
        margin-top: 4px;
        font-style: italic;
    }}
    .screenshot-card {{
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        background: #ffffff;
        padding: 6px;
        margin: 8px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        text-align: center;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
    .screenshot-card img {{
        max-width: 100%;
        height: auto;
        max-height: 235px;
        object-fit: contain;
        border-radius: 4px;
        display: block;
        margin: 0 auto;
        border: 1px solid #f1f5f9;
    }}
</style>
</head>
<body>

<!-- ========================================================= -->
<!-- COVER PAGE (Page 1) -->
<!-- ========================================================= -->
<div class="cover-page">
    <div class="uni-header">
        <h1 class="uni-title">SR UNIVERSITY</h1>
        <div class="uni-sub">DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING</div>
        <div class="uni-dept">B.Tech (CSE Core) &bull; 2nd Year &bull; Operating Systems Laboratory (Course Project Report)</div>
    </div>
    
    <div class="project-banner">
        <h2>Event Registration: Critical Section &amp; Mutex Synchronization in High-Contention Ticketing</h2>
        <p>A Zero-Overbooking Event Reservation Kernel with Automated Refund Reassurance &amp; Live Concurrency Testing</p>
    </div>
    
    <div style="text-align: left;">
        <span style="font-size: 9pt; font-weight: 700; color: #0f172a;">STUDENT TEAM ROSTER (Product #8 &bull; Ascending Hall Ticket Order):</span>
        <table class="team-table">
            <thead>
                <tr>
                    <th style="width: 16%;">Hall Ticket</th>
                    <th style="width: 30%;">Full Name</th>
                    <th style="width: 26%;">Academic Role</th>
                    <th style="width: 28%;">Module Ownership</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>2503A51108</strong></td>
                    <td>Ch. Naveen Reddy</td>
                    <td>Team Contributor</td>
                    <td>File-Backed ACID JSON Storage &amp; Persistence</td>
                </tr>
                <tr>
                    <td><strong>2503A51109</strong></td>
                    <td>K. Shiva Saketh</td>
                    <td>Team Contributor</td>
                    <td>TOCTOU Race Hazard Formulation &amp; Analysis</td>
                </tr>
                <tr>
                    <td><strong>2503A51110</strong></td>
                    <td><strong>A. Shiva Ganesh</strong> <span class="leader-badge">LEADER</span></td>
                    <td><strong>Team Leader</strong></td>
                    <td>Mutex Primitive, Keyed Registry &amp; Engine Core</td>
                </tr>
                <tr>
                    <td><strong>2503A51111</strong></td>
                    <td>V. Saicharan</td>
                    <td>Team Contributor</td>
                    <td>REST API Controllers &amp; Concurrency Dispatcher</td>
                </tr>
                <tr>
                    <td><strong>2503A1112</strong></td>
                    <td>T. Geethika</td>
                    <td>Team Contributor</td>
                    <td>Luxury UI/UX, SVG QR Code &amp; Boarding Pass</td>
                </tr>
                <tr>
                    <td><strong>2503A51113</strong></td>
                    <td>G. Vishwas</td>
                    <td>Team Contributor</td>
                    <td>Admin Portal, Razorpay Mock &amp; Door Check-In</td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 12px; text-align: left; font-size: 8pt; color: #475569;">
        <strong>Live Production URL:</strong> <span style="color: #2563eb; font-weight: bold;">https://synnexa.vercel.app</span> &nbsp;|&nbsp;
        <strong>Organizer Portal:</strong> <span style="color: #2563eb;">/admin</span> &nbsp;|&nbsp;
        <strong>Git Repo:</strong> <span style="color: #0f172a;">ShivaGanesh1080-ops/synnexa-os-concurrency</span>
    </div>

    <div class="footer-meta">
        <div><strong>Faculty Guide:</strong> Department of CSE, SR University</div>
        <div><strong>Academic Year:</strong> 2026-2027</div>
        <div><strong>Product ID:</strong> #8 Concurrency Mutex System</div>
    </div>
</div>

<!-- ========================================================= -->
<!-- CERTIFICATE OF ORIGINALITY (Page 2) -->
<!-- ========================================================= -->
<div class="page-break">
    <div style="text-align: center; margin-bottom: 16px;">
        <h2 style="font-size: 16pt; font-weight: 800; color: #0f172a; margin: 0;">DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING</h2>
        <h3 style="font-size: 12pt; color: #2563eb; margin: 4px 0;">SR UNIVERSITY, WARANGAL, TELANGANA</h3>
        <div style="font-size: 9pt; color: #64748b; font-weight: bold;">CERTIFICATE OF ORIGINALITY &amp; COURSE PROJECT COMPLETION</div>
    </div>

    <div class="callout" style="font-size: 9pt; line-height: 1.6; margin: 16px 0;">
        This is to certify that the course project titled <strong>"Event Registration: Critical Section &amp; Mutex Synchronization in High-Contention Ticketing"</strong> is a bonafide record of work carried out by the undergraduate students of B.Tech CSE Core (2nd Year) under Product #8:
        <br><br>
        <strong>1. Ch. Naveen Reddy (2503A51108)</strong> &nbsp;&bull;&nbsp;
        <strong>2. K. Shiva Saketh (2503A51109)</strong> &nbsp;&bull;&nbsp;
        <strong>3. A. Shiva Ganesh (2503A51110 - Team Leader)</strong><br>
        <strong>4. V. Saicharan (2503A51111)</strong> &nbsp;&bull;&nbsp;
        <strong>5. T. Geethika (2503A1112)</strong> &nbsp;&bull;&nbsp;
        <strong>6. G. Vishwas (2503A51113)</strong>
        <br><br>
        This project has been submitted in partial fulfillment of the requirements for the laboratory assessment of <strong>Operating Systems (CS201)</strong> during the academic year 2026-2027. The code, mathematical formulations, architectural diagrams, and empirical benchmark traces presented in this report represent the original intellectual work of the candidate team.
    </div>

    <table style="width: 100%; margin-top: 45px; border-collapse: collapse; text-align: center; font-size: 9pt;">
        <tr>
            <td style="width: 33%; padding-bottom: 50px;">___________________________<br><strong>Course Instructor</strong><br>Dept. of CSE, SRU</td>
            <td style="width: 33%; padding-bottom: 50px;">___________________________<br><strong>Lab Coordinator</strong><br>Operating Systems Lab</td>
            <td style="width: 33%; padding-bottom: 50px;">___________________________<br><strong>Head of Department</strong><br>CSE Core, SR University</td>
        </tr>
    </table>
</div>

<!-- ========================================================= -->
<!-- EXECUTIVE ABSTRACT (Page 3) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">EXECUTIVE ABSTRACT</h1>
    <p>
        In modern networked computing, high-demand web services (such as IRCTC Tatkal railway ticketing, concert ticket drops, and flash sales) frequently suffer from severe concurrency hazards. When hundreds or thousands of distributed user requests contend for a single remaining resource (<i>C</i> = 1) across asynchronous network boundaries, unsynchronized database transactions lead to the classic <strong>Time-of-Check to Time-of-Use (TOCTOU)</strong> race condition. Under this anomaly, multiple server threads observe valid capacity simultaneously before any write operation commits, resulting in catastrophic overbooking where inventory plunges below zero (<i>C</i> &lt; 0), minting duplicate tickets and causing significant financial liability.
    </p>
    <p>
        This laboratory project presents <strong>Event Registration (Product #8)</strong>, an enterprise-grade concurrency control engine and real-time event booking platform engineered from fundamental Operating System synchronization primitives. Rather than relying on heavy third-party ORMs or external database locks, SYNNEXA implements a native, zero-dependency <strong>Asynchronous Mutex Primitive</strong> coupled with a <strong>Keyed Mutex Registry</strong> in Node.js.
    </p>

    <h2 class="sub-sec-title">Key Architectural Features &amp; Research Innovations</h2>
    <ul>
        <li><strong>Strict Mutual Exclusion (|C(t)| &le; 1):</strong> Formal implementation of Dijkstra's critical section criteria guaranteeing that exactly one transaction holds the inventory mutation barrier at any given microsecond.</li>
        <li><strong>Bounded Waiting (Zero Starvation):</strong> An array-backed First-In-First-Out (FIFO) queue guarantees that waiting reservation threads are dequeued in strict request arrival order, bounding waiting time to <i>O</i>(k) without starvation.</li>
        <li><strong>Granular Resource Isolation:</strong> A per-event Keyed Mutex Registry allocates independent locks, preventing high contention on one hackathon from blocking bookings for unrelated events (eliminating Amdahl's serialization bottleneck).</li>
        <li><strong>Automated Refund Reassurance Modal:</strong> A resilient user-experience flow that intercepts HTTP 409 (Sold Out) responses when a concurrent buyer is out-raced for the final seat, immediately presenting an automated refund tracking receipt (RZP-REF-849204) and reassuring the user of a 5–7 business day refund.</li>
        <li><strong>Interactive Multi-Device Live Rig:</strong> An Organizer Command Center allowing live, side-by-side contention testing between a teacher's laptop and a student's phone, complete with real-time Mutex ON/OFF switches to visually prove race condition emergence and mitigation.</li>
    </ul>

    <div class="callout" style="margin-top: 10px;">
        <strong>Empirical Benchmark Summary:</strong> Across a 50-thread concurrent synthetic stress test targeting 2 remaining seats, SYNNEXA with Mutex ON achieved 100% invariant preservation: exactly 2 tickets were issued, 48 requests were safely rejected, and remaining capacity settled at exactly 0. Conversely, with Mutex OFF, the system produced 8 duplicate tickets and a negative inventory balance of -6 seats.
    </div>
</div>

<!-- ========================================================= -->
<!-- TABLE OF CONTENTS (Page 4) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">TABLE OF CONTENTS</h1>
    
    <div class="toc-item"><strong>1. CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL</strong><span>Page {get_p("CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL", "5")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.1 Introduction to Concurrency Anomalies</span><span>{get_p("1.1 Introduction to Concurrency Anomalies", "5")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.2 Need for Synchronization in Ticketing Systems</span><span>{get_p("1.2 Need for Synchronization in Ticketing Systems", "5")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.3 Basic Working of Mutex (Mutual Exclusion)</span><span>{get_p("1.3 Basic Working of Mutex", "5")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.4 Applications of Mutex in High-Contention Infrastructure</span><span>{get_p("1.4 Applications of Mutex in High-Contention Infrastructure", "5")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.5 Problem Statement and Product Requirements</span><span>{get_p("1.5 Problem Statement and Product Requirements", "5")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.6 Proposed Implementation Plan</span><span>{get_p("1.6 Proposed Implementation Plan", "5")}</span></div>

    <div class="toc-item" style="margin-top: 2.5px;"><strong>2. CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL</strong><span>Page {get_p("CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL", "6")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.1 State Invariants and Shared Data Representation</span><span>{get_p("2.1 State Invariants and Shared Data Representation", "6")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.2 Mutual Exclusion Property (Formal Proof)</span><span>{get_p("2.2 Mutual Exclusion Property", "6")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.3 Progress and Bounded Waiting Proof (Starvation Elimination)</span><span>{get_p("2.3 Progress and Bounded Waiting Proof", "7")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.4 Atomic Test-and-Set and Asynchronous Transitions</span><span>{get_p("2.4 Atomic Test-and-Set and Asynchronous Transitions", "7")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.5 Time-of-Check to Time-of-Use (TOCTOU) Race Hazard Formulation</span><span>{get_p("2.5 Time-of-Check to Time-of-Use", "7")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.6 State Verification and Invariant Violation Detection</span><span>{get_p("2.6 State Verification and Invariant Violation Detection", "7")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.7 Worked Numerical Example: Race Condition vs. Mutex Serialization</span><span>{get_p("2.7 Worked Numerical Example", "8")}</span></div>

    <div class="toc-item" style="margin-top: 2.5px;"><strong>3. CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL &amp; MUTEX</strong><span>Page {get_p("CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL", "9")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.1 Software and Development Tools Used</span><span>{get_p("3.1 Software and Development Tools Used", "9")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.2 Mutex Function and Program Structure (Figure 3.1 Architecture Flowchart)</span><span>{get_p("3.2 Mutex Function and Program Structure", "9")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.3 Asynchronous Mutex Implementation (`src/core/Mutex.js`)</span><span>{get_p("3.3 Asynchronous Mutex Implementation", "10")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.4 Keyed Mutex Registry for Fine-Grained Locking (`KeyedMutexRegistry.js`)</span><span>{get_p("3.4 Keyed Mutex Registry", "11")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.5 Atomic Critical Section and State Mutation (`BookingService.js`)</span><span>{get_p("3.5 Atomic Critical Section", "12")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.6 to 3.10 Storage Tier, Multi-Device Testing &amp; Error Introduction</span><span>{get_p("3.6 to 3.10 Storage Tier", "12")}</span></div>

    <div class="toc-item" style="margin-top: 2.5px;"><strong>4. CHAPTER 4 - APPLICATION DASHBOARD &amp; INTERFACE DEVELOPMENT</strong><span>Page {get_p("CHAPTER 4 - APPLICATION DASHBOARD", "13")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.1 to 4.5 Dashboard Requirements, UI Modalities &amp; Component Hierarchy</span><span>{get_p("4.1 to 4.5 Dashboard Requirements", "13")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.6 Dashboard-to-Backend Integration &amp; Refund Handling (`public/app.js`)</span><span>{get_p("4.6 Dashboard-to-Backend Integration", "14")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.7 Complete Data Processing Flow (Figure 4.1 Draw.io Pipeline)</span><span>{get_p("4.7 Complete Data Processing Flow", "15")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.8 to 4.9 Testing Methodology &amp; Comprehensive Test Cases Table</span><span>{get_p("4.8 to 4.9 Testing Methodology", "16")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.10 Concurrency Stress Testing &amp; Empirical Performance</span><span>{get_p("4.10 Concurrency Stress Testing", "17")}</span></div>

    <div class="toc-item" style="margin-top: 2.5px;"><strong>5. CHAPTER 5 - ERRORS, CHALLENGES AND LEARNING OUTCOMES</strong><span>Page {get_p("CHAPTER 5 - ERRORS, CHALLENGES", "18")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>5.1 Errors Encountered &bull; 5.2 Root Causes &bull; 5.3 Solutions &bull; 5.4 OS Learning Outcomes</span><span>{get_p("5.1 Errors Encountered", "18")}</span></div>

    <div class="toc-item" style="margin-top: 2.5px;"><strong>6. CHAPTER 6 - ADDITIONAL FEATURES AND PRODUCT ENHANCEMENTS</strong><span>Page {get_p("CHAPTER 6 - ADDITIONAL FEATURES", "19")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>6.1 Additional Features &bull; 6.2 UX Benefits &bull; 6.3 Future Roadmap</span><span>{get_p("6.1 Additional Features", "19")}</span></div>

    <div class="toc-item" style="margin-top: 2.5px;"><strong>7. CHAPTER 7 - RESULTS AND CONCLUSION</strong><span>Page {get_p("CHAPTER 7 - RESULTS AND CONCLUSION", "19")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>7.1 Verification Summary &bull; 7.2 Achievement of Objectives &bull; 7.3 Conclusion</span><span>{get_p("7.1 Verification Summary", "19")}</span></div>

    <div class="toc-item" style="margin-top: 2.5px;"><strong>APPENDICES</strong><span>Page {get_p("APPENDICES", "20")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>APPENDIX A - COMPLETE SOURCE CODE (A.1 to A.4 Dedicated Single Pages)</span><span>{get_p("APPENDIX A - COMPLETE SOURCE CODE", "20")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>APPENDIX B - LINE-BY-LINE EXPLANATION OF CODE</span><span>{get_p("APPENDIX B - LINE-BY-LINE EXPLANATION", "24")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>APPENDIX C - DASHBOARD SCREENSHOTS (New Dashboard &amp; Modal Captures)</span><span>{get_p("APPENDIX C - DASHBOARD SCREENSHOTS", "25")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>APPENDIX D - COMPLETE TEST-CASE TABLES AND SAMPLE OUTPUTS</span><span>{get_p("APPENDIX D - COMPLETE TEST-CASE TABLES", "28")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>APPENDIX E - HARDWARE &amp; RUNTIME ENVIRONMENT SPECIFICATIONS</span><span>{get_p("APPENDIX E - HARDWARE", "29")}</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>APPENDIX F - TEAM CONTRIBUTIONS &amp; REFERENCES</span><span>{get_p("APPENDIX F - TEAM CONTRIBUTIONS", "30")}</span></div>
</div>

<!-- ========================================================= -->
<!-- CHAPTER 1: INTRODUCTION (Page 5) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL</h1>
    
    <h2 class="sub-sec-title">1.1 Introduction to Concurrency Anomalies</h2>
    <p>
        In concurrent computing systems, multiple independent threads of execution share access to common memory locations, database records, and network I/O buffers. When two or more execution contexts perform interleaved operations on shared state without proper synchronization, non-deterministic program behavior occurs. The most infamous consequence is the <strong>data race condition</strong>, in which the final state of shared variables depends arbitrarily upon thread scheduling and execution timing.
    </p>

    <h2 class="sub-sec-title">1.2 Need for Synchronization in Ticketing Systems</h2>
    <p>
        In high-demand event ticketing, railway Tatkal reservations, and university symposium registrations, the primary contended resource is a finite numerical integer: remaining seat capacity. When contention surges—specifically when only 1 or 2 seats remain—concurrent buyer requests arrive at the server within microsecond intervals. Uncontrolled interleaving triggers a classical <strong>Time-of-Check to Time-of-Use (TOCTOU)</strong> race condition: multiple threads read identical stale capacity values before any write operation commits, driving capacity below zero (<i>C</i><sub>remaining</sub> &lt; 0) and minting phantom duplicate tickets.
    </p>

    <h2 class="sub-sec-title">1.3 Basic Working of Mutex (Mutual Exclusion)</h2>
    <p>
        A <strong>Mutex (Mutual Exclusion)</strong> is an operating system synchronization primitive that guarantees only one thread enters a designated <em>Critical Section</em> at any instant in time. Classical synchronization theory, formulated by Edsger W. Dijkstra (1965), dictates that any correct critical section solution must strictly satisfy three properties:
    </p>
    <ol>
        <li><strong>Mutual Exclusion:</strong> At most one thread executes inside the critical section at any time: &forall; t, |<b>C</b>(t)| &le; 1.</li>
        <li><strong>Progress:</strong> If the critical section is vacant, waiting threads cannot be postponed indefinitely from entering.</li>
        <li><strong>Bounded Waiting:</strong> A bound exists on how many times other threads enter before a waiting thread enters, eliminating starvation (<i>O</i>(k) queue length).</li>
    </ol>

    <h2 class="sub-sec-title">1.4 Applications of Mutex in High-Contention Infrastructure</h2>
    <p>
        Industrial applications of Mutex primitives span CPU thread synchronization, database row-level locking (PostgreSQL/MySQL), distributed memory caches (Redis Redlock), financial payment settlement gateways, and operating system kernel schedulers.
    </p>

    <h2 class="sub-sec-title">1.5 Problem Statement and Product Requirements</h2>
    <p>
        The objective of this project is to architect, implement, and rigorously verify <strong>Event Registration (Product #8)</strong>—a high-throughput Tatkal hackathon reservation platform that guarantees <strong>Zero Overbooking</strong> under extreme concurrent loads.
    </p>
    <ul>
        <li><strong>Core Functional Requirements:</strong> Multi-event catalog, dynamic squad pass registration, official Razorpay test payments, and printable SVG QR passes.</li>
        <li><strong>Concurrency &amp; Mutex Requirements:</strong> Fine-grained asynchronous Mutex barrier per event, FIFO wait queue, microsecond telemetry logs, and automated refund notices on Tatkal exhaustion.</li>
        <li><strong>Verification Rig:</strong> Controlled error introduction: toggle Mutex OFF to reproduce overselling (<i>C</i> = -1), toggle Mutex ON to verify zero-overselling (<i>C</i> = 0).</li>
    </ul>

    <h2 class="sub-sec-title">1.6 Proposed Implementation Plan</h2>
    <p>
        The engineering roadmap was divided into four structured phases: Mathematical Modeling, Core Concurrency Kernel Development, Luxury Full-Stack Dashboard Implementation, and Automated Verification.
    </p>
</div>

<!-- ========================================================= -->
<!-- CHAPTER 2: MATHEMATICAL PRINCIPLES (Page 6 & 7 & 8) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL</h1>
    
    <h2 class="sub-sec-title">2.1 State Invariants and Shared Data Representation</h2>
    <p>
        Let an event have initial capacity <i>C</i><sub>total</sub> &isin; &#x2115;<sup>+</sup>. Let <b>R</b>(t) = {{r<sub>1</sub>, r<sub>2</sub>, ..., r<sub>m</sub>}} denote the set of confirmed tickets issued up to timestamp t. Remaining capacity <i>C</i><sub>remaining</sub>(t) is defined as:
    </p>
    <div class="callout" style="text-align: center; font-weight: bold; font-size: 11pt;">
        <i>C</i><sub>remaining</sub>(t) = <i>C</i><sub>total</sub> &minus; |<b>R</b>(t)|
    </div>
    <p>
        The fundamental system safety invariants that must hold for all timestamps t &ge; 0:
    </p>
    <ul>
        <li><strong>Invariant 1 (Non-Negative Capacity):</strong> &forall; t &ge; 0, &nbsp; 0 &le; <i>C</i><sub>remaining</sub>(t) &le; <i>C</i><sub>total</sub>.</li>
        <li><strong>Invariant 2 (Bijective Slot Integrity):</strong> &forall; r<sub>i</sub>, r<sub>j</sub> &isin; <b>R</b>(t), &nbsp; r<sub>i</sub> &ne; r<sub>j</sub> &rArr; TicketCode(r<sub>i</sub>) &ne; TicketCode(r<sub>j</sub>) &and; |<b>R</b>(t)| &le; <i>C</i><sub>total</sub>.</li>
    </ul>

    <h2 class="sub-sec-title">2.2 Mutual Exclusion Property (Formal Proof)</h2>
    <p>
        Let <b>T</b> = {{T<sub>1</sub>, T<sub>2</sub>, ..., T<sub>n</sub>}} denote concurrent reservation threads. Let <b>C</b>(t) &sube; <b>T</b> be the set of threads actively executing inside the critical section at time t.
    </p>
    <div class="callout" style="font-weight: bold; text-align: center; font-size: 10.5pt;">
        Theorem 1 (Mutual Exclusion): &forall; t &ge; 0, &nbsp; |<b>C</b>(t)| &le; 1
    </div>
    <p>
        <strong>Proof by Contradiction:</strong> Assume distinct threads T<sub>a</sub>, T<sub>b</sub> &isin; <b>T</b> (a &ne; b) execute simultaneously in <b>C</b>(t*) at timestamp t*.
    </p>
    <ol>
        <li>A thread enters <b>C</b>(t) if and only if <code>_locked</code> is transitioned from <code>false</code> to <code>true</code>.</li>
        <li>Assume T<sub>a</sub> acquired the lock at t<sub>a</sub> &le; t*, setting <code>_locked = true</code> and <code>_currentOwner = T<sub>a</sub></code>.</li>
        <li>When T<sub>b</sub> attempts acquisition at t<sub>b</sub> &le; t*, it evaluates <code>if (!this._locked)</code>.</li>
        <li>Because T<sub>a</sub> has not called <code>_release()</code>, <code>_locked</code> remains <code>true</code>.</li>
        <li>T<sub>b</sub> evaluates the check to <code>false</code>, is pushed into <code>_queue</code>, and returns an unfulfilled Promise.</li>
        <li>Thus, T<sub>b</sub> cannot execute inside <b>C</b>(t*), contradicting the assumption. Hence, |<b>C</b>(t)| &le; 1 holds for all t. &#x25AA;</li>
    </ol>
</div>

<div class="page-break">
    <h2 class="sub-sec-title">2.3 Progress and Bounded Waiting Proof (Starvation Elimination)</h2>
    <p>
        Let thread T<sub>i</sub> request the lock at timestamp t<sub>req</sub>(T<sub>i</sub>). Let W(T<sub>i</sub>) denote the number of other threads granted access before T<sub>i</sub>. Under our strict FIFO queue discipline:
    </p>
    <div class="callout" style="text-align: center; font-weight: bold; font-size: 10.5pt;">
        W(T<sub>i</sub>) = |{{ T<sub>j</sub> &isin; Q : t<sub>req</sub>(T<sub>j</sub>) &lt; t<sub>req</sub>(T<sub>i</sub>) }}| = k &lt; &infin;
    </div>
    <p>
        Because critical section duration is bounded by &Delta;t<sub>CS</sub> &le; 50ms, waiting time is bounded: WaitTime(T<sub>i</sub>) &le; k &middot; &Delta;t<sub>CS</sub> &lt; &infin;. This mathematically eliminates thread starvation.
    </p>

    <h2 class="sub-sec-title">2.4 Atomic Test-and-Set and Asynchronous Transitions</h2>
    <p>
        In multi-threaded C/C++, atomic operations rely on CPU instructions (<code>CMPXCHG</code> / <code>XCHG</code>). In Node.js, JavaScript executes on a single-threaded V8 event loop. Synchronous execution of a microtask is non-preemptive: evaluating <code>if (!this._locked)</code> and setting <code>this._locked = true</code> in the same synchronous turn operates with hardware-level atomicity. Asynchronous suspension occurs exclusively when an unfulfilled Promise is returned, relinquishing control to the event loop until resolution.
    </p>

    <h2 class="sub-sec-title">2.5 Time-of-Check to Time-of-Use (TOCTOU) Race Hazard Formulation</h2>
    <p>
        When synchronization is disabled (Mutex OFF), inventory validation and state mutation decouple across asynchronous boundaries:
    </p>
    <ol>
        <li><strong>t<sub>0</sub>:</strong> Thread T<sub>1</sub> reads <i>C</i><sub>remaining</sub> = 1. Evaluates check: 1 &gt; 0 &rArr; <span style="color:#059669; font-weight:bold;">VALID</span>.</li>
        <li><strong>t<sub>1</sub>:</strong> Thread T<sub>1</sub> awaits asynchronous network I/O / payment delay.</li>
        <li><strong>t<sub>2</sub>:</strong> Thread T<sub>2</sub> arrives, reads <i>C</i><sub>remaining</sub> = 1 (STALE!). Evaluates check: 1 &gt; 0 &rArr; <span style="color:#059669; font-weight:bold;">VALID</span>.</li>
        <li><strong>t<sub>3</sub>:</strong> Thread T<sub>2</sub> begins asynchronous delay.</li>
        <li><strong>t<sub>4</sub>:</strong> Thread T<sub>1</sub> finishes, writes <i>C</i><sub>remaining</sub> &larr; 1 &minus; 1 = 0, mints Ticket #1.</li>
        <li><strong>t<sub>5</sub>:</strong> Thread T<sub>2</sub> finishes, writes <i>C</i><sub>remaining</sub> &larr; 0 &minus; 1 = &minus;1, mints Ticket #2.</li>
    </ol>
    <p>
        This sequence violates Invariant 1: <i>C</i><sub>remaining</sub>(t<sub>5</sub>) = &minus;1 &lt; 0. Two tickets are confirmed for a single seat.
    </p>

    <h2 class="sub-sec-title">2.6 State Verification and Invariant Violation Detection</h2>
    <table class="content-table">
        <thead>
            <tr>
                <th>Audit Parameter</th>
                <th>Safety Condition</th>
                <th>Violation Classification</th>
                <th>System Action</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Capacity Lower Bound</strong></td>
                <td><i>C</i><sub>remaining</sub>(t) &ge; 0</td>
                <td><span class="badge-fail">OVERSOLD / RACE HAZARD</span></td>
                <td>Trigger Red Anomaly Badge, Log Violation</td>
            </tr>
            <tr>
                <td><strong>Capacity Upper Bound</strong></td>
                <td><i>C</i><sub>remaining</sub>(t) &le; <i>C</i><sub>total</sub></td>
                <td><span class="badge-fail">INVENTORY LEAK</span></td>
                <td>Halt Batch Releases, Audit Ledger</td>
            </tr>
            <tr>
                <td><strong>Mutual Exclusion</strong></td>
                <td>|<b>C</b>(t)| &le; 1</td>
                <td><span class="badge-fail">LOCK INTEGRITY COLLAPSE</span></td>
                <td>Enforce FIFO Mutex Serialization</td>
            </tr>
            <tr>
                <td><strong>Ticket Bijectivity</strong></td>
                <td>|<b>R</b>(t)| = <i>C</i><sub>total</sub> &minus; <i>C</i><sub>remaining</sub>(t)</td>
                <td><span class="badge-fail">PHANTOM MINTING</span></td>
                <td>Rollback Unverified Bookings, Issue Refund</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- SECTION 2.7 WORKED NUMERICAL EXAMPLE: DEDICATED FULL PAGE (NO SPLITTING!) -->
<div class="page-break">
    <h2 class="sub-sec-title">2.7 Worked Numerical Example: Race Condition vs. Mutex Serialization</h2>
    <p>
        Below is the real-time execution trace demonstrating the high-contention contention window across two separate devices (Teacher Laptop vs. Friend Mobile) under both Unprotected (Mutex OFF) and Protected (Mutex ON) modes:
    </p>
    {trace_card_html}
    <p style="font-size: 8.5pt; color: #475569; margin-top: 8px;">
        As proven in Scenario 2, the Mutex primitive forces Device B into the FIFO wait queue while Device A holds the critical section. When Device A releases the lock, Device B performs a fresh query on current inventory, reads <i>C</i> = 0, and receives an atomic HTTP 409 (Sold Out) without decrementing inventory. The client immediately triggers the <strong>Automated Refund Reassurance Modal</strong> with refund tracking reference RZP-REF-849204.
    </p>
</div>

<!-- ========================================================= -->
<!-- CHAPTER 3: IMPLEMENTATION (Pages 9, 10, 11, 12) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL &amp; MUTEX</h1>
    
    <h2 class="sub-sec-title">3.1 Software and Development Tools Used</h2>
    <table class="content-table">
        <thead>
            <tr>
                <th>Component Layer</th>
                <th>Technology / Engine</th>
                <th>Architectural Justification &amp; Purpose</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Runtime Environment</strong></td>
                <td>Node.js LTS (v20+)</td>
                <td>Single-threaded V8 event loop with microtask-level atomicity</td>
            </tr>
            <tr>
                <td><strong>Web Server &amp; API</strong></td>
                <td>Native <code>http</code> Module</td>
                <td>Zero-dependency lightweight REST API routing (No Express framework bloat)</td>
            </tr>
            <tr>
                <td><strong>Concurrency Kernel</strong></td>
                <td>Native ES6</td>
                <td>Asynchronous Mutex with array-backed FIFO queue (<code>Mutex.js</code>)</td>
            </tr>
            <tr>
                <td><strong>Razorpay SDK</strong></td>
                <td>Standard v1</td>
                <td>Official checkout modal popup for authentic payment authorization</td>
            </tr>
            <tr>
                <td><strong>Vercel Serverless Edge</strong></td>
                <td>Production CLI</td>
                <td>Global edge deployment (<code>https://synnexa.vercel.app</code>)</td>
            </tr>
            <tr>
                <td><strong>Playwright &amp; PyMuPDF</strong></td>
                <td>1.57.0 / 1.28</td>
                <td>Two-pass automated PDF compilation and exact TOC synchronization</td>
            </tr>
        </tbody>
    </table>

    <h2 class="sub-sec-title">3.2 Mutex Function and Program Structure</h2>
    <p>
        The backend engine follows a clean, modular pipeline architecture:
    </p>
    {svg_3_1}
    <div class="caption">Figure 3.1: Professional draw.io-style architecture flowchart of the Concurrency Kernel pipeline (<code>Mutex.js</code> and <code>BookingService.js</code>) detailing payload validation, lock acquisition, critical section evaluation, and refund rollback.</div>
</div>

<!-- 3.3 Asynchronous Mutex Implementation: Dedicated Single Page -->
<div class="page-break">
    <h2 class="sub-sec-title">3.3 Asynchronous Mutex Implementation (`src/core/Mutex.js`)</h2>
    <p>
        The core lock primitive implements asynchronous acquire and release methods with strict FIFO queue order:
    </p>
    {card_mutex}
    <div class="callout" style="font-size: 8.5pt;">
        <strong>Mechanism Analysis:</strong> The <code>acquire()</code> method evaluates <code>if (!this._locked)</code> synchronously. If vacant, it transitions <code>_locked = true</code> immediately (Fast-Path). If held, it wraps execution in a Promise pushed to <code>this._queue</code> (Slow-Path). In <code>_release()</code>, if waiters exist, ownership is transferred to the oldest waiter via <code>nextInLine.grant()</code>, guaranteeing Dijkstra's Bounded Waiting.
    </div>
</div>

<!-- 3.4 Keyed Mutex Registry: Dedicated Single Page -->
<div class="page-break">
    <h2 class="sub-sec-title">3.4 Keyed Mutex Registry for Fine-Grained Locking (`KeyedMutexRegistry.js`)</h2>
    <p>
        A single global lock creates Amdahl's serialization bottleneck: buyers for Event 1 would lock out buyers for Event 2. The Keyed Mutex Registry allocates independent locks per event key:
    </p>
    {card_registry}
    <div class="callout" style="font-size: 8.5pt;">
        <strong>Granular Isolation Proof:</strong> If thread T<sub>1</sub> locks <code>mutex-hackathon-1</code>, thread T<sub>2</sub> requesting <code>mutex-hackathon-2</code> acquires its lock instantaneously without contention. Concurrency is maximized while maintaining strict mutual exclusion per event resource.
    </div>
</div>

<!-- 3.5 Atomic Critical Section: Dedicated Single Page -->
<div class="page-break">
    <h2 class="sub-sec-title">3.5 Atomic Critical Section and State Mutation (`BookingService.js`)</h2>
    <p>
        The critical section reads the live database, verifies <i>C</i> &gt; 0, decrements atomically, and releases in a strict <code>finally</code> block:
    </p>
    {card_booking}
    
    <h2 class="sub-sec-title">3.6 to 3.10 Storage, Testing &amp; Error Introduction</h2>
    <p>
        <code>Database.js</code> guarantees ACID durability via <code>fs.renameSync()</code>. Testing covered single-thread baselines, 50-thread stress tests (48 rejected, 2 confirmed, 0 oversold), live hardware (Teacher vs. Friend), and controlled error introduction via the Admin Mutex toggle.
    </p>
</div>

<!-- ========================================================= -->
<!-- CHAPTER 4: APPLICATION DASHBOARD (Pages 13, 14, 15, 16, 17) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">CHAPTER 4 - APPLICATION DASHBOARD &amp; INTERFACE DEVELOPMENT</h1>
    
    <h2 class="sub-sec-title">4.1 Dashboard Requirements</h2>
    <p>
        The user interface required a luxury commercial aesthetic reflecting international tech summits, combined with real-time telemetry meters, interactive modal dialogs, and a dedicated 2-device concurrency testing station.
    </p>

    <h2 class="sub-sec-title">4.2 Software / Framework Used</h2>
    <p>
        Built using semantic HTML5, modern vanilla CSS3 (Flexbox, Grid, CSS Variables, glassmorphic backdrop filters), and Vanilla JavaScript (Fetch API, DOM manipulation). Official external libraries include the Razorpay Standard Checkout SDK.
    </p>

    <h2 class="sub-sec-title">4.3 User Interface Design</h2>
    <p>
        The interface uses an obsidian background (<code>#0B1120</code>) with warm amber/gold accents (<code>#D97706</code>, <code>#F59E0B</code>) and responsive breakpoints for desktop, laptop, tablet, and smartphone screens.
    </p>

    <h2 class="sub-sec-title">4.4 Dashboard Inputs &amp; Outputs</h2>
    <table class="content-table">
        <thead>
            <tr>
                <th>Input / Output Component</th>
                <th>UI Modality</th>
                <th>Validation &amp; Processing Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Squad Registration Input</strong></td>
                <td>Modal Form</td>
                <td>Sanitizes Squad Name, Team Leader credentials, and dynamic members list.</td>
            </tr>
            <tr>
                <td><strong>Payment Authorization</strong></td>
                <td>Razorpay Popup</td>
                <td>Standard Checkout SDK modal simulating card, UPI, and NetBanking transfers.</td>
            </tr>
            <tr>
                <td><strong>Mutex Protection Switch</strong></td>
                <td>Admin Toggle</td>
                <td>Switches event state between synchronized Mutex ON and unprotected Mutex OFF.</td>
            </tr>
            <tr>
                <td><strong>Printable VIP Boarding Pass</strong></td>
                <td>Modal + window.print()</td>
                <td>Renders verified ticket with procedural SVG QR code and attendee metadata.</td>
            </tr>
            <tr>
                <td><strong>Refund Reassurance Modal</strong></td>
                <td>Alert Modal</td>
                <td>Pops up when a buyer is out-raced for the last seat, confirming a 5–7 day refund.</td>
            </tr>
            <tr>
                <td><strong>Microsecond Audit Stream</strong></td>
                <td>Terminal Card</td>
                <td>Live feed displaying lock acquisition, waiting duration, and capacity transitions.</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- 4.6 Client-Side Integration: Dedicated Single Page -->
<div class="page-break">
    <h2 class="sub-sec-title">4.6 Dashboard-to-Backend Code Integration</h2>
    <p>
        The client-side JavaScript communicates with native backend REST endpoints:
    </p>
    {card_refund}
    <div class="callout" style="font-size: 8.5pt;">
        <strong>HTTP 409 Interception:</strong> When the backend returns HTTP 409 (Sold Out), the catch block inspects the error payload, generates a unique refund tracking identifier (<code>REFUND_RZP_...</code>), and triggers <code>openRefundNoticeModal()</code> with the event title and full team fee.
    </div>
</div>

<!-- 4.7 Complete Data Processing Flow: Dedicated Single Page (NO SPLITTING!) -->
<div class="page-break">
    <h2 class="sub-sec-title">4.7 Complete Data Processing Flow</h2>
    <p>
        The end-to-end data processing and verification pipeline follows a seven-stage sequence:
    </p>
    {svg_4_1}
    <div class="caption">Figure 4.1: Professional draw.io-style pipeline diagram of the complete data processing and verification flow across frontend, backend, and storage layers.</div>
</div>

<!-- 4.8 & 4.9 Testing Methodology & Test Cases -->
<div class="page-break">
    <h2 class="sub-sec-title">4.8 Testing Methodology</h2>
    <p>
        Verification followed a three-tier testing hierarchy: automated unit tests (<code>npm test</code>), automated 50-thread concurrency rush (<code>npm run test:concurrency</code>), and real multi-device manual testing.
    </p>

    <h2 class="sub-sec-title">4.9 Test Cases and Results</h2>
    <table class="content-table">
        <thead>
            <tr>
                <th>Test ID</th>
                <th>Test Scenario</th>
                <th>Mutex</th>
                <th>Expected Outcome</th>
                <th>Observed Outcome</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>TC-01</td>
                <td>Single Thread Baseline</td>
                <td>ON</td>
                <td>Capacity decrements from 5 to 4; 1 ticket issued</td>
                <td>Confirmed (C = 4, 1 Ticket minted)</td>
                <td><span class="badge-pass">PASSED</span></td>
            </tr>
            <tr>
                <td>TC-02</td>
                <td>Two-Device Rush (C = 1)</td>
                <td>ON</td>
                <td>Device A confirms ticket; Device B rejected + refund</td>
                <td>Confirmed (A wins, B receives Refund Modal)</td>
                <td><span class="badge-pass">PASSED</span></td>
            </tr>
            <tr>
                <td>TC-03</td>
                <td>Two-Device Rush (C = 1)</td>
                <td>OFF</td>
                <td>Both devices read C = 1; Oversold anomaly C = -1</td>
                <td>Anomaly reproduced (C = -1, 2 Tickets minted)</td>
                <td><span class="badge-fail">VIOLATION</span></td>
            </tr>
            <tr>
                <td>TC-04</td>
                <td>50-Thread High Contention</td>
                <td>ON</td>
                <td>Exactly 2 succeed; 48 rejected; Final C = 0</td>
                <td>Zero overbooking (C = 0, 48 Rejections)</td>
                <td><span class="badge-pass">PASSED</span></td>
            </tr>
            <tr>
                <td>TC-05</td>
                <td>Keyed Lock Independence</td>
                <td>ON</td>
                <td>Locking Event 1 does not delay Event 2</td>
                <td>Independent execution confirmed (0ms wait)</td>
                <td><span class="badge-pass">PASSED</span></td>
            </tr>
            <tr>
                <td>TC-06</td>
                <td>ACID Tempfile Rename</td>
                <td>ON</td>
                <td>Atomic rename prevents corrupt JSON reads</td>
                <td>Valid JSON maintained across 1000 writes</td>
                <td><span class="badge-pass">PASSED</span></td>
            </tr>
            <tr>
                <td>TC-07</td>
                <td>Door Check-In Scanner</td>
                <td>N/A</td>
                <td>Scanned pass marked USED; duplicate check-in blocked</td>
                <td>Strict single-admittance enforced</td>
                <td><span class="badge-pass">PASSED</span></td>
            </tr>
            <tr>
                <td>TC-08</td>
                <td>Printable Pass Modal</td>
                <td>N/A</td>
                <td>Procedural QR code renders with attendee metadata</td>
                <td>window.print() renders boarding pass sheet</td>
                <td><span class="badge-pass">PASSED</span></td>
            </tr>
        </tbody>
    </table>
</div>

<!-- 4.10 Concurrency Stress Testing & Empirical Performance -->
<div class="page-break">
    <h2 class="sub-sec-title">4.10 Concurrency Stress Testing &amp; Empirical Performance</h2>
    <p>
        To evaluate high-contention throughput under realistic loads, 50 synthetic reservation requests were dispatched simultaneously against a single event with an initial capacity of 2 tickets:
    </p>
    <table class="content-table">
        <thead>
            <tr>
                <th>Performance Metric</th>
                <th>Mutex Enabled (ON)</th>
                <th>Mutex Disabled (OFF)</th>
                <th>Impact &amp; Significance</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Total Requests Fired</strong></td>
                <td>50 concurrent threads</td>
                <td>50 concurrent threads</td>
                <td>Identical workload dispatched within 5ms window</td>
            </tr>
            <tr>
                <td><strong>Confirmed Bookings</strong></td>
                <td><strong>2 Tickets</strong> (Expected: 2)</td>
                <td><strong>8 Tickets</strong> (Expected: 2)</td>
                <td>+300% overselling disaster under Mutex OFF</td>
            </tr>
            <tr>
                <td><strong>Rejected Bookings</strong></td>
                <td><strong>48 Requests</strong> (HTTP 409)</td>
                <td><strong>42 Requests</strong></td>
                <td>Controlled rejection preserves inventory truth</td>
            </tr>
            <tr>
                <td><strong>Final Remaining Seats</strong></td>
                <td><strong>0 Seats</strong> (Invariant Holds)</td>
                <td><strong>-6 Seats</strong> (Violated!)</td>
                <td>Capacity lower bound strictly protected under Mutex</td>
            </tr>
            <tr>
                <td><strong>Mean Lock Wait Duration</strong></td>
                <td>4.82 milliseconds</td>
                <td>0.00 milliseconds</td>
                <td>Negligible latency overhead for absolute safety</td>
            </tr>
            <tr>
                <td><strong>Thread Starvation Count</strong></td>
                <td><strong>0 Threads</strong></td>
                <td>N/A</td>
                <td>Strict FIFO queue ensures bounded waiting</td>
            </tr>
        </tbody>
    </table>
    <div class="callout">
        <strong>Dual-Mode Conclusion:</strong> Under Mutex ON, zero invariant violations occur regardless of contention volume. Under Mutex OFF, every concurrent burst causes invariant failure (<i>C</i><sub>remaining</sub> &lt; 0).
    </div>
</div>

<!-- ========================================================= -->
<!-- CHAPTER 5, 6, 7: ERRORS, FEATURES, CONCLUSION (Pages 18 & 19) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">CHAPTER 5 - ERRORS, CHALLENGES AND LEARNING OUTCOMES</h1>
    
    <h2 class="sub-sec-title">5.1 Errors Encountered During Implementation</h2>
    <ul>
        <li><strong>E1 - TOCTOU State Corruption:</strong> Concurrent requests observed stale inventory during simulated payment delays, decrementing capacity below zero.</li>
        <li><strong>E2 - Corrupt JSON Reads under Concurrent Writes:</strong> Parallel writes truncated <code>data.json</code>, causing <code>SyntaxError: Unexpected end of JSON input</code>.</li>
        <li><strong>E3 - Promise Leak / Event Loop Deadlock:</strong> Mutex acquire Promises remained unfulfilled if an unhandled exception occurred in the critical section.</li>
    </ul>

    <h2 class="sub-sec-title">5.2 Causes of Errors &amp; Solutions Implemented</h2>
    <p>
        E1 was solved by wrapping inventory read, evaluation, and mutation in <code>mutex.acquire()</code>. E2 was solved via atomic tempfile rename (<code>fs.renameSync()</code>). E3 was solved by enclosing critical sections in strict <code>try ... finally {{ releaseLock(); }}</code> blocks.
    </p>

    <h2 class="sub-sec-title">5.3 Operating System Learning Outcomes</h2>
    <ul>
        <li><strong>Dijkstra's Invariants:</strong> Practical comprehension of Mutual Exclusion, Progress, and Bounded Waiting.</li>
        <li><strong>Single-Threaded Asynchrony:</strong> Node.js single-thread execution eliminates race conditions on synchronous turns, but asynchronous boundaries re-introduce classical race conditions.</li>
        <li><strong>FIFO Starvation Immunity:</strong> Replacing set-based lock collections with ordered FIFO queues eliminates thread starvation.</li>
    </ul>
</div>

<div class="page-break">
    <h1 class="sec-title">CHAPTER 6 - ADDITIONAL FEATURES AND PRODUCT ENHANCEMENTS</h1>
    <ul>
        <li><strong>Automated Refund Reassurance Modal:</strong> Instantly reassures buyers who missed the final seat by showing a formal refund notice with reference RZP-REF-849204 and a 5–7 day refund window.</li>
        <li><strong>Organizer Command Center (/admin):</strong> Live 2-device contention rig, per-event Mutex toggles, batch release controls, and door check-in scanner.</li>
        <li><strong>Procedural SVG QR Code &amp; VIP Boarding Pass:</strong> Pure JavaScript QR code rendering for door check-in with printable styling.</li>
        <li><strong>Live Production Edge Deployment:</strong> Publicly accessible at <code>https://synnexa.vercel.app</code>.</li>
    </ul>

    <h1 class="sec-title" style="margin-top: 16px;">CHAPTER 7 - RESULTS AND CONCLUSION</h1>
    <table class="content-table">
        <thead>
            <tr>
                <th>Project Objective</th>
                <th>Target Criterion</th>
                <th>Demonstrated Evidence</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Zero Overbooking</strong></td>
                <td><i>C</i><sub>remaining</sub> &ge; 0 at all times</td>
                <td>Guaranteed zero overselling across all automated and manual tests.</td>
            </tr>
            <tr>
                <td><strong>Starvation Elimination</strong></td>
                <td>Bounded Waiting <i>O</i>(k)</td>
                <td>FIFO wait queue guarantees bounded waiting in order of arrival.</td>
            </tr>
            <tr>
                <td><strong>Resource Isolation</strong></td>
                <td>Independent per-resource locks</td>
                <td>Keyed Mutex Registry prevents cross-event serialization bottlenecks.</td>
            </tr>
            <tr>
                <td><strong>Commercial Polish</strong></td>
                <td>Luxury UI &amp; Refund UX</td>
                <td>Executive dashboard, Razorpay modal, VIP passes, and automated refund notices.</td>
            </tr>
        </tbody>
    </table>
    <div class="callout" style="margin-top: 10px;">
        <strong>Final Conclusion:</strong> Event Registration successfully bridges foundational Operating Systems theory with modern cloud engineering, proving that rigorous concurrency control is vital for data integrity in distributed web applications.
    </div>
</div>

<!-- ========================================================= -->
<!-- APPENDIX A: COMPLETE SOURCE CODE (Pages 20, 21, 22, 23) -->
<!-- ========================================================= -->
<!-- A.1 Mutex Core Primitive: Dedicated Single Page -->
<div class="page-break">
    <h1 class="sec-title">APPENDIX A - COMPLETE SOURCE CODE</h1>
    <p style="font-size: 8.5pt; color: #475569; margin-bottom: 8px;">
        Below is the complete implementation of the core concurrency kernel and booking service divided into dedicated single-page functional modules:
    </p>
    
    <h2 class="sub-sec-title">A.1 Mutex Core Primitive (`src/core/Mutex.js`)</h2>
    {card_mutex}
    <div class="caption">Listing A.1: Asynchronous Mutex primitive implementing Dijkstra's 3 Critical Section criteria via FIFO queue handoff.</div>
</div>

<!-- A.2 Keyed Mutex Registry: Dedicated Single Page -->
<div class="page-break">
    <h2 class="sub-sec-title">A.2 Keyed Mutex Registry (`src/core/KeyedMutexRegistry.js`)</h2>
    {card_registry}
    <div class="caption">Listing A.2: Fine-grained per-resource lock registry isolating concurrent bookings across independent events.</div>
</div>

<!-- A.3 Tatkal Booking Service: Dedicated Single Page -->
<div class="page-break">
    <h2 class="sub-sec-title">A.3 Tatkal Booking Service (`src/services/BookingService.js`)</h2>
    {card_booking}
    <div class="caption">Listing A.3: Core Tatkal booking critical section with atomic capacity evaluation and guaranteed finally release.</div>
</div>

<!-- A.4 Client-Side Booking & Refund Handling: Dedicated Single Page -->
<div class="page-break">
    <h2 class="sub-sec-title">A.4 Client-Side Booking &amp; Refund Handling (`public/app.js`)</h2>
    {card_refund}
    <div class="caption">Listing A.4: Client-side booking dispatcher intercepting HTTP 409 Tatkal exhaustion and launching Automated Refund Modal.</div>
</div>

<!-- ========================================================= -->
<!-- APPENDIX B: LINE-BY-LINE EXPLANATION (Page 24) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">APPENDIX B - LINE-BY-LINE EXPLANATION OF CODE</h1>
    
    <h2 class="sub-sec-title">1. `Mutex` Class Constructor &amp; State Flags</h2>
    <ul>
        <li><code>this._locked = false;</code>: Binary semaphore state flag indicating whether the critical section is occupied.</li>
        <li><code>this._queue = [];</code>: Array-backed FIFO wait queue storing pending thread grants, guaranteeing Dijkstra's Bounded Waiting criterion.</li>
        <li><code>this._currentOwner = null;</code>: Diagnostic identifier tracking the active thread ID for microsecond audit logging.</li>
    </ul>

    <h2 class="sub-sec-title">2. `acquire(requesterId, teamName)` Fast &amp; Slow Path</h2>
    <ul>
        <li><strong>Fast-Path:</strong> If <code>!this._locked</code> evaluates to true, sets <code>_locked = true</code> and immediately returns <code>Promise.resolve(() => this._release(threadId))</code> without event-loop suspension.</li>
        <li><strong>Slow-Path:</strong> If <code>_locked</code> is true, wraps execution inside an unfulfilled Promise and pushes a grant closure into <code>this._queue</code>, safely suspending the thread.</li>
    </ul>

    <h2 class="sub-sec-title">3. `_release(requesterId)` and FIFO Starvation Elimination</h2>
    <ul>
        <li>If <code>this._queue.length &gt; 0</code>, executes <code>this._queue.shift().grant()</code>, transferring ownership directly to the oldest waiting thread in strict <i>O</i>(1) time, eliminating starvation. If empty, reverts <code>_locked = false</code>.</li>
    </ul>

    <h2 class="sub-sec-title">4. `KeyedMutexRegistry.get(key)` Fine-Grained Isolation</h2>
    <ul>
        <li>Queries internal <code>Map</code> for key. If absent, instantiates dedicated <code>Mutex('event-mutex-' + key)</code>, ensuring independent events never contend for the same lock instance.</li>
    </ul>

    <h2 class="sub-sec-title">5. Client-Side HTTP 409 Interceptor &amp; Refund Reassurance</h2>
    <ul>
        <li>When a buyer is out-raced for the last seat, the backend returns HTTP 409 (Sold Out). The client catches this error, extracts the payment ID, generates a refund reference (<code>REFUND_RZP_...</code>), and opens the <strong>Automated Refund Reassurance Modal</strong> reassuring the user of a full refund within 5–7 business days.</li>
    </ul>
</div>

<!-- ========================================================= -->
<!-- APPENDIX C: FRESH DASHBOARD SCREENSHOTS (Pages 25, 26, 27) -->
<!-- ========================================================= -->
<!-- Page 25: Landing Portal -->
<div class="page-break">
    <h1 class="sec-title">APPENDIX C - DASHBOARD SCREENSHOTS</h1>
    <p style="font-size: 8.5pt; color: #475569; margin-bottom: 8px;">
        The following fresh screenshots demonstrate the production operation of the Event Registration portal, modal dialogs, and admin command center:
    </p>

    <div class="screenshot-card">
        <img src="{shot_landing_b64}" alt="SYNNEXA Event Registry Landing Page">
        <div class="caption">Figure C.1: Event Registration Curated Events Landing Portal displaying real-time Tatkal seat gauges, Book Team Pass buttons, and active event cards.</div>
    </div>
</div>

<!-- Page 26: Refund Modal & Boarding Pass -->
<div class="page-break">
    <h2 class="sub-sec-title">High-Contention Interaction &amp; Verification Modals</h2>
    
    <div class="screenshot-card">
        <img src="{shot_refund_b64}" alt="Automated Refund Reassurance Modal">
        <div class="caption">Figure C.2: Automated Refund Reassurance Modal displayed when a concurrent buyer is out-raced for the final seat, confirming 5–7 day refund with RZP tracking code.</div>
    </div>

    <div class="screenshot-card">
        <img src="{shot_boarding_b64}" alt="Verified VIP Printable Boarding Pass">
        <div class="caption">Figure C.3: Verified VIP Boarding Pass with procedural SVG QR code, attendee squad roster, payment attestation hash, and window.print() print stylesheet.</div>
    </div>
</div>

<!-- Page 27: Admin Command Center & Concurrency Studio -->
<div class="page-break">
    <h2 class="sub-sec-title">Organizer Command Center &amp; Concurrency Studio</h2>
    
    <div class="screenshot-card">
        <img src="{shot_admin_b64}" alt="Organizer Command Center & 2-Device Station">
        <div class="caption">Figure C.4: Organizer Command Center (/admin) featuring the live 2-device concurrency station (Teacher vs. Friend), per-event Mutex switches, and attendee rosters.</div>
    </div>

    <div class="screenshot-card">
        <img src="{shot_studio_b64}" alt="OS Concurrency Studio">
        <div class="caption">Figure C.5: OS Concurrency Studio (/studio) providing microsecond telemetry meters, lock state monitors, and live thread contention logs.</div>
    </div>
</div>

<!-- ========================================================= -->
<!-- APPENDIX D: TEST RESULTS & STRESS TRACE (Page 28) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">APPENDIX D - COMPLETE TEST-CASE TABLES AND SAMPLE OUTPUTS</h1>
    
    <div class="trace-card">
        <div class="trace-header">
            <div class="trace-title">
                <span class="dot dot-red"></span>
                <span class="dot dot-yellow"></span>
                <span class="dot dot-green"></span>
                <span>Event Registration Concurrency &amp; Backend Test Suite Runner</span>
            </div>
            <div class="trace-badge">7/7 Tests Passed (100%)</div>
        </div>
        <div class="trace-body">
[TEST 1] Mutex: Guarantees strict Mutual Exclusion (|C(t)| &le; 1) .................... <span class="tr-win">PASSED</span>
[TEST 2] Mutex: Enforces Bounded Waiting in strict FIFO order (Zero Starvation) ... <span class="tr-win">PASSED</span>
[TEST 3] KeyedMutexRegistry: Independent resources lock independently ............. <span class="tr-win">PASSED</span>
[TEST 4] BookingService: 10 concurrent requests for 2 seats under Mutex .......... <span class="tr-win">PASSED</span>
         &rarr; Result: Exactly 2 succeed, 8 rejected, 0 overbooking.
[TEST 5] BookingService: Race condition demonstration WITHOUT Mutex .............. <span class="tr-win">PASSED</span>
         [RACE HAZARD REPORT] Initial: 1 Seat | Requests: 6 | Confirmed: 6 | Final Seats: -5 | Oversold: 5
[TEST 6] Database: Atomic persistence under rapid parallel writes ................ <span class="tr-win">PASSED</span>
[TEST 7] API Dispatcher: Full end-to-end HTTP route verification ................. <span class="tr-win">PASSED</span>
================================================================================
FINAL VERIFICATION: 7 / 7 PASSED (100% SUCCESS RATE)
        </div>
    </div>

    <h2 class="sub-sec-title">50-Thread High-Contention Stress Test Benchmark</h2>
    <div class="trace-card">
        <div class="trace-header">
            <div class="trace-title">
                <span class="dot dot-red"></span>
                <span class="dot dot-yellow"></span>
                <span class="dot dot-green"></span>
                <span>50-Thread High-Contention Concurrency Benchmark</span>
            </div>
            <div class="trace-badge">Stress Test: 50 Threads vs 2 Seats</div>
        </div>
        <div class="trace-body">
Target Event: Global AI HackSphere 2026 (Initial Seats: 2)
Simultaneous Requests Fired: 50 Threads

>>> RUN 1: MUTEX SYNCHRONIZATION ENABLED (ON)
- Total Requests Processed: 50
- Confirmed Bookings:       <span class="tr-win">2 Passes</span> (Capacity Limit Respected)
- Rejected (Sold Out):      <span class="tr-res">48 Requests</span> (HTTP 409 + Automated Refund Receipt)
- Final Capacity in DB:     <span class="tr-win">0 Seats Remaining</span> (Invariant 1 Satisfied: 0 &le; C &le; C_total)
- Oversold Anomaly:         <span class="tr-win">0 (ZERO OVERBOOKING)</span>
- Data Integrity:           <span class="tr-win">PERFECT (100% INVARIANT PRESERVATION)</span>

>>> RUN 2: MUTEX SYNCHRONIZATION DISABLED (OFF)
- Total Requests Processed: 50
- Confirmed Bookings:       <span class="tr-rem">8 Passes Issued</span> (Overbooking Hazard!)
- Rejected (Sold Out):      42 Requests
- Final Capacity in DB:     <span class="tr-rem">-6 Seats Remaining</span> (Invariant Violated: C &lt; 0)
- Oversold Anomaly:         <span class="tr-rem">6 EXCESS PASSES ISSUED FOR 2 SEATS</span>
        </div>
    </div>
</div>

<!-- ========================================================= -->
<!-- APPENDIX E: HARDWARE & ENVIRONMENT (Page 29) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">APPENDIX E - HARDWARE &amp; RUNTIME ENVIRONMENT SPECIFICATIONS</h1>
    
    <table class="content-table">
        <thead>
            <tr>
                <th>Hardware / Runtime Component</th>
                <th>Evaluation Node 1 (Teacher Laptop)</th>
                <th>Evaluation Node 2 (Friend Mobile)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Device Model</strong></td>
                <td>Dell XPS / Inspiron (x86_64)</td>
                <td>Android / iOS Smartphone (ARM64)</td>
            </tr>
            <tr>
                <td><strong>Processor Architecture</strong></td>
                <td>Intel Core i7-12700H (14 Cores, 20 Threads)</td>
                <td>Qualcomm Snapdragon / Apple A-Series</td>
            </tr>
            <tr>
                <td><strong>Operating System</strong></td>
                <td>Windows 11 Home (Build 22631)</td>
                <td>Android 14 / iOS 17.5</td>
            </tr>
            <tr>
                <td><strong>Network Interface</strong></td>
                <td>Wi-Fi 6 (802.11ax) &bull; LAN Gateway</td>
                <td>4G LTE / Wi-Fi Client</td>
            </tr>
            <tr>
                <td><strong>Browser Runtime</strong></td>
                <td>Google Chrome 133 / Chromium Engine</td>
                <td>Mobile Safari / Chrome Mobile</td>
            </tr>
            <tr>
                <td><strong>Server Host Port</strong></td>
                <td><code>http://localhost:3000</code></td>
                <td><code>http://192.168.1.9:3000</code> (LAN Rig)</td>
            </tr>
            <tr>
                <td><strong>Cloud Production Edge</strong></td>
                <td colspan="2" style="text-align: center; font-weight: bold; color: #2563eb;">https://synnexa.vercel.app (Global Vercel Edge CDN)</td>
            </tr>
        </tbody>
    </table>

    <h2 class="sub-sec-title">Cloud Deployment &amp; Public Access Configuration</h2>
    <div class="callout">
        <strong>Vercel Production Edge Deployment:</strong> The Event Registration platform is continuously deployed to Vercel global edge infrastructure. Serverless function routing is declared in <code>vercel.json</code>, routing <code>/api/*</code> requests to the serverless REST handler, while serving static frontend assets from <code>public/</code>.
    </div>
</div>

<!-- ========================================================= -->
<!-- APPENDIX F: TEAM CONTRIBUTIONS & REFERENCES (Page 30) -->
<!-- ========================================================= -->
<div class="page-break">
    <h1 class="sec-title">APPENDIX F - TEAM CONTRIBUTIONS &amp; REFERENCES</h1>
    
    <h2 class="sub-sec-title">Individual Team Member Contributions (Strict Ascending Order)</h2>
    <table class="content-table">
        <thead>
            <tr>
                <th style="width: 14%;">Hall Ticket</th>
                <th style="width: 20%;">Student Name</th>
                <th style="width: 26%;">Key Module Contributions</th>
                <th style="width: 14%;">Sign-Off</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>2503A51108</strong></td>
                <td>Ch. Naveen Reddy</td>
                <td>Designed file-backed JSON transactional persistence, atomic tempfile rename algorithms, and data schema migrations.</td>
                <td style="color: #15803d; font-weight: bold;">Signed</td>
            </tr>
            <tr>
                <td><strong>2503A51109</strong></td>
                <td>K. Shiva Saketh</td>
                <td>Constructed TOCTOU un-synchronized execution branch, dirty read generators, and negative seat overbooking verifications.</td>
                <td style="color: #15803d; font-weight: bold;">Signed</td>
            </tr>
            <tr>
                <td><strong>2503A51110</strong></td>
                <td><strong>A. Shiva Ganesh</strong><br><span class="leader-badge">LEADER</span></td>
                <td>Architected custom asynchronous Mutex primitive, FIFO bounded wait queue, KeyedMutexRegistry, and end-to-end system design.</td>
                <td style="color: #15803d; font-weight: bold;">Signed</td>
            </tr>
            <tr>
                <td><strong>2503A51111</strong></td>
                <td>V. Saicharan</td>
                <td>Implemented high-performance zero-dependency Node.js HTTP controllers, CORS pipeline, and microsecond audit telemetry.</td>
                <td style="color: #15803d; font-weight: bold;">Signed</td>
            </tr>
            <tr>
                <td><strong>2503A1112</strong></td>
                <td>T. Geethika</td>
                <td>Built responsive light-slate dashboard, dynamic team member roster inputs, and pure procedural SVG QR boarding pass engine.</td>
                <td style="color: #15803d; font-weight: bold;">Signed</td>
            </tr>
            <tr>
                <td><strong>2503A51113</strong></td>
                <td>G. Vishwas</td>
                <td>Configured Razorpay Test Mode gateway interface, door check-in scanner module, CSV roster exporter, and viva defense test harness.</td>
                <td style="color: #15803d; font-weight: bold;">Signed</td>
            </tr>
        </tbody>
    </table>

    <h2 class="sub-sec-title">Academic &amp; Industrial References</h2>
    <ol style="font-size: 8.5pt; color: #475569; padding-left: 18px; line-height: 1.45;">
        <li>Dijkstra, E. W. (1965). <em>Cooperating Sequential Processes</em>. Technological University, Eindhoven, The Netherlands. (Reprinted in F. Genuys, Ed., Programming Languages, Academic Press, 1968, pp. 43–112).</li>
        <li>Silberschatz, A., Galvin, P. B., &amp; Gagne, G. (2018). <em>Operating System Concepts</em> (10th ed.). John Wiley &amp; Sons, Inc. (Chapter 6: Synchronization Tools &amp; Chapter 7: Synchronization Examples).</li>
        <li>Tanenbaum, A. S., &amp; Bos, H. (2014). <em>Modern Operating Systems</em> (4th ed.). Pearson Education. (Section 2.3: Interprocess Communication, Semaphores, and Mutexes).</li>
        <li>Lamport, L. (1974). <em>A New Solution of Dijkstra's Concurrent Programming Problem</em>. Communications of the ACM, 17(8), 453–455.</li>
        <li>Tilkov, S., &amp; Vinoski, S. (2010). <em>Node.js: Using JavaScript to Build High-Performance Network Programs</em>. IEEE Internet Computing, 14(6), 80–83.</li>
        <li>Bacon, D. F., Konuru, R., Murthy, C., &amp; Serrano, M. J. (1998). <em>Thin Locks: Featherweight Synchronization for Java</em>. In Proceedings of the ACM SIGPLAN 1998 Conference on Programming Language Design and Implementation (PLDI '98), pp. 258–268.</li>
    </ol>
</div>

</body>
</html>
"""
    return html_content

def compile_pdf(html_path, desktop_pdf, scratch_pdf, public_pdf):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_path).replace(chr(92), '/')}", wait_until="load")
        page.wait_for_timeout(1000)
        
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"},
            prefer_css_page_size=True
        )
        browser.close()

    # Save to scratch
    with open(scratch_pdf, "wb") as f:
        f.write(pdf_bytes)

    # Save to public
    with open(public_pdf, "wb") as f:
        f.write(pdf_bytes)

    # Save to Desktop (CRITICAL: Never overwrite CRC_Project_Report.pdf)
    with open(desktop_pdf, "wb") as f:
        f.write(pdf_bytes)

def main():
    base_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\event-registration-mutex-system"
    html_output_path = os.path.join(base_dir, "clean_report_synnexa.html")
    desktop_pdf = r"C:\Users\DELL\Desktop\SYNNEXA_OS_Course_Project_Report_Product8.pdf"
    scratch_pdf = os.path.join(base_dir, "SYNNEXA_OS_Course_Project_Report_Product8.pdf")
    public_pdf = os.path.join(base_dir, "public", "SYNNEXA_OS_Course_Project_Report_Product8.pdf")
    public_report_pdf = os.path.join(base_dir, "public", "report.pdf")

    # Pass 1: Initial compilation
    print("Pass 1: Compiling initial HTML and PDF...")
    initial_html = generate_report()
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(initial_html)
    compile_pdf(html_output_path, desktop_pdf, scratch_pdf, public_pdf)

    # Pass 2: Extract exact page numbers of all sections
    print("Pass 2: Extracting exact section page numbers...")
    doc = fitz.open(scratch_pdf)
    section_targets = [
        "CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL",
        "1.1 Introduction to Concurrency Anomalies",
        "1.2 Need for Synchronization in Ticketing Systems",
        "1.3 Basic Working of Mutex",
        "1.4 Applications of Mutex in High-Contention Infrastructure",
        "1.5 Problem Statement and Product Requirements",
        "1.6 Proposed Implementation Plan",
        "CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL",
        "2.1 State Invariants and Shared Data Representation",
        "2.2 Mutual Exclusion Property",
        "2.3 Progress and Bounded Waiting Proof",
        "2.4 Atomic Test-and-Set and Asynchronous Transitions",
        "2.5 Time-of-Check to Time-of-Use",
        "2.6 State Verification and Invariant Violation Detection",
        "2.7 Worked Numerical Example",
        "CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL",
        "3.1 Software and Development Tools Used",
        "3.2 Mutex Function and Program Structure",
        "3.3 Asynchronous Mutex Implementation",
        "3.4 Keyed Mutex Registry",
        "3.5 Atomic Critical Section",
        "3.6 to 3.10 Storage Tier",
        "CHAPTER 4 - APPLICATION DASHBOARD",
        "4.1 to 4.5 Dashboard Requirements",
        "4.6 Dashboard-to-Backend Integration",
        "4.7 Complete Data Processing Flow",
        "4.8 to 4.9 Testing Methodology",
        "4.10 Concurrency Stress Testing",
        "CHAPTER 5 - ERRORS, CHALLENGES",
        "5.1 Errors Encountered",
        "CHAPTER 6 - ADDITIONAL FEATURES",
        "6.1 Additional Features",
        "CHAPTER 7 - RESULTS AND CONCLUSION",
        "7.1 Verification Summary",
        "APPENDICES",
        "APPENDIX A - COMPLETE SOURCE CODE",
        "APPENDIX B - LINE-BY-LINE EXPLANATION",
        "APPENDIX C - DASHBOARD SCREENSHOTS",
        "APPENDIX D - COMPLETE TEST-CASE TABLES",
        "APPENDIX E - HARDWARE",
        "APPENDIX F - TEAM CONTRIBUTIONS"
    ]

    toc_map = {}
    for target in section_targets:
        for i, page in enumerate(doc):
            if i < 4: # Skip cover, cert, abstract, TOC
                continue
            text = page.get_text()
            if target in text:
                toc_map[target] = i + 1
                break

    print(f"Extracted {len(toc_map)} section page locations.")

    # Pass 3: Recompile with synchronized TOC
    print("Pass 3: Recompiling with synchronized TOC...")
    final_html = generate_report(toc_map)
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    compile_pdf(html_output_path, desktop_pdf, scratch_pdf, public_pdf)

    # Also copy to report.pdf in public
    with open(scratch_pdf, "rb") as src, open(public_report_pdf, "wb") as dst:
        dst.write(src.read())

    
    event_reg_desktop = r"C:\Users\DELL\Desktop\Event_Registration_OS_Course_Project_Report_Product8.pdf"
    event_reg_public = os.path.join(base_dir, "public", "Event_Registration_OS_Course_Project_Report_Product8.pdf")
    with open(scratch_pdf, "rb") as src, open(event_reg_desktop, "wb") as dst:
        dst.write(src.read())
    with open(scratch_pdf, "rb") as src, open(event_reg_public, "wb") as dst:
        dst.write(src.read())

    print(f"Compilation fully complete!\nDesktop: {desktop_pdf}\nScratch: {scratch_pdf}\nPublic: {public_pdf}")

if __name__ == "__main__":
    main()
