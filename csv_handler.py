import csv
import os
import shutil
from datetime import datetime

# Reporting layer for readable per-test evidence and the suite-wide status summary.
screenshot_index = 1
_screenshot_map = {}

# Mirrors a test ID such as TC01_a_a as TC01/TC01_a/TC01_a_a in the results folder.
def _get_nested_path(base_name, root_dir):
    parts = base_name.split('_')
    nested = [parts[0]]
    for i in range(1, len(parts)):
        nested.append('_'.join(parts[:i+1]))
    return os.path.join(root_dir, *nested)

# Rebuilds one test report from the shared outcome data and links any captured failure screenshot.
def append_to_csv(data_dict, filename, screenshot_path=None):
    global screenshot_index, _screenshot_map

    base_name = filename.replace('.csv', '')
    project_root = os.path.dirname(os.path.abspath(__file__))
    test_results_root = os.path.join(project_root, "Test_Results")

    full_path = _get_nested_path(base_name, test_results_root)
    screenshots_folder = os.path.join(full_path, "screenshots")
    filepath = os.path.join(full_path, filename)

    os.makedirs(full_path, exist_ok=True)
    os.makedirs(screenshots_folder, exist_ok=True)

    recent_page = list(data_dict.keys())[-1] if data_dict else None

    # Associate the screenshot with the most recent failed checkpoint before writing the report.
    if screenshot_path and os.path.exists(screenshot_path) and recent_page:
        screenshot_name = f"screenshot_{screenshot_index}.png"
        _screenshot_map[recent_page] = screenshot_name
        screenshot_index += 1
        dest_path = os.path.join(screenshots_folder, screenshot_name)
        shutil.move(screenshot_path, dest_path)
        print("Screenshot moved to:", dest_path)

    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Page', 'Start Timestamp', 'End Timestamp', 'Load Time', 'Status', 'Error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for page, result in data_dict.items():
            err = result.get("error", "")
            if "driver unreachable" in err.lower():
                err = "Button not found"
            if err and page in _screenshot_map:
                err = f"{err} - {_screenshot_map[page]}"
            row = {
                "Page": page,
                "Start Timestamp": "'" + result.get("start_time", ""),
                "End Timestamp": "'" + result.get("end_time", ""),
                "Load Time": result.get("load_time", ""),
                "Status": result.get("status", ""),
                "Error": err
            }
            writer.writerow(row)

# Updates one test case in the aggregate summary without discarding results from other cases.
def update_summary_csv(test_case_name, status):
    summary_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Test_Results", "test_summary.csv")
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)

    rows = []
    found = False

    if os.path.exists(summary_file):
        with open(summary_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            if row["Test Cases"] == test_case_name:
                row["Status"] = status
                found = True
                break

    if not found:
        rows.append({"Test Cases": test_case_name, "Status": status})

    with open(summary_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Test Cases", "Status"])
        writer.writeheader()
        writer.writerows(rows)
