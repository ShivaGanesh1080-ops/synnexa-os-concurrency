import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    # 16:9 Widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors (Light Slate Modern Design)
    BG_COLOR = RGBColor(248, 250, 252)       # Slate 50
    CARD_BG = RGBColor(255, 255, 255)        # Pure White
    CARD_BORDER = RGBColor(226, 232, 240)    # Slate 200
    TEXT_DARK = RGBColor(15, 23, 42)         # Slate 900
    TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500
    PRIMARY = RGBColor(79, 70, 229)          # Indigo 600
    PRIMARY_DARK = RGBColor(49, 46, 129)     # Indigo 900
    PRIMARY_LIGHT = RGBColor(238, 242, 255)  # Indigo 50
    SECONDARY = RGBColor(14, 165, 233)       # Sky 500
    ACCENT = RGBColor(139, 92, 246)          # Purple 500
    DANGER = RGBColor(239, 68, 68)           # Red 500
    DANGER_LIGHT = RGBColor(254, 242, 242)   # Red 50
    SUCCESS = RGBColor(16, 185, 129)         # Emerald 500
    SUCCESS_LIGHT = RGBColor(236, 253, 245)  # Emerald 50

    def add_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = PRIMARY
        bar.line.fill.background()

    def add_header(slide, eyebrow, title, subtitle=None):
        add_slide_background(slide)

        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.3))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = eyebrow.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY
        p0.font.name = "Segoe UI"
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_DARK
        p1.font.name = "Segoe UI"

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(12)
            p2.font.color.rgb = TEXT_MUTED
            p2.font.name = "Segoe UI"
            p2.space_before = Pt(3)

    # ────────────────────────────────────────────────────────────────
    # SLIDE 1: TITLE SLIDE
    # ────────────────────────────────────────────────────────────────
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_background(s1)

    main_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    main_card.fill.solid()
    main_card.fill.fore_color.rgb = CARD_BG
    main_card.line.color.rgb = CARD_BORDER
    main_card.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.8), Inches(1.3), Inches(9.733), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SR UNIVERSITY • CSE CORE • OPERATING SYSTEMS LAB • PRODUCT #8"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.font.name = "Segoe UI"
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Critical Section & Mutex Synchronization"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.font.name = "Segoe UI"
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = "High-Throughput Tatkal Event & Hackathon Registration Platform"
    p.font.size = Pt(17)
    p.font.color.rgb = SECONDARY
    p.font.name = "Segoe UI"
    p.space_after = Pt(20)

    p = tf.add_paragraph()
    p.text = "Team Leader: A. Shiva Ganesh (HTNO: 2503A51110)  |  B.Tech CSE Core (2nd Year)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.font.name = "Segoe UI"
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Key Invariants: Mutex Mutual Exclusion, Zero Overbooking, FIFO Bounded Waiting, IRCTC Tatkal Concurrency Rush"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.font.name = "Segoe UI"

    stats = [
        ("Zero Overbooking", "Strict Mutual Exclusion", PRIMARY),
        ("FIFO Wait Queue", "Zero Starvation Guarantee", SECONDARY),
        ("Per-Resource Locks", "Fine-Grained Isolation", ACCENT)
    ]
    for i, (title, desc, color) in enumerate(stats):
        cx = Inches(1.8 + i * 3.3)
        cy = Inches(4.8)
        sc = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, Inches(3.1), Inches(1.2))
        sc.fill.solid()
        sc.fill.fore_color.rgb = PRIMARY_LIGHT if i == 0 else (CARD_BG)
        sc.line.color.rgb = color
        sc.line.width = Pt(1.5)
        stf = sc.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_right = Inches(0.2)
        stf.margin_top = Inches(0.2)
        sp1 = stf.paragraphs[0]
        sp1.text = title
        sp1.font.bold = True
        sp1.font.size = Pt(13)
        sp1.font.color.rgb = color
        sp1.font.name = "Segoe UI"
        sp2 = stf.add_paragraph()
        sp2.text = desc
        sp2.font.size = Pt(10.5)
        sp2.font.color.rgb = TEXT_MUTED
        sp2.font.name = "Segoe UI"

    # ────────────────────────────────────────────────────────────────
    # SLIDE 2: PROJECT ENGINEERING TEAM (ASCENDING HTNO ORDER)
    # ────────────────────────────────────────────────────────────────
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Engineering Roster", "Project Team Members & Work Distribution",
               "Sorted in ascending order of Hall Ticket Numbers with specialized module ownership.")

    team_members = [
        ("2503A51108", "Ch. Naveen Reddy", "Core Persistence & Storage Tier",
         "Designed file-backed JSON transactional persistence, atomic tempfile rename algorithms, and data schema migrations.",
         SECONDARY),
        ("2503A51109", "K. Shiva Saketh", "Concurrency & Race Condition Engine",
         "Constructed TOCTOU un-synchronized execution branch, dirty read generators, and negative seat overbooking verifications.",
         PRIMARY),
        ("2503A51110", "A. Shiva Ganesh", "Team Leader & Mutex Architecture",
         "Architected custom asynchronous Mutex primitive, FIFO bounded wait queue, KeyedMutexRegistry, and end-to-end system design.",
         PRIMARY_DARK),
        ("2503A51111", "V. Saicharan", "REST API & High-Throughput Dispatcher",
         "Implemented high-performance zero-dependency Node.js HTTP controllers, CORS pipeline, and microsecond audit telemetry.",
         ACCENT),
        ("2503A51112", "T. Geethika", "Full-Stack UI/UX & Portal Experience",
         "Built responsive light-slate dashboard, dynamic team member roster inputs, and pure procedural SVG QR boarding pass engine.",
         SECONDARY),
        ("2503A51113", "G. Vishwas", "Platform Administration & System QA",
         "Configured Razorpay Test Mode gateway interface, door check-in scanner module, CSV roster exporter, and viva defense test harness.",
         SUCCESS)
    ]

    for i, (htno, name, role, desc, color) in enumerate(team_members):
        col = i % 3
        row = i // 3
        cx = Inches(0.8 + col * 4.0)
        cy = Inches(1.85 + row * 2.65)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, Inches(3.7), Inches(2.45))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.25)

        p = ctf.paragraphs[0]
        p.text = f"{htno}  •  {role.split('&')[0].strip()}"
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = color

        p = ctf.add_paragraph()
        p.text = name + (" (Leader)" if "Shiva Ganesh" in name else "")
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

        p = ctf.add_paragraph()
        p.text = role
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

        p = ctf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # ────────────────────────────────────────────────────────────────
    # SLIDE 3: PROBLEM STATEMENT & IRCTC TATKAL ANALOGY
    # ────────────────────────────────────────────────────────────────
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement", "The Concurrency Rush: IRCTC Tatkal Flash Booking",
               "Analyzing Product 8: 'Several users attempt to register when only one or two places remain.'")

    c_left = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(5.0))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = DANGER_LIGHT
    c_left.line.color.rgb = DANGER
    c_left.line.width = Pt(1.5)
    ltf = c_left.text_frame
    ltf.word_wrap = True
    ltf.margin_left = ltf.margin_right = ltf.margin_top = Inches(0.35)
    
    lp0 = ltf.paragraphs[0]
    lp0.text = "WITHOUT MUTEX: RACE CONDITION HAZARD"
    lp0.font.bold = True
    lp0.font.size = Pt(13)
    lp0.font.color.rgb = DANGER
    lp0.space_after = Pt(12)

    bullets_left = [
        ("Stale Reads (TOCTOU):", "Thread A and Thread B concurrently read remainingCapacity = 1 at the same exact millisecond."),
        ("False Condition Check:", "Both threads evaluate 'remainingCapacity > 0' as TRUE because neither has written back yet."),
        ("Unsynchronized Writes:", "Both threads decrement capacity from 1 -> 0 and 0 -> -1, issuing two valid tickets for a single physical seat."),
        ("Catastrophic State:", "Capacity drops to negative values (-1, -7, -18). The system violates physical venue capacity limits.")
    ]
    for b_title, b_desc in bullets_left:
        bp = ltf.add_paragraph()
        bp.text = f"• {b_title} "
        bp.font.bold = True
        bp.font.size = Pt(11)
        bp.font.color.rgb = TEXT_DARK
        run = bp.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(8)

    c_right = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(5.0))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = SUCCESS_LIGHT
    c_right.line.color.rgb = SUCCESS
    c_right.line.width = Pt(1.5)
    rtf = c_right.text_frame
    rtf.word_wrap = True
    rtf.margin_left = rtf.margin_right = rtf.margin_top = Inches(0.35)

    rp0 = rtf.paragraphs[0]
    rp0.text = "WITH MUTEX: CRITICAL SECTION SERIALIZATION"
    rp0.font.bold = True
    rp0.font.size = Pt(13)
    rp0.font.color.rgb = SUCCESS
    rp0.space_after = Pt(12)

    bullets_right = [
        ("Atomic Lock Acquisition:", "Thread A acquires the event Mutex before reading capacity. Thread B's request is enqueued into a FIFO wait queue."),
        ("Isolated Execution:", "Thread A checks capacity, checks for duplicate email, decrements capacity from 1 -> 0, commits ticket, and releases lock."),
        ("Clean Rejection:", "Thread B wakes up, enters the critical section, reads updated capacity (0), and is cleanly rejected with 409 SOLD_OUT."),
        ("Guaranteed Invariant:", "Capacity never drops below zero (0 <= remaining <= total). Venue safety and consistency are 100% preserved.")
    ]
    for b_title, b_desc in bullets_right:
        bp = rtf.add_paragraph()
        bp.text = f"• {b_title} "
        bp.font.bold = True
        bp.font.size = Pt(11)
        bp.font.color.rgb = TEXT_DARK
        run = bp.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(8)

    # ────────────────────────────────────────────────────────────────
    # SLIDE 4: TOCTOU TIMELINE TRACE TABLE
    # ────────────────────────────────────────────────────────────────
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Concurrency Theory", "The Mechanics of a Check-Then-Act Race Condition",
               "Deconstructing register-level non-atomicity during concurrent ticket requests.")

    tb_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(11.733), Inches(5.1))
    tb_card.fill.solid()
    tb_card.fill.fore_color.rgb = CARD_BG
    tb_card.line.color.rgb = CARD_BORDER

    rows, cols = 8, 4
    left, top, width, height = Inches(1.1), Inches(2.1), Inches(11.133), Inches(4.5)
    table = s4.shapes.add_table(rows, cols, left, top, width, height).table
    table.columns[0].width = Inches(1.2)
    table.columns[1].width = Inches(3.7)
    table.columns[2].width = Inches(3.7)
    table.columns[3].width = Inches(2.533)

    headers = ["Time", "Thread 1 (User A)", "Thread 2 (User B)", "Shared Memory State"]
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.size = Pt(11)
            p.alignment = PP_ALIGN.CENTER

    data = [
        ("t0", "READ remainingCapacity (1)", "[Idle / Queued]", "remainingCapacity = 1"),
        ("t1", "[CPU Context Switch]", "READ remainingCapacity (1) [STALE]", "remainingCapacity = 1"),
        ("t2", "CHECK (1 > 0) -> TRUE", "[Idle]", "remainingCapacity = 1"),
        ("t3", "[Idle]", "CHECK (1 > 0) -> TRUE [STALE CHECK]", "remainingCapacity = 1"),
        ("t4", "DECREMENT: 1 - 1 = 0", "[Idle]", "Reg_T1 = 0"),
        ("t5", "WRITE: commit ticket A", "DECREMENT: 0 - 1 = -1", "remainingCapacity = 0"),
        ("t6", "STATUS: Confirmed (Ticket A)", "WRITE: commit ticket B [CORRUPTION!]", "remainingCapacity = -1 (OVERBOOKED!)")
    ]
    for r_idx, row in enumerate(data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            if r_idx % 2 == 0:
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252)
            else:
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            if "OVERBOOKED" in val or "CORRUPTION" in val:
                cell.fill.fore_color.rgb = DANGER_LIGHT
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.name = "Segoe UI"
                if c_idx == 0:
                    p.alignment = PP_ALIGN.CENTER
                    p.font.bold = True
                elif "OVERBOOKED" in val:
                    p.font.bold = True
                    p.font.color.rgb = DANGER
                else:
                    p.font.color.rgb = TEXT_DARK

    # ────────────────────────────────────────────────────────────────
    # SLIDE 5: 3 PILLARS OF CRITICAL SECTION SOLUTION
    # ────────────────────────────────────────────────────────────────
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Dijkstra's Criteria", "The 3 Pillars of the Critical Section Solution",
               "Every production-grade OS synchronization mechanism must satisfy all three criteria without exception.")

    criteria = [
        ("1. Mutual Exclusion",
         "Strict Invariant Enforcement",
         "At most one process / thread can execute within the critical section for a specific resource at any given moment.",
         "Implementation:",
         "Our Mutex uses an atomic '_locked' state flag. Any secondary caller attempting entry while locked is intercepted and prevented from executing the critical block.",
         PRIMARY),
        ("2. Progress Guarantee",
         "Deadlock-Free Scheduling",
         "If no process is in the critical section and some processes wish to enter, only those not in their remainder section can decide who enters next. Selection cannot be postponed indefinitely.",
         "Implementation:",
         "Locks are granted immediately upon request if vacant. Asynchronous resolution prevents any deadlocks or extraneous stalls.",
         SECONDARY),
        ("3. Bounded Waiting",
         "Zero Starvation Policy",
         "There must be a deterministic limit on the number of times other processes can enter the critical section after a process has requested entry, before its request is granted.",
         "Implementation:",
         "Enforced through a strict First-In, First-Out (FIFO) wait queue array. Every competing thread has an upper bound of O(k) wait cycles.",
         ACCENT)
    ]

    for i, (title, sub, desc, impl_lbl, impl_desc, color) in enumerate(criteria):
        cx = Inches(0.8 + i * 4.0)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.9), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(2)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.3)

        p = ctf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = color
        p.space_after = Pt(2)

        p = ctf.add_paragraph()
        p.text = sub
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(14)

        p = ctf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(16)

        p = ctf.add_paragraph()
        p.text = impl_lbl
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = color
        p.space_after = Pt(4)

        p = ctf.add_paragraph()
        p.text = impl_desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

    # ────────────────────────────────────────────────────────────────
    # SLIDE 6: ASYNC MUTEX ARCHITECTURE WITH FIFO QUEUE
    # ────────────────────────────────────────────────────────────────
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Core Primitive Design", "Asynchronous Mutex with FIFO Wait Queue",
               "How 'src/core/Mutex.js' avoids busy-waiting spinlocks and eliminates thread starvation.")

    c_code = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(6.0), Inches(5.0))
    c_code.fill.solid()
    c_code.fill.fore_color.rgb = CARD_BG
    c_code.line.color.rgb = CARD_BORDER
    ctf = c_code.text_frame
    ctf.word_wrap = True
    ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.3)

    p = ctf.paragraphs[0]
    p.text = "MUTEX ACQUIRE & RELEASE ALGORITHM"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(10)

    code_lines = [
        "acquire(requesterId) {",
        "  if (!this._locked) {",
        "    this._locked = true; // Fast Path: Grant lock",
        "    this._currentOwner = requesterId;",
        "    return Promise.resolve(releaseCallback);",
        "  }",
        "  // Contention Path: Enqueue in FIFO Wait Queue",
        "  return new Promise(resolve => {",
        "    this._queue.push({ requesterId, grant: () => {",
        "      this._locked = true;",
        "      this._currentOwner = requesterId;",
        "      resolve(releaseCallback);",
        "    }});",
        "  });",
        "}",
        "_release(ownerId) {",
        "  if (this._queue.length > 0) {",
        "    const next = this._queue.shift(); // Strict FIFO!",
        "    next.grant();",
        "  } else { this._locked = false; }",
        "}"
    ]
    for cl in code_lines:
        p = ctf.add_paragraph()
        p.text = cl
        p.font.size = Pt(9.5)
        p.font.name = "Consolas"
        p.font.color.rgb = TEXT_DARK if not cl.strip().startswith("//") else PRIMARY

    c_adv = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.9), Inches(5.4), Inches(5.0))
    c_adv.fill.solid()
    c_adv.fill.fore_color.rgb = PRIMARY_LIGHT
    c_adv.line.color.rgb = PRIMARY
    atf = c_adv.text_frame
    atf.word_wrap = True
    atf.margin_left = atf.margin_right = atf.margin_top = Inches(0.35)

    p = atf.paragraphs[0]
    p.text = "KEY ARCHITECTURAL HIGHLIGHTS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = PRIMARY_DARK
    p.space_after = Pt(14)

    advs = [
        ("No CPU Burn (Zero Busy-Waiting):", "Traditional spinlocks burn 100% CPU waiting for locks. Our async mutex suspends the task non-blockingly until awoken via the event loop."),
        ("Strict FIFO Bounded Waiting:", "Calls are dequeued in the exact order of their arrival. High-priority threads cannot starve low-priority threads."),
        ("Telemetry & Real-Time Metrics:", "Calculates active queue length, maximum queue surge, total acquisitions, and microsecond lock-hold durations."),
        ("Exception Safety Guarantee:", "Encapsulated in 'runExclusive(task)' using try...finally to ensure locks are never orphaned even if an exception occurs.")
    ]
    for atitle, adesc in advs:
        p = atf.add_paragraph()
        p.text = f"✔ {atitle} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = PRIMARY_DARK
        run = p.add_run()
        run.text = adesc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # ────────────────────────────────────────────────────────────────
    # SLIDE 7: FINE-GRAINED KEYED MUTEX REGISTRY
    # ────────────────────────────────────────────────────────────────
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Scalability & Concurrency", "Lock Granularity: Coarse vs. Fine-Grained Locking",
               "How 'KeyedMutexRegistry.js' unlocks maximum parallelism across independent events.")

    c_coarse = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(5.0))
    c_coarse.fill.solid()
    c_coarse.fill.fore_color.rgb = DANGER_LIGHT
    c_coarse.line.color.rgb = DANGER
    ctf = c_coarse.text_frame
    ctf.word_wrap = True
    ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.35)

    p = ctf.paragraphs[0]
    p.text = "COARSE-GRAINED LOCKING (SINGLE GLOBAL MUTEX)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = DANGER
    p.space_after = Pt(12)

    c_points = [
        ("Global Serialization:", "A single global lock protects the entire database or application server."),
        ("Artificial Bottleneck:", "A user registering for 'Hackathon A' blocks a user registering for 'Hackathon B', despite zero shared state."),
        ("Severe Latency Degradation:", "Throughput collapses linearly with the number of concurrent events. Amdahl's Law limits multi-core benefits."),
        ("High Contention Overhead:", "Massive lock contention queues even under normal organizational loads.")
    ]
    for cp_title, cp_desc in c_points:
        p = ctf.add_paragraph()
        p.text = f"✖ {cp_title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        run = p.add_run()
        run.text = cp_desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    c_fine = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(5.0))
    c_fine.fill.solid()
    c_fine.fill.fore_color.rgb = SUCCESS_LIGHT
    c_fine.line.color.rgb = SUCCESS
    ftf = c_fine.text_frame
    ftf.word_wrap = True
    ftf.margin_left = ftf.margin_right = ftf.margin_top = Inches(0.35)

    p = ftf.paragraphs[0]
    p.text = "FINE-GRAINED LOCKING (KEYED MUTEX REGISTRY)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = SUCCESS
    p.space_after = Pt(12)

    f_points = [
        ("Per-Resource Partitioning:", "Each unique eventId maintains its own independent Mutex instance."),
        ("Parallel Execution:", "Registrations for Event #1 and Event #2 run simultaneously at maximum speed without locking each other."),
        ("Localized Serialization:", "Only requests competing for the exact same event are serialized, preserving consistency where needed."),
        ("Dynamic Lock Instantiation:", "Mutexes are lazily created on-demand as events are accessed, conserving system resources.")
    ]
    for fp_title, fp_desc in f_points:
        p = ftf.add_paragraph()
        p.text = f"✔ {fp_title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        run = p.add_run()
        run.text = fp_desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # ────────────────────────────────────────────────────────────────
    # SLIDE 8: 3-ROLE ENTERPRISE SYSTEM ARCHITECTURE
    # ────────────────────────────────────────────────────────────────
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Platform Architecture", "3 Dedicated Role Dashboards & Concurrency Engine",
               "Architectural division separating participant booking, organizer release, and gateway management.")

    roles = [
        ("Platform Administrator",
         "Gateway & Audit Command Center",
         "• Razorpay Test Mode integration (Key ID & Secret management)\n• Global platform fee governance and webhook orchestration\n• High-resolution microsecond audit trail covering every critical section\n• Global metrics: Total events, revenue, acquisitions, contentions",
         PRIMARY),
        ("Hackathon Organizer (Admin)",
         "Batch Release & Crowd Management",
         "• Dynamic ticket batch creation (Total Quota vs Tatkal Rush Quota)\n• Event-level Mutex toggles (Protected Mode vs Race Test Mode)\n• Live attendee roster inspection with dynamic multi-member squad display\n• Door check-in tool and 1-click CSV roster exporter for judges",
         SECONDARY),
        ("User / Participant Portal",
         "Tatkal Flash Booking & Passes",
         "• Live hackathon discovery with real-time seat depletion bars\n• Multi-member squad registration (Team Leader + dynamic members)\n• Razorpay Test Mode checkout card with instant mock authorization\n• Confirmed digital boarding passes with procedural pure-SVG QR codes",
         ACCENT),
        ("Tatkal Concurrency Studio",
         "Real-Time OS Benchmark Lab",
         "• Microsecond terminal streaming actual kernel lock events\n• Real concurrent async request storm (Promise.all) against backend\n• Live hardware lock status: LOCKED (pulsing red) vs UNLOCKED (green)\n• Side-by-side scorecard comparing Mutex vs TOCTOU race condition",
         SUCCESS)
    ]

    for i, (title, sub, desc, color) in enumerate(roles):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 5.9)
        cy = Inches(1.85 + row * 2.65)

        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, Inches(5.6), Inches(2.45))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.25)

        p = ctf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = color

        p = ctf.add_paragraph()
        p.text = sub
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

        p = ctf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # ────────────────────────────────────────────────────────────────
    # SLIDE 9: EMPIRICAL BENCHMARKS (MUTEX VS RACE CONDITION)
    # ────────────────────────────────────────────────────────────────
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Empirical Verification", "Live Concurrency Stress Benchmark Results",
               "Empirical verification demonstrating 100% data integrity with Mutex vs severe overbooking without Mutex.")

    m_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(5.0))
    m_card.fill.solid()
    m_card.fill.fore_color.rgb = SUCCESS_LIGHT
    m_card.line.color.rgb = SUCCESS
    m_card.line.width = Pt(2)
    mtf = m_card.text_frame
    mtf.word_wrap = True
    mtf.margin_left = mtf.margin_right = mtf.margin_top = Inches(0.35)

    p = mtf.paragraphs[0]
    p.text = "PHASE 1: MUTEX SYNCHRONIZED (SAFE MODE)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = SUCCESS
    p.space_after = Pt(12)

    m_stats = [
        ("Initial Tatkal Seats:", "2 Seats"),
        ("Simultaneous Teams Rush:", "10 Concurrent Teams"),
        ("Execution Latency:", "28 ms"),
        ("Successful Bookings:", "Exactly 2 Teams (Matched physical quota)"),
        ("Cleanly Rejected (409 SOLD_OUT):", "8 Teams (Clean rejection, no false hopes)"),
        ("Final Remaining Seats:", "0 (Perfect Invariant: S >= 0)"),
        ("Oversold Count:", "0 Tickets Oversold (100% Data Integrity)")
    ]
    for m_label, m_val in m_stats:
        p = mtf.add_paragraph()
        p.text = f"• {m_label} "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        run = p.add_run()
        run.text = m_val
        run.font.bold = False
        run.font.color.rgb = SUCCESS if "0" in m_val or "100%" in m_val else TEXT_MUTED
        p.space_after = Pt(6)

    u_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(5.0))
    u_card.fill.solid()
    u_card.fill.fore_color.rgb = DANGER_LIGHT
    u_card.line.color.rgb = DANGER
    u_card.line.width = Pt(2)
    utf = u_card.text_frame
    utf.word_wrap = True
    utf.margin_left = utf.margin_right = utf.margin_top = Inches(0.35)

    p = utf.paragraphs[0]
    p.text = "PHASE 2: MUTEX DISABLED (TOCTOU RACE MODE)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = DANGER
    p.space_after = Pt(12)

    u_stats = [
        ("Initial Tatkal Seats:", "2 Seats"),
        ("Simultaneous Teams Rush:", "10 Concurrent Teams"),
        ("Execution Latency:", "42 ms"),
        ("Bookings Processed:", "10 Confirmed (All passed due to dirty reads!)"),
        ("Rejected Count:", "0 Teams (Check-then-act vulnerability!)"),
        ("Final Remaining Seats:", "-8 (CRITICAL OVERSELLING ANOMALY)"),
        ("Physical Venue Violation:", "8 Phantom Teams booked without physical capacity!")
    ]
    for u_label, u_val in u_stats:
        p = utf.add_paragraph()
        p.text = f"• {u_label} "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        run = p.add_run()
        run.text = u_val
        run.font.bold = False
        run.font.color.rgb = DANGER if "-8" in u_val or "Phantom" in u_val else TEXT_MUTED
        p.space_after = Pt(6)

    # ────────────────────────────────────────────────────────────────
    # SLIDE 10: SYNCHRONIZATION PRIMITIVES COMPARISON
    # ────────────────────────────────────────────────────────────────
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Comparative Analysis", "Mutex vs. Semaphore vs. Distributed Locks",
               "Evaluating synchronization primitives across different architectural tiers.")

    tb_c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(11.733), Inches(5.1))
    tb_c.fill.solid()
    tb_c.fill.fore_color.rgb = CARD_BG
    tb_c.line.color.rgb = CARD_BORDER

    rows, cols = 6, 4
    left, top, width, height = Inches(1.1), Inches(2.1), Inches(11.133), Inches(4.5)
    tbl = s10.shapes.add_table(rows, cols, left, top, width, height).table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(3.0)
    tbl.columns[2].width = Inches(3.0)
    tbl.columns[3].width = Inches(2.933)

    hdrs = ["Attribute", "Mutex (Used in Project)", "Binary Semaphore", "Distributed Lock (e.g. Redis)"]
    for c_idx, h_text in enumerate(hdrs):
        cell = tbl.cell(0, c_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.size = Pt(11)
            p.alignment = PP_ALIGN.CENTER

    comp_data = [
        ("Ownership", "Enforced: Only locking thread can unlock", "No ownership: Any thread can signal()", "Token-based: Caller holds unique random secret"),
        ("Primary Purpose", "Mutual exclusion for critical section", "Signaling & inter-thread coordination", "Cross-server cluster serialization"),
        ("Starvation Prevention", "Guaranteed via FIFO Wait Queue", "Dependent on OS semaphore wait queue", "Dependent on TTL & lease renewal algorithms"),
        ("Scope / Boundary", "Single OS Process / RAM Address Space", "Single OS Process / Kernel Space", "Multi-server distributed microservices"),
        ("Failure Recovery", "Automatic via try...finally block", "Manual signal() invocation required", "TTL (Time-To-Live) auto-expiration on crash")
    ]
    for r_idx, row in enumerate(comp_data, start=1):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 0 else RGBColor(255, 255, 255)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.name = "Segoe UI"
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = PRIMARY_DARK
                else:
                    p.font.color.rgb = TEXT_DARK

    # ────────────────────────────────────────────────────────────────
    # SLIDE 11: VIVA VOCE DEFENSE & EXAMINER QUESTIONS
    # ────────────────────────────────────────────────────────────────
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Viva Voce Preparation", "Key Defense Questions & Rigorous Technical Answers",
               "High-yield questions professors and evaluators frequently ask during project defense.")

    viva_qas = [
        ("Q: Why must duplicate checking and seat deduction happen INSIDE the critical section?",
         "A: If duplicate verification occurred outside the lock, two simultaneous requests from the same user would both see 'not registered' before either commits, leading to double-booking. Placing it inside the mutex guarantees serial read-then-insert atomicity."),
        ("Q: How does our Tatkal implementation prevent Deadlocks?",
         "A: It breaks the Coffman conditions: (1) No 'Hold and Wait' because threads only request a single lock per event, never holding Lock A while waiting for Lock B. (2) Guaranteed release via try...finally prevents orphaned locks even if an exception occurs."),
        ("Q: What underlying hardware CPU primitives make Mutex locks possible?",
         "A: Modern CPUs provide atomic read-modify-write instructions: Test-and-Set (TAS), Compare-and-Swap (CAS, e.g., cmpxchg on x86), and Load-Linked / Store-Conditional (LL/SC) on ARM/RISC-V architectures."),
        ("Q: How would you scale this to a 5-node distributed microservices cluster?",
         "A: Transition from in-memory Mutex to a Distributed Lock Manager (DLM) using Redis Redlock or database row-level locking (PostgreSQL 'SELECT ... FOR UPDATE') inside an ACID transaction.")
    ]

    for i, (q, a) in enumerate(viva_qas):
        cy = Inches(1.85 + i * 1.3)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), cy, Inches(11.733), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = PRIMARY
        card.line.width = Pt(1.2)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.3)
        ctf.margin_top = Inches(0.12)

        p = ctf.paragraphs[0]
        p.text = q
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = PRIMARY

        p = ctf.add_paragraph()
        p.text = a
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(3)

    # ────────────────────────────────────────────────────────────────
    # SLIDE 12: CONCLUSION & LIVE EVALUATOR LINKS
    # ────────────────────────────────────────────────────────────────
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Summary & Live Evaluation", "Project Conclusion & Live System Navigation",
               "Full-stack production deployment ready for immediate live demonstration.")

    card_main = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.733), Inches(5.0))
    card_main.fill.solid()
    card_main.fill.fore_color.rgb = CARD_BG
    card_main.line.color.rgb = PRIMARY
    card_main.line.width = Pt(1.5)
    ctf = card_main.text_frame
    ctf.word_wrap = True
    ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.4)

    p = ctf.paragraphs[0]
    p.text = "KEY TAKEAWAYS & PROJECT ACCOMPLISHMENTS"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    conclusions = [
        ("Rigorous OS Concurrency:", "Proved why unsynchronized check-then-act operations cause severe data corruption (-8 seats) and demonstrated 100% prevention using an asynchronous Mutex."),
        ("Dijkstra's Criteria Satisfied:", "Guaranteed Mutual Exclusion, Progress, and Bounded Waiting via a clean FIFO queue."),
        ("Enterprise 3-Tier Dashboards:", "Delivered dedicated dashboards for Platform Admin (Razorpay Test Mode credentials), Hackathon Organizers, and Participants."),
        ("Zero-Dependency Reliability:", "Built on native Node.js core modules with zero external package bloat, instant startup, and persistent transaction storage.")
    ]
    for c_title, c_desc in conclusions:
        p = ctf.add_paragraph()
        p.text = f"✔ {c_title} "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_DARK
        run = p.add_run()
        run.text = c_desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    p = ctf.add_paragraph()
    p.text = "LIVE SYSTEM ACCESS PORTALS:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = SECONDARY
    p.space_before = Pt(10)
    p.space_after = Pt(4)

    p = ctf.add_paragraph()
    p.text = "• User Booking Portal:      http://localhost:3000/#user\n• Tatkal Concurrency Studio: http://localhost:3000/#concurrency\n• Hackathon Admin Console:   http://localhost:3000/#hackadmin\n• Platform Admin Settings:   http://localhost:3000/#platform\n• Viva & OS Theory Center:   http://localhost:3000/#viva"
    p.font.size = Pt(10.5)
    p.font.name = "Consolas"
    p.font.color.rgb = PRIMARY_DARK

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "SyncReg_OS_Product8_Presentation.pptx"
    create_deck(out)
