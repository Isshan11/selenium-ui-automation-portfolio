# --- path shim (import base.py from nested folders) ---
import os, sys, time
cur = os.path.abspath(os.path.dirname(__file__))
while "base.py" not in os.listdir(cur):
    parent = os.path.dirname(cur)
    if parent == cur:
        raise FileNotFoundError("base.py not found while walking up")
    cur = parent
if cur not in sys.path:
    sys.path.insert(0, cur)
# --- end shim ---

import base
from base import current_timestamp
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

XPATH_HEADER = '//*[@id="vmo"]/div[1]/div[2]/div/div/div/div/div/div[1]/h2/span'
XPATH_MAP_INPUT = '//*[@id="map_search_box"]'
XPATH_CHECK_COVERAGE_BTN = '//*[@id="vmo-check-coverage-btn"]'

def _ts_ms(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def Automatic_map_coverage(self):
    page  = "Coverage Map - Search"
    start = time.time()
    try:
        # wait for input
        box = None
        for _ in range(24):
            try:
                el = self.find_element(By.XPATH, XPATH_MAP_INPUT)
                if el.is_displayed():
                    box = el
                    break
            except:
                time.sleep(0.5)
        if not box:
            base.Final_Outcome[page] = {
                "status": "Fail", "load_time": "",
                "start_time": _ts_ms(start),
                "end_time": current_timestamp(),
                "error": f"Input not found: {XPATH_MAP_INPUT}"
            }
            return

        # human typing + Enter (kept)
        actions = ActionChains(self).click(box)
        for ch in "design district":
            actions.send_keys(ch).pause(0.5)
        actions.send_keys(Keys.RETURN).perform()

        # small settle
        time.sleep(1)

        base.Final_Outcome[page] = {
            "status": "Pass",
            "load_time": round(time.time() - start, 2),
            "start_time": _ts_ms(start),
            "end_time": current_timestamp(),
            "error": ""
        }

    except Exception as e:
        base.Final_Outcome[page] = {
            "status": "Fail", "load_time": "",
            "start_time": _ts_ms(start),
            "end_time": current_timestamp(),
            "error": f"Exception: {e}"
        }
