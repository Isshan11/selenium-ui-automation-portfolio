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
from pages import plan_selection_page as ps
from pages import plan_offer_page as po
from pages import select_number_page as sn
from pages import login_page as lp
from pages.login_page import AutoMatic_Login
from pages import residency_page as rp
from pages import address_map_page as am
from pages.address_map_page import AutoMatic_Address_Map
from pages import address_area_page as aa
from pages.address_area_page import AutoMatic_Address_Area
from pages import payment_page as pp
from pages import payment_option_page as pop
from pages import order_confirmation_page as oc
from csv_handler import append_to_csv
from pages import device_selection_page as ds
from pages import choose_your_iphone_page as cyi

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

file_name = "TC01_d_b.csv"

def Confirm_Main_Page():
    SafeStep(0,mp.XPATH_HEADER,"Main","Join Virgin Mobile")

def Go_to_JoinPage():
    SafeStep(mp.XPATH_GET_STARTED_BTN,jp.XPATH_HEADER,"Join","What Brings You Here?")

def Go_To_PlanSelection_Page():
    SafeStep(jp.XPATH_MOBILE_PLAN_BTN,ps.XPATH_HEADER,"Plan Selection","Build your own plan")
    SafeStep(0,ps.XPATH_YOUTH_PLAN_HEADER,"Youth Plan Option","Youth Plan")
    SafeStep(ps.XPATH_STARTER_PLANS_BTN,ps.XPATH_STARTER_PLANS_HEADER,"Starter Plans Option","Check our great starter plans!")

def Go_to_SelectNumber_Page():
    time.sleep(2)
    SafeStep(ps.XPATH_50_MONTHLY_BTN,sn.XPATH_HEADER,"Select Number","Find a number you love")

def Go_To_Login_Page():
    SafeStep(sn.XPATH_THIS_NUMBER_BTN,lp.XPATH_HEADER,"Login Page","It's nice to meet you!")
    time.sleep(3)
    AutoMatic_Login(driver)
    SafeStep(0,lp.XPATH_CONFIRM_EMAIL_HEADER,"Login Popup(Confirm Email)","Is this your email?")

def Go_to_Residency_Page():
    SafeStep(lp.XPATH_CONFIRM_EMAIL_BTN,rp.XPATH_HEADER,"Residency","Choose your ID type")

def Go_To_Address_Map_Page():
    SafeStep(rp.XPATH_EMIRATED_ID_BTN,am.XPATH_HEADER,"Address Map","We'll deliver your SIM")
    AutoMatic_Address_Map(driver)

def Go_To_Address_Area_Page():
    SafeStep(am.XPATH_DELIVER_HERE_BTN,aa.XPATH_HEADER,"Address Area","We'll deliver your SIM")
    SafeStep(aa.XPATH_VILLA_BTN,aa.XPATH_VILLA_HEADER,"Address Villa(option)","How can we get in touch in case the driver can't find you?")
    AutoMatic_Address_Area(driver)

def Go_To_PaymentPage():
    SafeStep(aa.XPATH_CONTINUE_BTN,pp.XPATH_HEADER,"Payment","Please review the info below.")
    Confirm_Plan_Information()

def Confirm_Plan_Information():
    SafeStep(pp.XPATH_AGREE_TERMS_BTN,0,0,0)
    SafeStep(pp.XPATH_ADD_TO_REGISTRY_BTN,0,0,0)
    SafeStep(pp.XPATH_CONFIRM_REGISTRY_BTN,0,0,0)

def Go_To_PaymentOption_Page():
    SafeStep(pp.XPATH_CHOOSE_PAYMENT_BTN,pop.XPATH_HEADER,"Payment Option","Payment method")
    SafeStep(pop.XPATH_PAY_ON_DELIVERY_BTN,0,0,0)
    SafeStep(pop.XPATH_PAYMENT_CONTINUE_BTN,pop.XPATH_HEADER_POPUP,"Order Confirm Popup","Once confirmed you will not be able to change your order.")

def Final_Order_Confirmation():
    time.sleep(5)
    driver.quit()

driver_update(driver,file_name)
# Run full flow
Confirm_Main_Page()
Go_to_JoinPage()
Go_To_PlanSelection_Page()
Go_to_SelectNumber_Page()
Go_To_Login_Page()
Go_to_Residency_Page()
Go_To_Address_Map_Page()
Go_To_Address_Area_Page()
Go_To_PaymentPage()
Go_To_PaymentOption_Page()
Final_Order_Confirmation()

csv_input(file_name)
#Main Mobile Plan - Starter Plan - AED 50 - order
