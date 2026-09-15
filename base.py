import time
import sys
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from csv_handler import append_to_csv, update_summary_csv
from xray_uploader import upload_result

# Shared execution and validation layer used by every end-to-end test flow.
# Test scripts describe the journey; this module performs each check and records its evidence.
Final_Outcome = {}
test_failed = False
driver = None
file = None

# Registers the active browser session and report name before a test begins.
def driver_update(self, csv_file):
    global driver, file
    driver = self
    file = csv_file

# Finalizes a successful run by writing its CSV evidence and publishing the result to Xray.
def csv_input(csv_file_name):
    if test_failed:
        print("Skipped csv_input, test already failed")
        return

    append_to_csv(Final_Outcome, csv_file_name)
    test_case_name = os.path.basename(csv_file_name).replace('.csv', '')

    lines = [f"Test: {test_case_name} (PASSED)"]
    for page, result in Final_Outcome.items():
        line = f"- {page}: {result['status'].upper()}"
        if result["status"].lower() == "pass":
            line += f" (Load Time: {result.get('load_time', '')}s)"
        else:
            line += f"\n  Error: {result.get('error', '')}"
        lines.append(line)

    comment = "\n".join(lines)
    upload_result(test_case_name, "PASSED", comment)

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def take_temp_screenshot():
    ts = int(time.time())
    name = f"temp_{ts}.png"
    try:
        driver.save_screenshot(name)
        print("Screenshot saved as:", name)
        return name
    except Exception as e:
        print("Screenshot failed:", e)
        return None

# Keeps every failure path consistent: capture evidence, update reports, close the browser, and stop.
def fail_and_exit(page, error_msg):
    start = time.time()
    Final_Outcome[page] = {
        "status": "Fail",
        "load_time": "",
        "start_time": datetime.fromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "end_time": current_timestamp(),
        "error": error_msg
    }

    print(page, "-", error_msg)
    screenshot_path = take_temp_screenshot()
    append_to_csv(Final_Outcome, file, screenshot_path=screenshot_path)

    test_case_name = os.path.basename(file).replace('.csv', '')
    update_summary_csv(test_case_name, "Fail")

    lines = [f"Test: {test_case_name} (FAILED)"]
    for p, result in Final_Outcome.items():
        line = f"- {p}: {result['status'].upper()}"
        if result["status"].lower() == "pass":
            line += f" (Load Time: {result.get('load_time', '')}s)"
        else:
            line += f"\n  Error: {result.get('error', '')}"
        lines.append(line)
    comment = "\n".join(lines)

    try:
        upload_result(test_case_name, "FAILED", comment)
    except Exception as e:
        print("Failed to upload to Xray:", e)

    try:
        driver.quit()
    except:
        pass

    sys.exit(1)

# Polls for delayed UI elements so normal page-load timing does not immediately fail a test.
def wait_for_element(xpath, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            return driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            time.sleep(0.5)
        except Exception as e:
            print("Driver unreachable:", e)
            break
    return None

# Core checkpoint used throughout the suite: optionally click an element, then validate the destination.
# Passing 0 for either XPath makes the same helper usable for click-only or check-only steps.
def SafeStep(xpath_btn, xpath_header, page, header_check, timeout=30):
    global test_failed
    if xpath_btn != 0:
        time.sleep(2)
        btn = wait_for_element(xpath_btn, timeout)
        if not btn:
            test_failed = True
            fail_and_exit(page, f"Button not found or driver unreachable: {xpath_btn}")
            return

        click_start = time.time()
        while time.time() - click_start < timeout:
            try:
                driver.execute_script("arguments[0].scrollIntoView()", btn)
                print("Clicking button on:", page)
                btn.click()
                break
            except Exception:
                time.sleep(0.5)
        else:
            test_failed = True
            fail_and_exit(page, "Button not clickable")
            return

    if xpath_header != 0:
        start_time = time.time()
        matched = False
        actual_text = ""

        # A checkpoint passes only when the visible heading exactly matches the expected test copy.
        while time.time() - start_time < timeout:
            try:
                element = driver.find_element(By.XPATH, xpath_header)
                actual_text = element.text.strip()
                if actual_text == header_check:
                    matched = True
                    break
            except NoSuchElementException:
                pass
            except Exception as e:
                test_failed = True
                fail_and_exit(page, "Driver error during header check")
                return
            time.sleep(0.5)

        test_case_name = os.path.basename(file).replace('.csv', '')

        # Store timing and status here so CSV and Xray reports share the same source of truth.
        if matched:
            load_time = round(time.time() - start_time, 2)
            Final_Outcome[page] = {
                "status": "Pass",
                "load_time": load_time,
                "start_time": datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "end_time": current_timestamp(),
                "error": ""
            }
            print(page, "- Loaded in", load_time, "s")
            update_summary_csv(test_case_name, "Pass")
        else:
            if actual_text == "":
                test_failed = True
                fail_and_exit(page, f"Header not found | Expected: '{header_check}'")
                return

            error_msg = f"Header mismatch (Found: '{actual_text}' | Expected: '{header_check}')"
            screenshot_path = take_temp_screenshot()
            Final_Outcome[page] = {
                "status": "Fail",
                "load_time": "",
                "start_time": datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "end_time": current_timestamp(),
                "error": error_msg
            }
            append_to_csv(Final_Outcome, file, screenshot_path=screenshot_path)
            print(page, "-", error_msg, "| Expected:", header_check)
            update_summary_csv(test_case_name, "Fail")
