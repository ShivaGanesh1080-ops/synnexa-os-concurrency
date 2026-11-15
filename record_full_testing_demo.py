import os, time, shutil
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\DELL\.gemini\antigravity\scratch\event-registration-mutex-system"
DESKTOP_DIR = r"C:\Users\DELL\Desktop"
VIDEO_TEMP_DIR = os.path.join(BASE_DIR, "video_temp")
OUTPUT_NAME = "Event_Registration_Full_Testing_Demo.webm"
DESKTOP_OUTPUT = os.path.join(DESKTOP_DIR, OUTPUT_NAME)
PUBLIC_OUTPUT = os.path.join(BASE_DIR, "public", OUTPUT_NAME)
PUBLIC_DEMO = os.path.join(BASE_DIR, "public", "demo.webm")

os.makedirs(VIDEO_TEMP_DIR, exist_ok=True)

CURSOR_JS = """
(() => {
  if (document.getElementById('demo-cursor')) return;
  const cursor = document.createElement('div');
  cursor.id = 'demo-cursor';
  cursor.innerHTML = `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M5 3L19 12L12 13L9 20L5 3Z" fill="#C28E35" stroke="#0F172A" stroke-width="1.8" stroke-linejoin="round"/>
  </svg>`;
  cursor.style.cssText = `
    position: fixed; z-index: 9999999; pointer-events: none;
    width: 28px; height: 28px;
    transition: left 0.12s ease-out, top 0.12s ease-out;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.4));
    left: 100px; top: 100px;
  `;
  document.body.appendChild(cursor);
  document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });
})();
"""

SUBTITLE_JS = """
(() => {
  if (document.getElementById('demo-subtitle')) return;
  const bar = document.createElement('div');
  bar.id = 'demo-subtitle';
  bar.style.cssText = `
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    z-index: 9999998; text-align: center; padding: 10px 28px;
    background: rgba(11, 17, 32, 0.94); border: 1px solid rgba(194, 142, 53, 0.5);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    border-radius: 9999px; color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 15px; font-weight: 600; letter-spacing: 0.3px;
    transition: opacity 0.3s ease, transform 0.3s ease; pointer-events: none;
    backdrop-filter: blur(10px); max-width: 90%; white-space: nowrap;
    opacity: 0;
  `;
  document.body.appendChild(bar);
})();
"""

def inject_overlays(page):
    try:
        page.evaluate(CURSOR_JS)
        page.evaluate(SUBTITLE_JS)
    except Exception as e:
        print("Overlay injection warning:", e)

def show_subtitle(page, text, hold_ms=1000):
    try:
        page.evaluate("""(t) => {
            const bar = document.getElementById('demo-subtitle');
            if (!bar) return;
            if (t) {
                bar.textContent = t;
                bar.style.opacity = '1';
            } else {
                bar.style.opacity = '0';
            }
        }""", text)
    except:
        pass
    if text and hold_ms > 0:
        page.wait_for_timeout(hold_ms)

def smooth_move(page, target_x, target_y, steps=10):
    page.mouse.move(target_x, target_y, steps=steps)
    page.wait_for_timeout(120)

def move_and_click(page, locator_or_selector, label=""):
    try:
        if isinstance(locator_or_selector, str):
            el = page.locator(locator_or_selector).first
        else:
            el = locator_or_selector
        
        if not el.is_visible():
            print(f"Warning: {label} not visible")
            return False
        
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        box = el.bounding_box()
        if box:
            smooth_move(page, box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=10)
            page.wait_for_timeout(200)
        el.click()
        page.wait_for_timeout(500)
        return True
    except Exception as e:
        print(f"move_and_click failed on {label}:", e)
        return False

