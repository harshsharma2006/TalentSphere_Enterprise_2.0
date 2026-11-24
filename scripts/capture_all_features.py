"""
TalentSphere Enterprise 2.0 - Automated Feature Screenshot Capture
Captures high-resolution screenshots of all working features across personas.
"""

import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path(r"C:\Users\Harsh Sharma\OneDrive\Music\Desktop\TalentSphere_Enterprise_2.0\docs\screenshots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

APP_URL = "http://localhost:8501"

def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print(f"Opening {APP_URL}...")
        page.goto(APP_URL, wait_until="networkidle", timeout=30000)
        time.sleep(3)

        # 1. Login Page
        print("Capturing 01_login_page.png...")
        page.screenshot(path=str(OUTPUT_DIR / "01_login_page.png"), full_page=False)

        # Login as Super Admin
        print("Logging in as Super Admin...")
        page.locator("input[type='text']").first.fill("superadmin")
        page.locator("input[type='password']").first.fill("SuperAdmin@2026")
        page.locator("button:has-text('Sign In to Workspace')").click()
        time.sleep(4)

        # 2. Super Admin Command Center
        print("Capturing 02_superadmin_dashboard.png...")
        page.screenshot(path=str(OUTPUT_DIR / "02_superadmin_dashboard.png"), full_page=False)

        def nav_click(label_text):
            print(f"Navigating to {label_text}...")
            page.locator(f"section[data-testid='stSidebar'] label:has-text('{label_text}')").click()
            time.sleep(3)

        # 3. Workforce Directory
        nav_click("Workforce Directory")
        print("Capturing 03_workforce_directory.png...")
        page.screenshot(path=str(OUTPUT_DIR / "03_workforce_directory.png"), full_page=False)

        # 4. Recruitment & Jobs
        nav_click("Recruitment & Jobs")
        print("Capturing 04_recruitment_jobs.png...")
        page.screenshot(path=str(OUTPUT_DIR / "04_recruitment_jobs.png"), full_page=False)

        # 5. Resume & ATS AI
        nav_click("Resume & ATS AI")
        try:
            diag_btn = page.locator("button:has-text('Run ATS Score & Competency Diagnostic')")
            if diag_btn.is_visible():
                diag_btn.click()
                time.sleep(3)
        except Exception as e:
            print(f"Diagnostic button: {e}")
        print("Capturing 05_resume_ats_analyzer.png...")
        page.screenshot(path=str(OUTPUT_DIR / "05_resume_ats_analyzer.png"), full_page=False)

        # 6. Performance Reviews
        nav_click("Performance Reviews")
        print("Capturing 06_performance_reviews.png...")
        page.screenshot(path=str(OUTPUT_DIR / "06_performance_reviews.png"), full_page=False)

        # 7. Learning Academy
        nav_click("Learning Academy")
        print("Capturing 07_learning_academy.png...")
        page.screenshot(path=str(OUTPUT_DIR / "07_learning_academy.png"), full_page=False)

        # 8. Career Pathways
        nav_click("Career Pathways")
        print("Capturing 08_career_pathways.png...")
        page.screenshot(path=str(OUTPUT_DIR / "08_career_pathways.png"), full_page=False)

        # 9. Sign Out & Login as Employee
        print("Signing out to capture Employee persona...")
        page.locator("button:has-text('Sign Out')").click()
        time.sleep(3)

        page.locator("input[type='text']").first.fill("john_employee")
        page.locator("input[type='password']").first.fill("Employee@2026")
        page.locator("button:has-text('Sign In to Workspace')").click()
        time.sleep(4)

        print("Capturing 09_employee_self_service.png...")
        page.screenshot(path=str(OUTPUT_DIR / "09_employee_self_service.png"), full_page=False)

        # 10. Sign Out & Login as College Student
        print("Signing out to capture College Student persona...")
        page.locator("button:has-text('Sign Out')").click()
        time.sleep(3)

        page.locator("input[type='text']").first.fill("alex_student")
        page.locator("input[type='password']").first.fill("Student@2026")
        page.locator("button:has-text('Sign In to Workspace')").click()
        time.sleep(4)

        print("Capturing 10_student_placement_portal.png...")
        page.screenshot(path=str(OUTPUT_DIR / "10_student_placement_portal.png"), full_page=False)

        browser.close()
        print("✅ SUCCESS: ALL 10 FEATURE SCREENSHOTS CAPTURED!")

if __name__ == "__main__":
    capture_all()
