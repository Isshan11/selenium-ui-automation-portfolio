import os, sys, time
cur = os.path.abspath(os.path.dirname(__file__))
while "base.py" not in os.listdir(cur):
    parent = os.path.dirname(cur)
    if parent == cur:
        raise FileNotFoundError("base.py not found while walking up")
    cur = parent
if cur not in sys.path:
    sys.path.insert(0, cur)


import base
from base import current_timestamp
from datetime import datetime

import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

XPATH_HEADER = '//*[@id="vmo-onboarding-page"]/div/div/div/div/div/div[2]/div[1]/div/h2/span[1]'
XPATH_MAP_INPUT = '//*[@id="map_search_box"]'
XPATH_MAP_OPTION1 = '//*[@id="map_search"]/div/div/div/div[1]/div/div/ul/li[1]'
XPATH_DELIVER_HERE_BTN = '//*[@id="vmo-onboarding-page"]/div/div/div/div/div/div[2]/div[2]/div[3]/button'

def _ts_ms(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def AutoMatic_Address_Map(self):
    page  = "Address Map - Search"
    start = time.time()
    try:
        # wait for input
        input_box = None
        for _ in range(24):
            try:
                el = self.find_element(By.XPATH, XPATH_MAP_INPUT)
                if el.is_displayed():
                    input_box = el
                    break
            except:
                time.sleep(0.5)
        if not input_box:
            base.Final_Outcome[page] = {
                "status": "Fail",
                "load_time": "",
                "start_time": _ts_ms(start),
                "end_time": current_timestamp(),
                "error": f"Input Box Not Found"
            }
            return

        # human typing
        actions = ActionChains(self)
        actions.click(input_box)
        for ch in "design ":
            actions.send_keys(ch).pause(0.5)
        actions.perform()

        # keep your Enter press
        ActionChains(self).send_keys(Keys.RETURN).perform()

        # wait for first option and click
        option = None
        for _ in range(24):
            try:
                el = self.find_element(By.XPATH, XPATH_MAP_OPTION1)
                if el.is_displayed():
                    option = el
                    break
            except:
                time.sleep(0.5)
        if not option:
            base.Final_Outcome[page] = {
                "status": "Fail",
                "load_time": "",
                "start_time": _ts_ms(start),
                "end_time": current_timestamp(),
                "error": f"Suggestion option not found."
            }
            return

        option.click()
        time.sleep(3)

        base.Final_Outcome[page] = {
            "status": "Pass",
            "load_time": round(time.time() - start, 2),
            "start_time": _ts_ms(start),
            "end_time": current_timestamp(),
            "error": ""
        }

    except Exception as e:
        base.Final_Outcome[page] = {
            "status": "Fail",
            "load_time": "",
            "start_time": _ts_ms(start),
            "end_time": current_timestamp(),
            "error": f"Exception: {e}"
        }
