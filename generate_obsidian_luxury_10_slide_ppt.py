# -*- coding: utf-8 -*-
"""
generate_obsidian_luxury_10_slide_ppt.py
Generates the official 10-slide OBSIDIAN DARK LUXURY presentation deck for Event Registration (Product #8).
- Exact match to website dark luxury theme:
  * Midnight Obsidian Canvas (#0B1120)
  * Elevated Charcoal/Navy Cards (#111827 / #1E293B)
  * Subtle Electric Slate Borders (#334155)
  * Warm Amber/Gold Glowing Accents (#F59E0B / #D97706)
  * Tech Cyan (#38BDF8) & Emerald Green (#10B981) Accents
  * Crisp Diamond White Headings (#FFFFFF) & Muted Platinum Body (#94A3B8 / #CBD5E1)
- Clean breathing room, high visual impact, ZERO text walls (not overwhelming!)
- Each slide explains ONE meaningful, high-value systems concept
- ZERO code in any slide
- 16:9 widescreen layout
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Obsidian Dark Luxury Color System ---
    BG_OBSIDIAN = RGBColor(11, 17, 32)       # #0B1120 Midnight Obsidian
    SURFACE_CARD = RGBColor(17, 24, 39)      # #111827 Elevated Card
    SURFACE_ELEVATED = RGBColor(30, 41, 59)  # #1E293B Highlight Card
    BORDER_SUBTLE = RGBColor(51, 65, 85)     # #334155 Slate Border

    TEXT_TITLE = RGBColor(255, 255, 255)     # #FFFFFF Diamond White
    TEXT_BODY = RGBColor(203, 213, 225)      # #CBD5E1 Platinum Body
    TEXT_MUTED = RGBColor(148, 163, 184)     # #94A3B8 Slate Muted

    GOLD_ACCENT = RGBColor(245, 158, 11)     # #F59E0B Radiant Amber Gold
    GOLD_DEEP = RGBColor(217, 119, 6)        # #D97706 Deep Gold
    GOLD_BG = RGBColor(35, 26, 15)           # Soft Gold Glow Container

    CYAN_ACCENT = RGBColor(56, 189, 248)     # #38BDF8 Tech Cyan Glow
    CYAN_BG = RGBColor(12, 33, 54)           # Soft Cyan Container

    EMERALD_ACCENT = RGBColor(16, 185, 129)  # #10B981 Emerald Success
    EMERALD_BG = RGBColor(10, 40, 30)        # Soft Emerald Container

    RED_ACCENT = RGBColor(239, 68, 68)       # #EF4444 Hazard Red
    RED_BG = RGBColor(45, 18, 20)            # Soft Red Container

    def apply_base_canvas(slide):
        # 1. Base Midnight Obsidian Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_OBSIDIAN
        bg.line.fill.background()

        # 2. Glowing Top Gold & Cyan Accent Line
        bar_gold = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(8.0), Inches(0.06))
        bar_gold.fill.solid()
        bar_gold.fill.fore_color.rgb = GOLD_ACCENT
        bar_gold.line.fill.background()

        bar_cyan = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.0), 0, Inches(5.333), Inches(0.06))
        bar_cyan.fill.solid()
        bar_cyan.fill.fore_color.rgb = CYAN_ACCENT
        bar_cyan.line.fill.background()

        # 3. Slide Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.733), Inches(0.3))
        ftf = footer_box.text_frame
        ftf.word_wrap = True
        ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0
        p = ftf.paragraphs[0]
        p.text = "Event Registration • Product #8 Concurrency Mutex Platform • SR University CSE Core"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

    def add_slide_header(slide, tag, title, subtitle):
        apply_base_canvas(slide)
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.3))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = tag.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = GOLD_ACCENT
        p0.font.name = "Segoe UI"
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_TITLE
        p1.font.name = "Segoe UI"

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(11)
            p2.font.color.rgb = TEXT_MUTED
            p2.font.name = "Segoe UI"
            p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (CINEMATIC OBSIDIAN BRAND COVER)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_base_canvas(s1)

    # Hero Center Container
    hero_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.95))
    hero_card.fill.solid()
    hero_card.fill.fore_color.rgb = SURFACE_CARD
    hero_card.line.color.rgb = BORDER_SUBTLE
    hero_card.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.15), Inches(10.9), Inches(5.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "SR UNIVERSITY • DEPARTMENT OF CSE CORE • OPERATING SYSTEMS LAB (CS201)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Event Registration: High-Throughput Concurrency & Mutex System"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = TEXT_TITLE
    p.font.name = "Segoe UI"
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Tatkal Quota Event Platform with Zero Overbooking, Distributed Locking & Automated Refund Reassurance"
    p.font.size = Pt(12)
    p.font.color.rgb = CYAN_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Team Leader: A. Shiva Ganesh (HTNO: 2503A51110)  •  B.Tech CSE Core (2nd Year)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Core Pillars: Mutual Exclusion (|C| ≤ 1) • Time-of-Check to Time-of-Use Elimination • Distributed Lock Manager"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.font.name = "Segoe UI"

    # 3 Stat Cards on Title Slide
    stats = [
        ("Strict Mutual Exclusion", "|C(t)| ≤ 1 at all times\nZero capacity overbooking", CYAN_ACCENT, CYAN_BG),
        ("FIFO Wait Queue", "Bounded Waiting O(k)\nComplete starvation immunity", GOLD_ACCENT, GOLD_BG),
        ("Distributed Lock Manager", "Multi-device synchronization\nCross-container serverless safety", EMERALD_ACCENT, EMERALD_BG)
    ]
    for idx, (stitle, sdesc, col, bg_col) in enumerate(stats):
        left = Inches(1.2 + idx * 3.7)
        top = Inches(4.45)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.5), Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = col
        card.line.width = Pt(1.2)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = Inches(0.18)

        p = ctf.paragraphs[0]
        p.text = stitle
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"
        p.space_after = Pt(4)

        p = ctf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2: THE PROBLEM (TOCTOU RACE HAZARD)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "The Core Problem", "The Flash-Sale Dilemma: Time-of-Check to Time-of-Use (TOCTOU)",
                     "Why un-synchronized high-demand booking systems crash and oversell during peak traffic")

    cards_s2 = [
        ("The Surge Demand Dilemma",
         "When Capacity Reaches 1",
         [
             "Flash-demand systems (IRCTC Tatkal, concert passes, tech summits) experience bursts of thousands of requests per second.",
             "The system reaches critical instability specifically when remaining inventory drops to the final 1 or 2 seats.",
             "Multiple concurrent buyer requests arrive within microsecond intervals, all competing for the exact same slot.",
             "Without synchronization barriers, inventory validation and state mutation decouple across asynchronous boundaries."
         ],
         CYAN_ACCENT, CYAN_BG),
        ("TOCTOU Race Hazard Anatomy",
         "Microsecond Race Sequence",
         [
             "1. t0: Laptop 1 reads C = 1 (Evaluates: 1 > 0 → VALID).",
             "2. t1: Laptop 1 awaits payment processing delay.",
             "3. t2: Laptop 2 arrives, reads C = 1 (STALE READ!).",
             "4. t3: Laptop 1 finishes, writes C ← 0, mints Ticket #1.",
             "5. t4: Laptop 2 finishes, writes C ← -1, mints Ticket #2!",
             "RESULT: Invariant Violated! C = -1 < 0 (Overbooked)."
         ],
         RED_ACCENT, RED_BG),
        ("Real-World Catastrophe",
         "Severe Financial & Physical Impact",
         [
             "Physical Venue Chaos: Two different attendee squads arrive at the door with confirmed tickets for the same seat.",
             "Financial Chargebacks: Duplicate credit card captures require manual customer service remediation and banking fees.",
             "E-Commerce Breach of Trust: Outraged customers experience public panic and loss of brand credibility.",
             "Database Corruption: Negative integers ripple through reporting and analytical data pipelines."
         ],
         GOLD_ACCENT, GOLD_BG)
    ]
    for idx, (ctitle, csub, points, col, bg_col) in enumerate(cards_s2):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(1.85)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_CARD
        card.line.color.rgb = BORDER_SUBTLE
        card.line.width = Pt(1.2)

        # Header Pill
        pill = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + Inches(0.2), Inches(3.333), Inches(0.75))
        pill.fill.solid()
        pill.fill.fore_color.rgb = bg_col
        pill.line.color.rgb = col
        ptf = pill.text_frame
        ptf.word_wrap = True
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = Inches(0.08)
        p = ptf.paragraphs[0]
        p.text = ctitle
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"
        p = ptf.add_paragraph()
        p.text = csub
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

        tb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(1.05), Inches(3.333), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        for p_idx, pt in enumerate(points):
            p = tf.paragraphs[0] if p_idx == 0 else tf.add_paragraph()
            p.text = pt
            p.font.size = Pt(9.3)
            p.font.color.rgb = TEXT_BODY if "RESULT:" not in pt else RED_ACCENT
            p.font.bold = ("RESULT:" in pt)
            p.font.name = "Segoe UI"
            p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 3: OPERATING SYSTEM THEORY (DIJKSTRA'S 3 PILLARS)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "Theoretical Foundation", "Dijkstra's Three Classical Concurrency Control Pillars",
                     "The mathematical laws governing Critical Section safety and deterministic thread synchronization")

    pillars = [
        ("Pillar 1: Mutual Exclusion",
         "|C(t)| ≤ 1 at all times t ≥ 0",
         [
             "Formal Criterion: At most ONE execution thread may execute inside the critical section at any given moment.",
             "Proof by Contradiction: If thread Ta holds the lock (_locked = true), arriving thread Tb evaluates if (!this._locked) to false.",
             "Tb cannot acquire the lock and is appended to the wait queue.",
             "Therefore, concurrent execution inside the critical section is mathematically impossible."
         ],
         CYAN_ACCENT, CYAN_BG),
        ("Pillar 2: Progress Guarantee",
         "Zero Deadlock or Livelock",
         [
             "Formal Criterion: If no thread is executing in the critical section, and threads wish to enter, only pending threads participate in selection.",
             "Selection cannot be postponed indefinitely by external or inactive processes.",
             "Fast-Path Operation: When the mutex is vacant, incoming requests acquire the lock immediately with 0ms wait delay.",
             "No artificial event-loop stalls or CPU-spinning."
         ],
         GOLD_ACCENT, GOLD_BG),
        ("Pillar 3: Bounded Waiting",
         "FIFO Elimination of Starvation",
         [
             "Formal Criterion: A bound must exist on the number of times other threads are granted entry before a pending thread is served.",
             "FIFO Queue Discipline: Arriving threads are placed in a strict First-In, First-Out array queue.",
             "Bounded Wait Proof: W(Ti) = k < ∞. With bounded execution time (ΔtCS ≤ 50ms): WaitTime(Ti) ≤ k · ΔtCS < ∞.",
             "Thread starvation is mathematically eliminated."
         ],
         EMERALD_ACCENT, EMERALD_BG)
    ]
    for idx, (ptitle, psub, points, col, bg_col) in enumerate(pillars):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(1.85)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_CARD
        card.line.color.rgb = BORDER_SUBTLE
        card.line.width = Pt(1.2)

        pill = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + Inches(0.2), Inches(3.333), Inches(0.75))
        pill.fill.solid()
        pill.fill.fore_color.rgb = bg_col
        pill.line.color.rgb = col
        ptf = pill.text_frame
        ptf.word_wrap = True
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = Inches(0.08)
        p = ptf.paragraphs[0]
        p.text = ptitle
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"
        p = ptf.add_paragraph()
        p.text = psub
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

        tb = s3.shapes.add_textbox(left + Inches(0.2), top + Inches(1.05), Inches(3.333), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        for p_idx, pt in enumerate(points):
            p = tf.paragraphs[0] if p_idx == 0 else tf.add_paragraph()
            p.text = pt
            p.font.size = Pt(9.3)
            p.font.color.rgb = TEXT_BODY
            p.font.name = "Segoe UI"
            p.space_after = Pt(4)

    # Invariant Banner
    invar_bar = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.65))
    invar_bar.fill.solid()
    invar_bar.fill.fore_color.rgb = SURFACE_ELEVATED
    invar_bar.line.color.rgb = GOLD_ACCENT
    invar_bar.line.width = Pt(1.2)
    itf = invar_bar.text_frame
    itf.margin_left = Inches(0.3)
    p = itf.paragraphs[0]
    p.text = "System Safety Invariant: ∀ t ≥ 0,  0 ≤ C_remaining(t) ≤ C_total  •  Zero Negative Inventory Tolerated"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = GOLD_ACCENT
    p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 4: ARCHITECTURE & 4-TIER PIPELINE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "System Engineering", "Four-Stage Architectural Data & Concurrency Pipeline",
                     "Clean separation of concerns across client ingress, synchronization barrier, atomic mutation, and durability")

    tiers = [
        ("Stage 1: Squad Ingress",
         "Client & Payment Authorization",
         [
             "• Squad leader enters team name, members list, and college roll numbers.",
             "• Official Razorpay checkout modal popup authorizes test UPI / Cards.",
             "• Dispatches payload to Node.js backend with unique transaction token."
         ],
         CYAN_ACCENT, CYAN_BG),
        ("Stage 2: Concurrency Barrier",
         "Distributed Lock & Keyed Registry",
         [
             "• KeyedMutexRegistry identifies the target hackathon resource ID.",
             "• DistributedLockManager coordinates cross-container serverless execution.",
             "• Requests queue up in strict FIFO arrival order; Amdahl bottlenecks prevented."
         ],
         GOLD_ACCENT, GOLD_BG),
        ("Stage 3: Critical Section",
         "Atomic Validation & State Mutation",
         [
             "• Non-preemptive capacity check: verifies remaining inventory C > 0.",
             "• Decrements seat counter atomically: C ← C - 1.",
             "• Mints cryptographic ticket code inside guaranteed `try ... finally` block."
         ],
         EMERALD_ACCENT, EMERALD_BG),
        ("Stage 4: State Durability & UI",
         "Audit Logging & Modal Dispatch",
         [
             "• Microsecond audit log records state transition (WAITING → LOCKED → UNLOCKED).",
             "• Winner receives Gold VIP Printable Boarding Pass with procedural SVG QR.",
             "• Out-raced buyer intercepted with Automated Refund Notice Modal."
         ],
         CYAN_ACCENT, CYAN_BG)
    ]
    for idx, (ttitle, tsub, tbullets, col, bg_col) in enumerate(tiers):
        left = Inches(0.8 + idx * 3.0)
        top = Inches(1.85)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.733), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_CARD
        card.line.color.rgb = BORDER_SUBTLE
        card.line.width = Pt(1.2)

        pill = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), top + Inches(0.2), Inches(2.433), Inches(0.75))
        pill.fill.solid()
        pill.fill.fore_color.rgb = bg_col
        pill.line.color.rgb = col
        ptf = pill.text_frame
        ptf.word_wrap = True
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = Inches(0.06)
        p = ptf.paragraphs[0]
        p.text = ttitle
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"
        p = ptf.add_paragraph()
        p.text = tsub
        p.font.size = Pt(7.8)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

        tb = s4.shapes.add_textbox(left + Inches(0.15), top + Inches(1.05), Inches(2.433), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        for b_idx, bullet in enumerate(tbullets):
            p = tf.paragraphs[0] if b_idx == 0 else tf.add_paragraph()
            p.text = bullet
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_BODY
            p.font.name = "Segoe UI"
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 5: KERNEL MECHANICS (ASYNC MUTEX & KEYED REGISTRY)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "Kernel Implementation", "Asynchronous Mutex & Fine-Grained Keyed Lock Registry",
                     "Designing non-preemptive mutual exclusion within Node.js single-threaded V8 event loops")

    # Left: Asynchronous Mutex
    c_left = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.9))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = SURFACE_CARD
    c_left.line.color.rgb = BORDER_SUBTLE
    c_left.line.width = Pt(1.2)

    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "ASYNCHRONOUS MUTEX PRIMITIVE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = CYAN_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    points_mutex = [
        ("Single-Threaded Event Loop Atomicity", "JavaScript evaluates microtasks sequentially. Checking `!this._locked` and setting `_locked = true` in the same synchronous turn occurs with hardware-level non-preemption."),
        ("Fast-Path (Vacant Entry)", "When the mutex is unheld, the caller transitions state to true instantly and receives a release closure with 0ms wait delay."),
        ("Slow-Path (FIFO Queue Handoff)", "When busy, the caller is wrapped in an unfulfilled Promise and pushed to `_queue`. The thread is suspended without CPU spinning."),
        ("RAII Guaranteed Release", "Wrapped in `try ... finally { releaseLock() }` to guarantee that unexpected errors or network failures never leave the mutex permanently locked.")
    ]
    for h, b in points_mutex:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_TITLE
        p.font.name = "Segoe UI"
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(6)

    # Right: Keyed Mutex Registry
    c_right = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.9))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = SURFACE_CARD
    c_right.line.color.rgb = BORDER_SUBTLE
    c_right.line.width = Pt(1.2)

    tb = s5.shapes.add_textbox(Inches(7.133), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "KEYED REGISTRY: AMDAHL BOTTLENECK ELIMINATION"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = GOLD_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    points_reg = [
        ("The Coarse-Grained Locking Bottleneck", "A single global platform lock forces all event bookings into a single queue. Buyers for Event 1 would unnecessarily block buyers for Event 2."),
        ("Per-Resource Fine-Grained Locking", "The KeyedMutexRegistry dynamically allocates independent Mutex instances mapped by event ID (`event-1`, `event-2`)."),
        ("Independent Parallelism", "Bookings for AI HackSphere and Tokyo CyberCon execute simultaneously at maximum line-rate without contention."),
        ("Localized Serialization", "Serialization is strictly enforced only when concurrent buyers contend for the exact same hackathon inventory.")
    ]
    for h, b in points_reg:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_TITLE
        p.font.name = "Segoe UI"
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 6: DISTRIBUTED SYSTEMS (CROSSING THE MULTI-DEVICE BARRIER)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "Distributed Systems Engineering", "Crossing the Physical Machine Barrier: Distributed Lock Manager",
                     "How our two-tier synchronization model eliminates container isolation hazards across multiple laptops")

    dlm_steps = [
        ("The Serverless Container Dilemma",
         "Isolated Memory Heaps",
         [
             "• In cloud deployments (Vercel/AWS Lambda), requests arriving within milliseconds land on separate microVM containers.",
             "• An in-memory JavaScript Mutex lives strictly inside a single container's RAM heap.",
             "• Laptop 1 hits Container A (locks local Mutex A) • Laptop 2 hits Container B (locks local Mutex B).",
             "• Neither container sees the other's lock → Both issue confirmed tickets for the same seat!"
         ],
         RED_ACCENT, RED_BG),
        ("The Two-Tier Synchronization Solution",
         "Local FIFO Mutex + Global Distributed Lock",
         [
             "• Tier 1 (Process Local): Dijkstra FIFO Mutex serializes threads hitting the same server instance.",
             "• Tier 2 (Global Distributed Lock): Cross-instance atomic lease lock coordinates global seat capacity.",
             "• Atomic Test-and-Set: Uses atomic Compare-And-Swap (CAS) to verify and claim the lock across cloud regions.",
             "• Single Source of Truth: All physical laptops read and write the exact same synchronized capacity."
         ],
         CYAN_ACCENT, CYAN_BG),
        ("Automatic Deadlock & Crash Immunity",
         "6-Second Auto-Expiring Leases",
         [
             "• Lease Expiration: If a container experiences network partitions or crashes mid-transaction, the lease automatically expires in 6 seconds.",
             "• Eliminates Frozen Lock States: Prevents perpetual deadlocks from halting future bookings.",
             "• Jittered Exponential Backoff: Competing instances poll gracefully without flooding networks.",
             "• 100% Mutual Exclusion: Confirmed across two physical laptops competing within 1ms!"
         ],
         EMERALD_ACCENT, EMERALD_BG)
    ]
    for idx, (ctitle, csub, points, col, bg_col) in enumerate(dlm_steps):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(1.85)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_CARD
        card.line.color.rgb = BORDER_SUBTLE
        card.line.width = Pt(1.2)

        pill = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + Inches(0.2), Inches(3.333), Inches(0.75))
        pill.fill.solid()
        pill.fill.fore_color.rgb = bg_col
        pill.line.color.rgb = col
        ptf = pill.text_frame
        ptf.word_wrap = True
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = Inches(0.08)
        p = ptf.paragraphs[0]
        p.text = ctitle
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"
        p = ptf.add_paragraph()
        p.text = csub
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

        tb = s6.shapes.add_textbox(left + Inches(0.2), top + Inches(1.05), Inches(3.333), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        for p_idx, pt in enumerate(points):
            p = tf.paragraphs[0] if p_idx == 0 else tf.add_paragraph()
            p.text = pt
            p.font.size = Pt(9.2)
            p.font.color.rgb = TEXT_BODY
            p.font.name = "Segoe UI"
            p.space_after = Pt(5)

    # =========================================================================
    # SLIDE 7: LIVE EXECUTION TRACE (MUTEX OFF VS MUTEX ON)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "Empirical Validation", "Two-Device Contention Window: Mutex OFF vs. Mutex ON",
                     "Live hardware test trace: Teacher Laptop vs. Friend Mobile competing simultaneously within 1 millisecond")

    # Left: Mutex OFF
    sc1_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.9))
    sc1_card.fill.solid()
    sc1_card.fill.fore_color.rgb = RED_BG
    sc1_card.line.color.rgb = RED_ACCENT
    sc1_card.line.width = Pt(1.5)

    tb = s7.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "SCENARIO 1: MUTEX DISABLED (OFF) — TOCTOU RACE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RED_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    timeline_off = [
        "t = 00ms: Laptop 1 reads C = 1 → Evaluates (1 > 0): VALID → Payment delay",
        "t = 15ms: Laptop 2 reads C = 1 (STALE READ!) → Evaluates: VALID",
        "t = 45ms: Laptop 1 completes payment → Decrements C ← 0 → Mints Ticket #1",
        "t = 55ms: Laptop 2 completes payment → Decrements C ← -1 → Mints Ticket #2",
        "🚨 RESULT: ANOMALY! C_remaining = -1. Two confirmed passes issued for 1 seat (Oversold!)"
    ]
    for step in timeline_off:
        p = tf.add_paragraph()
        p.text = step
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_TITLE if "RESULT:" in step else TEXT_BODY
        p.font.bold = ("RESULT:" in step)
        p.font.name = "Segoe UI"
        p.space_after = Pt(6)

    # Right: Mutex ON
    sc2_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.9))
    sc2_card.fill.solid()
    sc2_card.fill.fore_color.rgb = EMERALD_BG
    sc2_card.line.color.rgb = EMERALD_ACCENT
    sc2_card.line.width = Pt(1.5)

    tb = s7.shapes.add_textbox(Inches(7.133), Inches(2.05), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "SCENARIO 2: MUTEX ENABLED (ON) — DIJKSTRA CS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = EMERALD_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    timeline_on = [
        "t = 00ms: Laptop 1 requests lock → GRANTED! (Owner: Laptop 1)",
        "t = 12ms: Laptop 2 requests lock → BUSY! Enqueued in FIFO Wait Queue",
        "t = 30ms: Laptop 1 finishes payment → Decrements C ← 0 → Pass Confirmed TKT-01",
        "t = 31ms: Laptop 1 calls release() → Dequeues Laptop 2 & transfers lock",
        "t = 32ms: Laptop 2 enters Critical Section → Fresh Read: C = 0",
        "t = 33ms: Laptop 2 evaluates (0 ≤ 0) → REJECTED (HTTP 409 SOLD OUT)",
        "t = 35ms: Laptop 2 client intercepts 409 → Automated Refund Modal Launched!",
        "✅ RESULT: System Invariant PRESERVED: 0 ≤ C ≤ C_total. Zero Overbooking!"
    ]
    for step in timeline_on:
        p = tf.add_paragraph()
        p.text = step
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_TITLE if "RESULT:" in step else TEXT_BODY
        p.font.bold = ("RESULT:" in step)
        p.font.name = "Segoe UI"
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 8: DUAL-MODAL OUTCOMES (VIP PASS VS AUTOMATED REFUND)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "Customer Reliability", "Dual-Modal Outcomes: Verified VIP Pass vs. Automated Refund",
                     "Preserving buyer trust and eliminating manual banking disputes during high-velocity checkout rushes")

    # Left: VIP Digital Boarding Pass
    c_pass = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.9))
    c_pass.fill.solid()
    c_pass.fill.fore_color.rgb = SURFACE_CARD
    c_pass.line.color.rgb = BORDER_SUBTLE
    c_pass.line.width = Pt(1.2)

    tb = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "WINNER OUTCOME: VIP DIGITAL BOARDING PASS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = GOLD_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    pass_features = [
        ("Procedural SVG QR Engine", "Pure client-side zero-dependency generator synthesizes a 21x21 QR code matrix embedding ticket verification hash."),
        ("Squad Credential Roster", "Renders verified team name, leader email, member roll numbers, category track, and campus venue dates."),
        ("Real-Time Check-In Verification", "Organizers at the venue door scan the pass using the admin camera scanner, verifying authenticity in real time."),
        ("Printable VIP Layout", "Features dedicated `window.print()` print stylesheet for high-contrast badge printing.")
    ]
    for h, b in pass_features:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_TITLE
        p.font.name = "Segoe UI"
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(6)

    # Right: Automated Refund Modal
    c_refund = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.9))
    c_refund.fill.solid()
    c_refund.fill.fore_color.rgb = SURFACE_CARD
    c_refund.line.color.rgb = BORDER_SUBTLE
    c_refund.line.width = Pt(1.2)

    tb = s8.shapes.add_textbox(Inches(7.133), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "OUT-RACED BUYER: AUTOMATED REFUND REASSURANCE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = CYAN_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    refund_features = [
        ("HTTP 409 Interception", "The client-side API layer intercepts HTTP 409 (SOLD_OUT) immediately when the final seat is claimed milliseconds ahead."),
        ("Transparent User Modal", "Replaces jarring generic error toasts with an executive reassuring modal that explains the race condition clearly."),
        ("Cryptographic Audit Reference", "Generates a unique Razorpay tracking reference (`REFUND_RZP_849204`) mapped directly to the user's transaction."),
        ("Elimination of Chargebacks", "Informs the buyer that funds will credit within 5–7 business days, preventing customer panic and bank dispute fees.")
    ]
    for h, b in refund_features:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_TITLE
        p.font.name = "Segoe UI"
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 9: STRESS TESTING & BENCHMARK METRICS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "Performance & Verification", "High-Contention 50-Thread Stress Test & Metrics",
                     "Empirical proof of 100% invariant compliance and zero duplicate ticketing under heavy parallel load")

    # Table comparing Mutex OFF vs ON
    table_shape = s9.shapes.add_table(7, 3, Inches(0.8), Inches(1.85), Inches(11.733), Inches(3.6))
    table = table_shape.table
    table.columns[0].width = Inches(3.733)
    table.columns[1].width = Inches(4.0)
    table.columns[2].width = Inches(4.0)

    test_data = [
        ("Benchmark Metric / Parameter", "MUTEX DISABLED (OFF)", "MUTEX ENABLED (ON)"),
        ("Concurrent Contention", "50 Parallel Threads / 2 Laptops", "50 Parallel Threads / 2 Laptops"),
        ("Initial Tatkal Quota", "2 Seats Remaining", "2 Seats Remaining"),
        ("Confirmed Passes Issued", "6–8 Tickets (Severe Overbooking!)", "Exactly 2 Tickets Issued"),
        ("Rejected Requests", "0 (All requests accepted blindly)", "48 Requests Rejected (HTTP 409)"),
        ("Final Seat Inventory", "Negative (-4 to -6 Seats)", "Exactly 0 Seats Remaining"),
        ("System Safety Invariant", "VIOLATED (Data Race Anomaly)", "100% PRESERVED (Zero Overselling)")
    ]

    for row_idx, row_vals in enumerate(test_data):
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(row_idx, col_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Segoe UI"
            if row_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = SURFACE_ELEVATED
                p.font.bold = True
                p.font.size = Pt(10)
                p.font.color.rgb = GOLD_ACCENT
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = SURFACE_CARD if row_idx % 2 == 1 else BG_OBSIDIAN
                p.font.size = Pt(9.5)
                if col_idx == 1 and "VIOLATED" in val:
                    p.font.bold = True
                    p.font.color.rgb = RED_ACCENT
                elif col_idx == 2 and "PRESERVED" in val:
                    p.font.bold = True
                    p.font.color.rgb = EMERALD_ACCENT
                else:
                    p.font.color.rgb = TEXT_BODY

    # 3 Stat Cards below table
    stat_specs = [
        ("0 Double Bookings", "Strict mutual exclusion eliminates overselling", EMERALD_ACCENT, EMERALD_BG),
        ("18ms Median Lock Time", "Fast-path non-preemptive execution", CYAN_ACCENT, CYAN_BG),
        ("100% Invariant Pass", "0 ≤ C_remaining ≤ C_total holds unconditionally", GOLD_ACCENT, GOLD_BG)
    ]
    for idx, (stitle, sdesc, col, bg_col) in enumerate(stat_specs):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(5.65)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = col
        card.line.width = Pt(1.2)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = Inches(0.12)
        p = ctf.paragraphs[0]
        p.text = stitle
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"
        p = ctf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_BODY
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 10: CONCLUSION, SCALABILITY & TEAM DEFENSE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "Summary & Engineering Roadmap", "Project Conclusion, Planetary Scalability & Team Roster",
                     "Core takeaways, transition to microservice architectures, and student project contributors")

    # Left: Conclusion
    c1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(3.733), Inches(4.9))
    c1.fill.solid()
    c1.fill.fore_color.rgb = SURFACE_CARD
    c1.line.color.rgb = BORDER_SUBTLE
    c1.line.width = Pt(1.2)

    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(3.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "CORE SYSTEM TAKEAWAYS"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = CYAN_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = (
        "• Asynchronous Concurrency Vulnerability: Proved that single-threaded runtimes (Node.js) are NOT immune to race conditions across asynchronous boundaries.\n\n"
        "• Dijkstra's 3 Criteria: Formally demonstrated that Mutual Exclusion, Progress, and Bounded Waiting guarantee zero capacity overbooking.\n\n"
        "• Graceful Failure Design: Replaced frustrating failure toasts with proactive, transparent automated refund modals."
    )
    p.font.size = Pt(9.3)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # Middle: Industrial Scalability Roadmap
    c2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.85), Inches(3.733), Inches(4.9))
    c2.fill.solid()
    c2.fill.fore_color.rgb = SURFACE_CARD
    c2.line.color.rgb = BORDER_SUBTLE
    c2.line.width = Pt(1.2)

    tb = s10.shapes.add_textbox(Inches(5.0), Inches(2.05), Inches(3.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "INDUSTRIAL SCALE ROADMAP"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = GOLD_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = (
        "• Distributed Lock Managers: Transition from single-node Mutex to Redis Redlock algorithm across multi-region clusters.\n\n"
        "• Database Row-Level Locking: Implement PostgreSQL `SELECT ... FOR UPDATE` inside ACID transactions.\n\n"
        "• Event Streaming Architecture: Utilize Apache Kafka partitioned topics to linearize booking order events sequentially at 100k+ req/sec."
    )
    p.font.size = Pt(9.3)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # Right: Team Roster
    c3 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.85), Inches(3.733), Inches(4.9))
    c3.fill.solid()
    c3.fill.fore_color.rgb = SURFACE_CARD
    c3.line.color.rgb = BORDER_SUBTLE
    c3.line.width = Pt(1.2)

    tb = s10.shapes.add_textbox(Inches(9.0), Inches(2.05), Inches(3.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "TEAM DEFENSE ROSTER"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = EMERALD_ACCENT
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = (
        "SR University • B.Tech CSE Core (2nd Year)\n\n"
        "• Ch. Naveen Reddy (2503A51108)\n  Storage Tier & ACID JSON Durability\n\n"
        "• K. Shiva Saketh (2503A51109)\n  TOCTOU Race Hazard & Contention\n\n"
        "• A. Shiva Ganesh (2503A51110)\n  Team Leader & Concurrency Architect\n\n"
        "• V. Saicharan (2503A51111)\n  REST API & Distributed Dispatcher\n\n"
        "• T. Geethika (2503A51112)\n  Luxury UI/UX & Boarding Pass Engine\n\n"
        "• G. Vishwas (2503A51113)\n  Platform Admin & Systems QA"
    )
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # Save presentation
    prs.save(output_path)
    print(f"Obsidian Luxury 10-slide deck successfully created at: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_pptx = os.path.join(base_dir, "Event_Registration_OS_Product8_Presentation.pptx")
    public_pptx = os.path.join(base_dir, "public", "Event_Registration_OS_Product8_Presentation.pptx")
    synnexa_pptx = os.path.join(base_dir, "SYNNEXA_OS_Product8_Presentation.pptx")
    desktop_pptx = r"C:\Users\DELL\Desktop\Event_Registration_OS_Product8_Presentation.pptx"

    build_deck(target_pptx)
    build_deck(public_pptx)
    build_deck(synnexa_pptx)
    if os.path.exists(r"C:\Users\DELL\Desktop"):
        build_deck(desktop_pptx)