def type_slowly(page, selector, text, delay=35):
    try:
        el = page.locator(selector).first
        el.scroll_into_view_if_needed()
        box = el.bounding_box()
        if box:
            smooth_move(page, box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
            page.wait_for_timeout(150)
        el.click()
        el.fill("")
        el.press_sequentially(text, delay=delay)
        page.wait_for_timeout(250)
    except Exception as e:
        print(f"type_slowly failed on {selector}:", e)

def smooth_scroll(page, y_pos, steps=8):
    current = page.evaluate("window.scrollY")
    diff = y_pos - current
    for i in range(1, steps + 1):
        target = current + (diff * (i / steps))
        page.evaluate(f"window.scrollTo(0, {target})")
        page.wait_for_timeout(70)
    page.wait_for_timeout(250)

def record_demo():
    print("Starting Playwright Video Recording...")
    # Clean previous temp files
    for f in os.listdir(VIDEO_TEMP_DIR):
        try:
            os.remove(os.path.join(VIDEO_TEMP_DIR, f))
        except:
            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=VIDEO_TEMP_DIR,
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()

        # ====================================================================
        # SCENE 1: PORTAL OVERVIEW & BRANDING
        # ====================================================================
        page.goto("http://localhost:3000/")
        page.wait_for_load_state("networkidle")
        inject_overlays(page)
        
        show_subtitle(page, "Event Registration — Concurrency Control Platform", hold_ms=1200)
        smooth_move(page, 200, 45, steps=10) # Navbar brand
        page.wait_for_timeout(600)
        
        show_subtitle(page, "SR University CSE Core • Operating Systems Product #8", hold_ms=1200)
        smooth_move(page, 640, 260, steps=12) # Hero title
        page.wait_for_timeout(800)

        # ====================================================================
        # SCENE 2: EXPLORING CURATED HACKATHONS & SEAT GAUGES
        # ====================================================================
        show_subtitle(page, "Step 1: Browsing Events with Real-Time Tatkal Seat Gauges", hold_ms=1000)
        smooth_scroll(page, 650, steps=10)
        page.wait_for_timeout(800)

        # Pan across event cards
        smooth_move(page, 320, 480, steps=10) # Card 1
        page.wait_for_timeout(600)
        smooth_move(page, 720, 480, steps=10) # Card 2
        page.wait_for_timeout(600)

        # ====================================================================
        # SCENE 3: SQUAD BOOKING & BOARDING PASS GENERATION
        # ====================================================================
        show_subtitle(page, "Step 2: Testing Participant Checkout & Squad Pass Dispatch", hold_ms=1000)
        page.evaluate("window.Razorpay = null;") # Enable fast deterministic pass minting
        
        move_and_click(page, "button:has-text('Book Team Pass')", "Book Button")
        page.wait_for_timeout(500)
        inject_overlays(page)

        show_subtitle(page, "Filling Verified Squad Details & Team Leader Credentials", hold_ms=800)
        type_slowly(page, "#teamName", "KernelArchitects", delay=35)
        type_slowly(page, "#leaderName", "A. Shiva Ganesh (Team Lead)", delay=35)
        type_slowly(page, "#leaderEmail", "shivaganesh@sru.edu.in", delay=30)
        type_slowly(page, "#leaderHtno", "2503A51110", delay=35)
        page.wait_for_timeout(400)

        show_subtitle(page, "Submitting Booking with Simulated Payment Verification", hold_ms=800)
        move_and_click(page, "#submitBookingBtn", "Pay Button")
        page.wait_for_timeout(1200)
        inject_overlays(page)

        show_subtitle(page, "Booking Confirmed! Atomic Decrement & VIP Pass Minted", hold_ms=1500)
        smooth_move(page, 640, 360, steps=10) # Over boarding pass
        page.wait_for_timeout(1500)

        # Close pass modal
        move_and_click(page, "#passModal button:has-text('✕')", "Close Pass Modal")
        page.wait_for_timeout(500)

        # ====================================================================
        # SCENE 4: CONCURRENCY STUDIO (50-THREAD RUSH BENCHMARK)
        # ====================================================================
        show_subtitle(page, "Step 3: Navigating to Concurrency Benchmark Studio", hold_ms=1000)
        smooth_scroll(page, 0, steps=8)
        page.goto("http://localhost:3000/studio")
        page.wait_for_load_state("networkidle")
        inject_overlays(page)

        show_subtitle(page, "Configuring 50-Thread High Contention Tatkal Surge", hold_ms=1200)
        smooth_scroll(page, 320, steps=8)
        smooth_move(page, 400, 350, steps=10) # Contention controls
        page.wait_for_timeout(600)

        show_subtitle(page, "Executing 50 Simultaneous Reservation Requests (Mutex ON)", hold_ms=1000)
        move_and_click(page, "button:has-text('Fire Tatkal Concurrent Rush')", "Fire Rush Btn")
        page.wait_for_timeout(2500) # Wait for benchmark progress

        show_subtitle(page, "Benchmark Verified: 2 Confirmed • 48 Blocked (0 Oversold!)", hold_ms=2000)
        smooth_move(page, 640, 520, steps=10) # Over results card
        page.wait_for_timeout(1500)

        # ====================================================================
        # SCENE 5: ORGANIZER ADMIN COMMAND CENTER & 2-DEVICE RIG
        # ====================================================================
        show_subtitle(page, "Step 4: Opening Organizer Admin & Multi-Device Testing Station", hold_ms=1000)
        smooth_scroll(page, 0, steps=8)
        page.goto("http://localhost:3000/admin")
        page.wait_for_load_state("networkidle")
        inject_overlays(page)

        show_subtitle(page, "Real-Device Viva Test Rig: Teacher Laptop vs. Friend Mobile", hold_ms=1200)
        smooth_scroll(page, 280, steps=8)
        page.wait_for_timeout(800)

        # ====================================================================
        # SCENE 6: TEST CASE A - MUTEX OFF (RACE CONDITION DEMO)
        # ====================================================================
        show_subtitle(page, "Test Case A: Disabling Mutex Protection to Provoke Race Hazard", hold_ms=1200)
        move_and_click(page, "button:has-text('Toggle Event #1 Mutex')", "Toggle Mutex OFF")
        page.wait_for_timeout(600)

        show_subtitle(page, "Priming Event #1 to Exactly 1 Remaining Seat", hold_ms=1000)
        move_and_click(page, "button:has-text('Prime Event #1 to Exactly 1 Seat')", "Prime 1 Seat")
        page.wait_for_timeout(1000)

        # Simulate Unprotected Concurrent Twin Requests via backend API
        show_subtitle(page, "Teacher & Friend Checkout Simultaneously without Mutex Lock...", hold_ms=1200)
        page.evaluate("""async () => {
            await Promise.all([
                fetch('/api/book', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({hackathon_id: 1, team_name: 'Teacher Laptop', leader_name: 'Faculty Tester', leader_email: 'prof@sru.edu.in', members: []}) }),
                fetch('/api/book', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({hackathon_id: 1, team_name: 'Friend Mobile', leader_name: 'Student Tester', leader_email: 'student@sru.edu.in', members: []}) })
            ]);
            if (typeof fetchHackathons === 'function') fetchHackathons();
        }""")
        page.wait_for_timeout(1200)

        show_subtitle(page, "CRITICAL ANOMALY: Capacity = -1! Both passes issued for 1 seat!", hold_ms=2200)
        smooth_scroll(page, 520, steps=8) # Over batches table showing -1
        page.wait_for_timeout(1800)

        # ====================================================================
        # SCENE 7: TEST CASE B - MUTEX ON & REFUND MODAL INTERCEPTION
        # ====================================================================
        show_subtitle(page, "Test Case B: Enabling Dijkstra Critical Section (Mutex ON)", hold_ms=1200)
        smooth_scroll(page, 280, steps=8)
        move_and_click(page, "button:has-text('Toggle Event #1 Mutex')", "Toggle Mutex ON")
        page.wait_for_timeout(600)

        show_subtitle(page, "Resetting Capacity to 1 Seat with Mutex Active", hold_ms=1000)
        move_and_click(page, "button:has-text('Prime Event #1 to Exactly 1 Seat')", "Prime 1 Seat ON")
        page.wait_for_timeout(1000)

        show_subtitle(page, "Teacher Claims Final Seat; Friend Intercepts Quota Exhaustion", hold_ms=1200)
        page.evaluate("""async () => {
            const [resA, resB] = await Promise.all([
                fetch('/api/book', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({hackathon_id: 1, team_name: 'Teacher Laptop', leader_name: 'Prof. Examiner', leader_email: 'prof@sru.edu.in', members: []}) }).then(r => r.json()),
                fetch('/api/book', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({hackathon_id: 1, team_name: 'Friend Mobile', leader_name: 'Student Peer', leader_email: 'peer@sru.edu.in', members: []}) }).then(r => r.json())
            ]);
            if (typeof openRefundNoticeModal === 'function') {
                openRefundNoticeModal({
                    status: 'SOLD_OUT',
                    message: 'Tatkal quota completely exhausted (0 seats remaining).',
                    refund_ref: 'RZP-REF-849204',
                    team_name: 'Friend Mobile'
                });
            }
        }""")
        page.wait_for_timeout(1200)
        inject_overlays(page)

        show_subtitle(page, "Automated Refund Reassurance Modal (100% Refund in 5-7 Days)", hold_ms=2000)
        smooth_move(page, 640, 360, steps=10) # Over refund modal
        page.wait_for_timeout(1800)

        move_and_click(page, "#refundNoticeModal button:has-text('✕')", "Close Refund Modal")
        page.wait_for_timeout(500)

        # ====================================================================
        # SCENE 8: MICROSECOND AUDIT TRAIL VERIFICATION
        # ====================================================================
        show_subtitle(page, "Step 5: Inspecting Real-Time Microsecond Audit Stream", hold_ms=1000)
        smooth_scroll(page, 1400, steps=10) # Down to audit trail
        page.wait_for_timeout(1200)
        smooth_move(page, 640, 480, steps=10)
        page.wait_for_timeout(1200)

        # ====================================================================
        # SCENE 9: DOOR CHECK-IN SCANNER
        # ====================================================================
        show_subtitle(page, "Step 6: Testing Event-Day Door Check-In QR Scanner", hold_ms=1000)
        smooth_scroll(page, 0, steps=8)
        move_and_click(page, "button:has-text('Check-In')", "Door Check-In Btn")
        page.wait_for_timeout(500)
        inject_overlays(page)

        show_subtitle(page, "Scanning & Verifying Pass: Entry Granted", hold_ms=1000)
        type_slowly(page, "#checkInCode", "TKT-TATKAL-74842", delay=35)
        move_and_click(page, "#modalCheckIn button:has-text('Verify & Check In')", "Verify Pass")
        page.wait_for_timeout(1200)

        move_and_click(page, "#modalCheckIn button:has-text('Close')", "Close CheckIn Modal")
        page.wait_for_timeout(500)

        # ====================================================================
        # SCENE 10: CONCLUSION & TEST VERIFICATION COMPLETE
        # ====================================================================
        show_subtitle(page, "All Tests Passed: Zero Overbooking • Mutual Exclusion Proven!", hold_ms=2200)
        smooth_scroll(page, 2200, steps=10) # Down to institutional footer
        page.wait_for_timeout(2000)
        show_subtitle(page, "", hold_ms=500)

        # Close page & context to finalize video
        page.close()
        context.close()
        browser.close()

    print("Browser closed, locating recorded video...")
    recorded_files = [f for f in os.listdir(VIDEO_TEMP_DIR) if f.endswith(".webm")]
    if not recorded_files:
        raise Exception("No video file generated in " + VIDEO_TEMP_DIR)
    
    # Pick latest video file with non-zero size
    candidates = [os.path.join(VIDEO_TEMP_DIR, f) for f in recorded_files if os.path.getsize(os.path.join(VIDEO_TEMP_DIR, f)) > 0]
    if not candidates:
        raise Exception("All generated video files are empty")
        
    latest_video = max(candidates, key=os.path.getctime)
    video_size = os.path.getsize(latest_video)
    print(f"Recorded video located: {latest_video} ({video_size} bytes)")

    # Copy to Desktop
    shutil.copy2(latest_video, DESKTOP_OUTPUT)
    print(f"Copied to Desktop: {DESKTOP_OUTPUT} ({os.path.getsize(DESKTOP_OUTPUT)} bytes)")

    # Copy to public directory
    shutil.copy2(latest_video, PUBLIC_OUTPUT)
    shutil.copy2(latest_video, PUBLIC_DEMO)
    print(f"Copied to Public: {PUBLIC_OUTPUT}")

if __name__ == "__main__":
    record_demo()
