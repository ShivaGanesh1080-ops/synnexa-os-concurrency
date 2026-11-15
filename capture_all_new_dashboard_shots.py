# -*- coding: utf-8 -*-
"""
Capture all fresh dashboard screenshots using Playwright with domcontentloaded
"""

import os
from playwright.sync_api import sync_playwright

os.makedirs("public/screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1280, "height": 840}, device_scale_factor=1.5)
    page = context.new_page()

    # 1. Main Landing Portal
    page.goto("https://synnexa.vercel.app", wait_until="load", timeout=20000)
    page.wait_for_timeout(1500)
    page.screenshot(path="public/screenshots/shot_landing.png")
    print("Captured shot_landing.png")

    # 2. Open Boarding Pass Modal
    page.evaluate("""() => {
        if (typeof window.renderBoardingPass === 'function') {
            window.renderBoardingPass({
                ticket_code: 'TKT-TATKAL-89211',
                team_name: 'AlphaKernels',
                leader_name: 'A. Shiva Ganesh',
                members: ['Ch. Naveen Reddy', 'K. Shiva Saketh', 'V. Saicharan', 'T. Geethika', 'G. Vishwas'],
                payment_id: 'rzp_pay_90281491'
            }, {
                title: 'Global AI HackSphere 2026',
                venue: 'Moscone Center, San Francisco & Virtual Hub',
                dates: 'Nov 24–26, 2026'
            });
        }
    }""")
    page.wait_for_timeout(600)
    page.screenshot(path="public/screenshots/shot_boarding_pass.png")
    print("Captured shot_boarding_pass.png")

    # 3. Open Refund Reassurance Modal
    page.evaluate("""() => {
        if (typeof window.closePassModal === 'function') window.closePassModal();
        if (typeof window.openRefundNoticeModal === 'function') {
            window.openRefundNoticeModal({
                event: { title: 'Global AI HackSphere 2026' },
                team_name: 'ByteBusters',
                amount: 499,
                ref_id: 'RZP-REF-849204'
            });
        }
    }""")
    page.wait_for_timeout(600)
    page.screenshot(path="public/screenshots/shot_refund_modal.png")
    print("Captured shot_refund_modal.png")

    # 4. Admin Portal & Live 2-Device Station
    page.goto("https://synnexa.vercel.app/admin", wait_until="load", timeout=20000)
    page.wait_for_timeout(1500)
    page.screenshot(path="public/screenshots/shot_admin.png")
    print("Captured shot_admin.png")

    # 5. Concurrency Studio
    page.goto("https://synnexa.vercel.app/studio", wait_until="load", timeout=20000)
    page.wait_for_timeout(1500)
    page.screenshot(path="public/screenshots/shot_studio.png")
    print("Captured shot_studio.png")

    browser.close()

print("All screenshots captured successfully!")
