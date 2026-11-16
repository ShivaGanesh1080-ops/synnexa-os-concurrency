# -*- coding: utf-8 -*-
"""
generate_simple_10_slide_ppt.py
Generates the official 10-slide luxury presentation deck for Event Registration (Product #8).
- Exact 10 slides requested by user
- Luxury website theme: Warm Ivory Canvas, Deep Obsidian / Midnight Slate, Warm Amber Gold, Tech Cyan & Emerald Green
- ZERO code in any slide (strictly architectural cards, flowcharts, timeline traces, and comparison tables)
- Includes all 6 team members and comprehensive OS concurrency concepts
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_10_slide_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Luxury Website Theme Palette
    BG_PAGE = RGBColor(251, 251, 250)        # #FBFBFA (Warm Luxury Ivory)
    CARD_BG = RGBColor(255, 255, 255)        # Pure White Card
    CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0 Subtle Slate Border
    TEXT_MAIN = RGBColor(15, 23, 42)         # #0F172A Deep Midnight Navy
    TEXT_BODY = RGBColor(71, 85, 105)        # #475569 Slate Body
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B Slate Muted
    ACCENT_GOLD = RGBColor(194, 142, 53)     # #C28E35 Luxury Warm Gold
    GOLD_SOFT = RGBColor(249, 245, 236)      # Soft Gold Tint
    ACCENT_CYAN = RGBColor(2, 132, 199)      # #0284C7 Tech Cyan
    CYAN_SOFT = RGBColor(238, 246, 255)      # Soft Cyan Tint
    ACCENT_EMERALD = RGBColor(5, 150, 105)   # #059669 Emerald Green
    EMERALD_SOFT = RGBColor(236, 253, 245)   # Soft Emerald Tint
    ACCENT_RED = RGBColor(220, 38, 38)       # #DC2626 Anomaly Red
    RED_SOFT = RGBColor(254, 242, 242)       # Soft Red Tint
    MIDNIGHT = RGBColor(11, 17, 32)          # #0B1120 Obsidian Dark

    def add_slide_chrome(slide):
        # 1. Base Warm Ivory Canvas
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_PAGE
        bg.line.fill.background()

        # 2. Dual-Tone Header Accent Line (Obsidian + Gold)
        bar_dark = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(8.5), Inches(0.08))
        bar_dark.fill.solid()
        bar_dark.fill.fore_color.rgb = MIDNIGHT
        bar_dark.line.fill.background()

        bar_gold = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.5), 0, Inches(4.833), Inches(0.08))
        bar_gold.fill.solid()
        bar_gold.fill.fore_color.rgb = ACCENT_GOLD
        bar_gold.line.fill.background()

        # 3. Slide Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        ftf = footer_box.text_frame
        ftf.word_wrap = True
        ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0
        p = ftf.paragraphs[0]
        p.text = "Event Registration • Product #8 Concurrency Control System • SR University CSE Core"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

    def add_header(slide, eyebrow, title, subtitle=None):
        add_slide_chrome(slide)
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(1.3))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = eyebrow.upper()
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_GOLD
        p0.font.name = "Segoe UI"
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MAIN
        p1.font.name = "Segoe UI"

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(11)
            p2.font.color.rgb = TEXT_BODY
            p2.font.name = "Segoe UI"
            p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (LUXURY EXECUTIVE OVERVIEW)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_chrome(s1)

    main_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    main_card.fill.solid()
    main_card.fill.fore_color.rgb = CARD_BG
    main_card.line.color.rgb = CARD_BORDER
    main_card.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.15), Inches(10.9), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "SR UNIVERSITY • DEPARTMENT OF CSE CORE • OPERATING SYSTEMS LAB (CS201)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Event Registration: High-Throughput Concurrency & Mutex System"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.font.name = "Segoe UI"
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Tatkal Quota Event Reservation Engine with Zero Overbooking, Distributed Locking & Automated Refund Reassurance"
    p.font.size = Pt(12.5)
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Project Team: A. Shiva Ganesh (Lead) • Ch. Naveen Reddy • K. Shiva Saketh • V. Saicharan • T. Geethika • G. Vishwas"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.font.name = "Segoe UI"
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Core OS Concepts: Dijkstra's 3 Critical Section Criteria • TOCTOU Race Condition Elimination • FIFO Bounded Waiting • Distributed Leases"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # 3 Feature Pills
    features = [
        ("Strict Mutual Exclusion", "|C(t)| ≤ 1 at all times\nZero capacity overbooking", ACCENT_CYAN, CYAN_SOFT),
        ("FIFO Wait Queue", "Bounded Waiting O(k)\nComplete thread starvation immunity", ACCENT_GOLD, GOLD_SOFT),
        ("Distributed Lock Manager", "Multi-device synchronization\nCross-container serverless safety", ACCENT_EMERALD, EMERALD_SOFT)
    ]
    for idx, (ftitle, fdesc, col, bg_col) in enumerate(features):
        left = Inches(1.2 + idx * 3.7)
        top = Inches(4.35)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.5), Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = col
        card.line.width = Pt(1.2)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = Inches(0.18)

        p = ctf.paragraphs[0]
        p.text = ftitle
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"
        p.space_after = Pt(4)

        p = ctf.add_paragraph()
        p.text = fdesc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2: THE PROBLEM (TOCTOU RACE HAZARD FORMULATION)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Concurrency Challenge", "The Flash-Reservation Hazard: Time-of-Check to Time-of-Use (TOCTOU)",
               "Why high-velocity booking platforms oversell inventory when synchronization barriers are absent")

    cards_s2 = [
        ("The Flash-Sale Dilemma",
         "High-Contention Scenarios",
         "• IRCTC Tatkal, concert booking, and university hackathons experience massive traffic spikes.\n"
         "• Contention surges specifically when remaining capacity drops to 1 or 2 seats.\n"
         "• Multiple concurrent buyer requests arrive within microsecond intervals, competing for identical slots.\n"
         "• Without mutual exclusion, inventory validation and state mutation decouple across async boundaries.",
         ACCENT_CYAN, CYAN_SOFT),
        ("TOCTOU Race Hazard Anatomy",
         "Step-by-Step Interleaving",
         "1. t0: Laptop 1 reads C = 1 (Evaluates: 1 > 0 → VALID).\n"
         "2. t1: Laptop 1 awaits payment processing delay.\n"
         "3. t2: Laptop 2 arrives, reads C = 1 (STALE READ!).\n"
         "4. t3: Laptop 1 finishes, writes C ← 0, mints Ticket #1.\n"
         "5. t4: Laptop 2 finishes, writes C ← -1, mints Ticket #2!\n"
         "Result: Invariant violated! C = -1 < 0 (Oversold).",
         ACCENT_RED, RED_SOFT),
        ("Business & Systems Impact",
         "Catastrophic Failure Modes",
         "• Physical Venue Chaos: Two squads arrive with valid QR boarding passes for 1 physical seat.\n"
         "• Financial Liabilities: Duplicate payment captures require manual refunds & bank chargebacks.\n"
         "• Legal & Reputational Damage: E-commerce breach of trust & customer panic.\n"
         "• Database Corruption: Negative integer anomalies propagate through downstream pipelines.",
         ACCENT_GOLD, GOLD_SOFT)
    ]
    for idx, (ctitle, csub, cbody, col, bg_col) in enumerate(cards_s2):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(1.85)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
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
        p = tf.paragraphs[0]
        p.text = cbody
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 3: OPERATING SYSTEM THEORY (DIJKSTRA'S 3 PILLARS)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Theoretical Foundation", "Dijkstra's Three Classical Pillars of Concurrency Control",
               "Mathematical correctness criteria guaranteeing deterministic execution in multi-threaded environments")

    pillars = [
        ("Pillar 1: Mutual Exclusion",
         "|C(t)| ≤ 1 at all timestamps t ≥ 0",
         "Proof by Contradiction:\n"
         "• Assume threads Ta and Tb simultaneously execute in Critical Section.\n"
         "• Ta enters only by transitioning lock state from false to true.\n"
         "• When Tb arrives, it evaluates lock state. Since Ta has not released, state remains true.\n"
         "• Tb is placed in wait queue and denied entry, contradicting the assumption.\n"
         "• Therefore, |C(t)| ≤ 1 holds for all time t.",
         ACCENT_CYAN, CYAN_SOFT),
        ("Pillar 2: Progress Criterion",
         "Zero Livelock or Deadlock",
         "Formal Definition:\n"
         "• If no thread holds the Critical Section, and multiple threads request entry, only pending candidates participate in selection.\n"
         "• Selection cannot be postponed indefinitely by external processes.\n"
         "• Fast-Path Optimization: If the mutex is unlocked, incoming threads acquire ownership immediately (0ms wait delay) without event-loop suspension.",
         ACCENT_GOLD, GOLD_SOFT),
        ("Pillar 3: Bounded Waiting",
         "FIFO Elimination of Starvation",
         "Bounded Wait Proof:\n"
         "• Let thread Ti request lock at treq(Ti).\n"
         "• W(Ti) is bounded by threads queued before Ti: W(Ti) = k < ∞.\n"
         "• Since critical section execution is strictly bounded (ΔtCS ≤ 50ms):\n"
         "  WaitTime(Ti) ≤ k · ΔtCS < ∞\n"
         "• FIFO queue discipline mathematically prevents thread starvation.",
         ACCENT_EMERALD, EMERALD_SOFT)
    ]
    for idx, (ptitle, psub, pbody, col, bg_col) in enumerate(pillars):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(1.85)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
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
        p = tf.paragraphs[0]
        p.text = pbody
        p.font.size = Pt(9.3)
        p.font.color.rgb = TEXT_BODY
        p.font.name = "Segoe UI"

    # Bottom Invariant Bar
    invar_bar = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.65))
    invar_bar.fill.solid()
    invar_bar.fill.fore_color.rgb = MIDNIGHT
    invar_bar.line.fill.background()
    itf = invar_bar.text_frame
    itf.margin_left = Inches(0.3)
    p = itf.paragraphs[0]
    p.text = "System Safety Invariant 1: ∀ t ≥ 0,  0 ≤ C_remaining(t) ≤ C_total  •  Zero Negative Inventory Tolerated"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & 6-STAGE PIPELINE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Architectural Design", "End-to-End Modular Pipeline & Data Flow Architecture",
               "Clean decoupling across client presentation, REST routing, concurrency barriers, and persistent storage")

    stages = [
        ("1. User Input", "Squad registration, member HTNOs, lead email & category selection", ACCENT_CYAN, CYAN_SOFT),
        ("2. Payment Auth", "Razorpay Standard modal authorization simulating card, UPI & NetBanking", ACCENT_GOLD, GOLD_SOFT),
        ("3. Concurrency Kernel", "Distributed Lock Manager & Keyed Mutex Registry intercepting threads", MIDNIGHT, GOLD_SOFT),
        ("4. Critical Section", "Atomic capacity check (C > 0), seat decrement & cryptographic signing", ACCENT_EMERALD, EMERALD_SOFT),
        ("5. Durability Tier", "Atomic JSON commit, transactional audit logging & microsecond telemetry", ACCENT_CYAN, CYAN_SOFT),
        ("6. UI Dispatch", "Pass confirmed (Gold VIP Pass) OR 409 Rejected (Automated Refund Modal)", ACCENT_GOLD, GOLD_SOFT)
    ]
    for idx, (stitle, sdesc, col, bg_col) in enumerate(stages):
        row = idx // 3
        col_idx = idx % 3
        left = Inches(0.8 + col_idx * 4.0)
        top = Inches(1.85 + row * 2.5)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)

        pill = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + Inches(0.2), Inches(3.333), Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = bg_col
        pill.line.color.rgb = col
        ptf = pill.text_frame
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = Inches(0.06)
        p = ptf.paragraphs[0]
        p.text = stitle
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

        tb = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.85), Inches(3.333), Inches(1.25))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = sdesc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 5: ASYNCHRONOUS MUTEX & KEYED REGISTRY
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Kernel Mechanics", "Asynchronous Mutex & Fine-Grained Keyed Registry",
               "Engineering non-preemptive mutual exclusion within Node.js single-threaded V8 event loops")

    # Left: Asynchronous Mutex
    left_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    left_card.line.width = Pt(1.2)

    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "ASYNCHRONOUS MUTEX PRIMITIVE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• Event Loop Non-Preemption: In Node.js, JavaScript executes on a single thread. "
        "Synchronous evaluation of `!this._locked` and setting `this._locked = true` happens atomically in one tick.\n\n"
        "• Fast-Path (Vacant): When lock is free, it transitions state to true instantly and returns an immediate release callback (0ms wait delay).\n\n"
        "• Slow-Path (Contended): When lock is held, caller is wrapped in an unfulfilled Promise, pushed into `this._queue`, safely relinquishing execution back to V8.\n\n"
        "• RAII Guaranteed Release: The critical section is wrapped in `try { ... } finally { releaseLock() }` to ensure lock release even during unhandled runtime exceptions."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # Right: Keyed Mutex Registry
    right_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.9))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = CARD_BORDER
    right_card.line.width = Pt(1.2)

    tb = s5.shapes.add_textbox(Inches(7.133), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "KEYED MUTEX REGISTRY (RESOURCE ISOLATION)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_GOLD
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• Amdahl's Law Bottleneck: A single global lock creates unnecessary system serialization. "
        "Buyers for Event #1 would lock out buyers for Event #2, crippling platform throughput.\n\n"
        "• Fine-Grained Per-Event Registry: `KeyedMutexRegistry.get(eventId)` instantiates independent Mutex instances indexed by resource key.\n\n"
        "• Concurrent Parallelism: Bookings for Event 1 (AI HackSphere) and Event 2 (Tokyo CyberCon) proceed in parallel at full hardware line-rate.\n\n"
        "• Localized Contention: Strict serialization is enforced strictly when multiple requests target the same event ID."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 6: DISTRIBUTED LOCK MANAGER (SERVERLESS MULTI-DEVICE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Distributed Systems Engineering", "Scaling Beyond a Single Machine: Distributed Lock Manager (DLM)",
               "Guaranteeing Mutual Exclusion across multi-instance serverless microVMs and separate physical laptops")

    dlm_cards = [
        ("The Multi-Instance Challenge",
         "Serverless Memory Isolation",
         "• On cloud platforms (Vercel/AWS Lambda), requests from different laptops land on separate microVM containers.\n"
         "• Each container possesses its own isolated RAM heap. In-memory locks cannot cross process boundaries.\n"
         "• Laptop 1 locks Instance #1, Laptop 2 locks Instance #2 → Both issue passes simultaneously!",
         ACCENT_RED, RED_SOFT),
        ("Two-Tier Lock Architecture",
         "Local Mutex + Distributed Lease",
         "• Tier 1 (Process Local): Dijkstra FIFO Mutex orders requests arriving at the same server instance.\n"
         "• Tier 2 (Global Distributed Lock): Cross-instance atomic lease lock coordinates global remaining capacity.\n"
         "• Real-Time Atomic CAS: Test-and-Set guarantees only one container successfully reserves the final seat.",
         ACCENT_CYAN, CYAN_SOFT),
        ("Lease Timeout & Deadlock Safety",
         "Zero Frozen Lock States",
         "• 6-Second Lease Timeout: If a container experiences network partitions or crashes mid-flight, the lock automatically expires.\n"
         "• Bounded Backoff: Competing instances poll with jittered exponential backoff.\n"
         "• Zero Double-Booking: Guarantees strict serialization across physical laptops worldwide.",
         ACCENT_EMERALD, EMERALD_SOFT)
    ]
    for idx, (ctitle, csub, cbody, col, bg_col) in enumerate(dlm_cards):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(1.85)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.733), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
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
        p = tf.paragraphs[0]
        p.text = cbody
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 7: LIVE EXECUTION COMPARISON: MUTEX OFF VS MUTEX ON
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Empirical Execution Trace", "Two-Device Contention Window: Mutex OFF vs. Mutex ON",
               "Real-time millisecond execution timeline comparing unprotected race conditions against Mutex serialization")

    # Left: Mutex OFF
    sc1_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.9))
    sc1_card.fill.solid()
    sc1_card.fill.fore_color.rgb = RED_SOFT
    sc1_card.line.color.rgb = ACCENT_RED
    sc1_card.line.width = Pt(1.5)

    tb = s7.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "SCENARIO 1: MUTEX PROTECTION DISABLED (OFF)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_RED
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• Initial State: Event has C = 1 remaining Tatkal seat.\n"
        "• t = 00ms: Laptop 1 reads C = 1 → Evaluates check (1 > 0) as VALID.\n"
        "• t = 15ms: Laptop 2 reads C = 1 (STALE READ!). Check evaluated as VALID.\n"
        "• t = 45ms: Laptop 1 finishes payment → Decrements C ← 0 → Mints Ticket #1.\n"
        "• t = 55ms: Laptop 2 finishes payment → Decrements C ← -1 → Mints Ticket #2!\n\n"
        "🚨 ANOMALY CONFIRMED: System oversold! Remaining capacity C = -1. Two confirmed passes issued for a single physical seat!"
    )
    p.font.size = Pt(9.8)
    p.font.color.rgb = TEXT_MAIN
    p.font.name = "Segoe UI"

    # Right: Mutex ON
    sc2_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.9))
    sc2_card.fill.solid()
    sc2_card.fill.fore_color.rgb = EMERALD_SOFT
    sc2_card.line.color.rgb = ACCENT_EMERALD
    sc2_card.line.width = Pt(1.5)

    tb = s7.shapes.add_textbox(Inches(7.133), Inches(2.05), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "SCENARIO 2: MUTEX PROTECTION ENABLED (ON)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_EMERALD
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• Initial State: Event has C = 1 remaining Tatkal seat.\n"
        "• t = 00ms: Laptop 1 requests lock → GRANTED! Enters Critical Section.\n"
        "• t = 12ms: Laptop 2 requests lock → BUSY! Enqueued into FIFO Wait Queue.\n"
        "• t = 30ms: Laptop 1 finishes checkout → Decrements C ← 0 → Pass Confirmed TKT-01.\n"
        "• t = 31ms: Laptop 1 calls release() → Dequeues Laptop 2 and transfers lock.\n"
        "• t = 32ms: Laptop 2 enters Critical Section → Fresh Read: C = 0.\n"
        "• t = 33ms: Laptop 2 evaluates (0 ≤ 0) → REJECTED (HTTP 409 SOLD OUT).\n"
        "• t = 35ms: Laptop 2 client intercepts 409 → Automated Refund Modal launched!\n\n"
        "✅ INVARIANT PRESERVED: Capacity bounded [0, C_total]. Zero overbooking!"
    )
    p.font.size = Pt(9.8)
    p.font.color.rgb = TEXT_MAIN
    p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 8: AUTOMATED REFUND REASSURANCE & VIP PASS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "User Experience & Reliability", "Dual-Modal Outcomes: Verified VIP Pass vs. Automated Refund",
               "Preserving buyer trust during high-contention checkout races without customer service friction")

    # Left: VIP Digital Boarding Pass
    left_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    left_card.line.width = Pt(1.2)

    tb = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "WINNER OUTCOME: VIP DIGITAL BOARDING PASS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_GOLD
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• Procedural SVG QR Code: Pure client-side zero-dependency generator creates 21x21 QR matrix embedding ticket verification hash.\n\n"
        "• Squad Credential Roster: Displays verified squad leader, teammate names, college roll numbers, and venue dates.\n\n"
        "• Door Scanner Check-In: Event organizers use the built-in check-in module to scan QR codes and mark attendance in real time.\n\n"
        "• Verified Cryptographic Pass: Includes payment reference ID and window.print() print stylesheet."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # Right: Automated Refund Modal
    right_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.9))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = CARD_BORDER
    right_card.line.width = Pt(1.2)

    tb = s8.shapes.add_textbox(Inches(7.133), Inches(2.1), Inches(5.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "OUT-RACED BUYER: AUTOMATED REFUND REASSURANCE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• HTTP 409 Interception: Client-side fetch wrapper detects status 409 (SOLD_OUT) immediately when the final seat is claimed.\n\n"
        "• Automated Refund Reassurance Modal: Replaces error toasts with an executive reassuring modal.\n\n"
        "• Transaction Reference: Generates unique tracking ID (e.g. `REFUND_RZP_849204`) mapped to original Razorpay transaction.\n\n"
        "• Commercial Protection: Informs buyer that bank account will be credited within 5–7 business days, preventing chargebacks."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 9: STRESS TESTING & BENCHMARK RESULTS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Verification & Testing", "High-Contention Stress Benchmark & Hardware Testing",
               "Empirical verification proving 100% invariant preservation under heavy concurrent load")

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
                cell.fill.fore_color.rgb = MIDNIGHT
                p.font.bold = True
                p.font.size = Pt(10)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else RGBColor(248, 250, 252)
                p.font.size = Pt(9.5)
                if col_idx == 1 and "VIOLATED" in val:
                    p.font.bold = True
                    p.font.color.rgb = ACCENT_RED
                elif col_idx == 2 and "PRESERVED" in val:
                    p.font.bold = True
                    p.font.color.rgb = ACCENT_EMERALD
                else:
                    p.font.color.rgb = TEXT_MAIN

    # 3 Stat Cards below table
    stat_specs = [
        ("0 Double Bookings", "Strict mutual exclusion eliminates overselling", ACCENT_EMERALD, EMERALD_SOFT),
        ("18ms Median Lock Time", "Fast-path non-preemptive execution", ACCENT_CYAN, CYAN_SOFT),
        ("100% Invariant Pass", "0 ≤ C_remaining ≤ C_total holds unconditionally", ACCENT_GOLD, GOLD_SOFT)
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
    # SLIDE 10: CONCLUSION, SCALABILITY & TEAM ROSTER
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Summary & Engineering Roadmap", "Project Conclusion, Planetary Scalability & Team Roster",
               "Key academic takeaways, industrial microservice patterns, and student module contributors")

    # Left: Conclusion
    c1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(3.733), Inches(4.9))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = CARD_BORDER
    c1.line.width = Pt(1.2)

    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(3.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "ACADEMIC TAKEAWAYS"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• Concurrency in Asynchronous Runtimes: Demonstrated that single-threaded event loops (Node.js) are NOT inherently immune to race hazards across async boundaries.\n\n"
        "• Dijkstra's 3 Pillars: Formally validated that Mutual Exclusion, Progress, and Bounded Waiting guarantee zero capacity anomalies.\n\n"
        "• Graceful Failure Design: Replaced jarring failure toasts with transparent automated refund modals."
    )
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # Middle: Industrial Scalability Roadmap
    c2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.85), Inches(3.733), Inches(4.9))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = CARD_BORDER
    c2.line.width = Pt(1.2)

    tb = s10.shapes.add_textbox(Inches(5.0), Inches(2.05), Inches(3.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "INDUSTRIAL SCALE ROADMAP"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_GOLD
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "• Distributed Lock Managers: Transition from single-node Mutex to Redis Redlock algorithm across multi-region clusters.\n\n"
        "• Database Row-Level Locking: Implement PostgreSQL `SELECT ... FOR UPDATE` inside ACID transactions.\n\n"
        "• Event Streaming Architecture: Utilize Apache Kafka partitioned topics to linearize booking order events sequentially at 100k+ req/sec."
    )
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_BODY
    p.font.name = "Segoe UI"

    # Right: Team Roster
    c3 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.85), Inches(3.733), Inches(4.9))
    c3.fill.solid()
    c3.fill.fore_color.rgb = CARD_BG
    c3.line.color.rgb = CARD_BORDER
    c3.line.width = Pt(1.2)

    tb = s10.shapes.add_textbox(Inches(9.0), Inches(2.05), Inches(3.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "TEAM ROSTER & DEFENSE"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_EMERALD
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = (
        "SR University • B.Tech CSE Core (2nd Year)\n\n"
        "• Ch. Naveen Reddy (2503A51108)\n  Storage Tier & ACID JSON Durability\n\n"
        "• K. Shiva Saketh (2503A51109)\n  TOCTOU Race Hazard & Contention\n\n"
        "• A. Shiva Ganesh (2503A51110)\n  Team Leader & Concurrency Architect\n\n"
        "• V. Saicharan (2503A51111)\n  REST API & Distributed Dispatcher\n\n"
        "• T. Geethika (2503A1112)\n  Luxury UI/UX & Boarding Pass Engine\n\n"
        "• G. Vishwas (2503A51113)\n  Platform Admin & Systems QA"
    )
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_MAIN
    p.font.name = "Segoe UI"

    # Save to destination
    prs.save(output_path)
    print(f"Simple 10-slide luxury deck generated successfully at: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_pptx = os.path.join(base_dir, "Event_Registration_OS_Product8_Presentation.pptx")
    public_pptx = os.path.join(base_dir, "public", "Event_Registration_OS_Product8_Presentation.pptx")
    synnexa_pptx = os.path.join(base_dir, "SYNNEXA_OS_Product8_Presentation.pptx")
    desktop_pptx = r"C:\Users\DELL\Desktop\Event_Registration_OS_Product8_Presentation.pptx"

    create_10_slide_deck(target_pptx)
    create_10_slide_deck(public_pptx)
    create_10_slide_deck(synnexa_pptx)
    if os.path.exists(r"C:\Users\DELL\Desktop"):
        create_10_slide_deck(desktop_pptx)
