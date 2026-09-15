import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import sys
import os

cur = os.path.abspath(os.path.dirname(__file__))
while "base.py" not in os.listdir(cur):
    cur = os.path.dirname(cur)
    if cur == os.path.dirname(cur): raise FileNotFoundError("base.py not found.")
sys.path.insert(0, cur)

from pages import main_page as mp
from pages import join_page as jp
from pages import plan_offer_page as po
from pages import payment_option_page as pop
from pages import login_page as lp
from pages.login_page import AutoMatic_Login
from pages import residency_page as rp
from pages import address_area_page as aa
from pages.address_area_page import AutoMatic_Address_Area
from pages import payment_page as pp
from pages import coverage_map_page as cm
from pages.coverage_map_page import Automatic_map_coverage
from pages import plans_page as p
from pages import confirm_coverage_page as cc
from pages import delivery_page as dp
from pages import collect_in_store as cis
from csv_handler import append_to_csv

from base import SafeStep
from base import csv_input
from base import driver_update

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
try:
    driver.maximize_window()
except:
    pass
driver.implicitly_wait(30)
driver.get(os.environ["BASE_URL"])
time.sleep(3)

file_name = "TC04_c.csv"

def Confirm_Main_Page():
    SafeStep(0,mp.XPATH_HEADER_BUILD_A_PLAN_HEADER,"Main","Build a plan that’s right for YOU")

def Go_to_JoinPage():
    SafeStep(mp.XPATH_BUILD_YOUR_PLAN_BTN,jp.XPATH_HEADER,"Join","What Brings You Here?")

def Go_To_Coverage_Map_Page():
    SafeStep(jp.XPATH_HOME_INTERNET_BTN,cm.XPATH_HEADER,"Coverage Map","Check your coverage")
    Automatic_map_coverage(driver)

def Go_To_Confirm_Coverage_Page():
    time.sleep(4)
    SafeStep(cm.XPATH_CHECK_COVERAGE_BTN,cc.XPATH_HEADER,"Confirm Coverage","Good news!")

def Go_to_Residency_Page():
    SafeStep(cc.XPATH_CONTINUE_BTN,rp.XPATH_HEADER_VALID_EMIRATES,"Residency","Have a valid Emirates ID?")
    time.sleep(5)

def Go_to_Plans_Page():
    SafeStep(rp.XPATH_NO_EMIRATES_ID_BTN,p.XAPTH_HEADER,"Plans","12-months offer")
    time.sleep(4)
    SafeStep(p.XPATH_NO_ROUTER_BTN,0,0,0)

def Go_To_Login_Page():
    SafeStep(p.XPATH_CONTINUE_BTN,lp.XPATH_HEADER_HOME_INTERNET,"Login","It's nice to meet you!")
    time.sleep(3)
    AutoMatic_Login(driver)

def Got_To_Collect_In_Store():
    SafeStep(lp.XPATH_CONFIRM_EMAIL_BTN,cis.XPATH_HEADER,"Collect In Store","Pay now and collect from a")
    time.sleep(5)

def Go_To_PaymentPage():
    SafeStep(cis.XPATH_CONTINUE_BTN,pp.XPATH_HEADER_HOME_INTERNT,"Payment","Review your order")
    time.sleep(2)
    SafeStep(pp.XPATH_GEOLOCKED_CONFIRM_BTN,0,0,0)
    Confirm_Plan_Information()

def Confirm_Plan_Information():
    time.sleep(2)
    SafeStep(pp.XPATH_AGREE_TERMS_HOME_INTERNET_BTN,0,0,0)
    SafeStep(pp.XPATH_ADD_TO_REGISTRY_HOME_INTERNET_BTN,0,0,0)
    SafeStep(pp.XPATH_CONFIRM_REGISTRY_HOME_INTERNET_BTN,0,0,0)

def Go_To_PaymentOption_Page():
    SafeStep(pp.XPATH_CHOOSE_PAYMENT_HOME_INTERNET_BTN,pop.XPATH_HEADER_HOME_INTERNET,"Payment Option","Payment method")

def Final_Order_Confirmation():
    time.sleep(5)
    driver.quit()

driver_update(driver,file_name)
Confirm_Main_Page()
Go_to_JoinPage()
Go_To_Coverage_Map_Page()
Go_To_Confirm_Coverage_Page()
Go_to_Residency_Page()
Go_to_Plans_Page()

Go_To_Login_Page()
Got_To_Collect_In_Store()
Go_To_PaymentPage()
Go_To_PaymentOption_Page()
Final_Order_Confirmation()
csv_input(file_name)

# Home Internet Plan - With Location - No Emirates Id - No router - order
