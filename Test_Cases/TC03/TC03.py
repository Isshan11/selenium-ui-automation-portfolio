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
from pages import login_page as lp
from pages.login_page import AutoMatic_Login
from pages import payment_page as pp
from pages import payment_option_page as pop
from csv_handler import append_to_csv
from pages import activation_method_page as am

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
file_name = "TC03.csv"

def Confirm_Main_Page():
    SafeStep(0,mp.XPATH_HEADER_REASON_TO_LOVE,"Main","6 reasons why you’ll love us")


def Go_to_JoinPage():
    SafeStep(mp.XPATH_GET_STARTED_2_BTN,jp.XPATH_HEADER,"Join","What Brings You Here?")

def Go_To_PlanSelection_Page():
    SafeStep(jp.XPATH_TOURIST_PLAN_BTN,ps.XPATH_HEADER_TOURIST_PLAN,"Plan Selection","Pick a plan that suits you")

def Go_To_Login_Page():
    SafeStep(ps.XPATH_CONTINUE_TOURIST_BTN,lp.XPATH_HEADER,"Login Page","It's nice to meet you!")

    AutoMatic_Login(driver)
    SafeStep(0,lp.XPATH_CONFIRM_EMAIL_HEADER,"Login Popup(Confirm Email)","Is this your email?")

def Got_To_Activation_Method():
    SafeStep(lp.XPATH_CONFIRM_EMAIL_BTN,am.XPATH_HEADER,"Activation Method Page","Choose activation method")


def Go_To_PaymentPage():
    SafeStep(am.XPATH_PHYSICAL_ACTIVATION_BTN,pp.XPATH_HEADER,"Payment","Please review the info below.")
    Confirm_Plan_Information()

def Confirm_Plan_Information():
    SafeStep(pp.XPATH_AGREE_TERMS_BTN,0,0,0)
    SafeStep(pp.XPATH_ADD_TO_REGISTRY_BTN,0,0,0)
    SafeStep(pp.XPATH_CONFIRM_REGISTRY_BTN,0,0,0)

def Go_To_PaymentOption_Page():
    SafeStep(pp.XPATH_CHOOSE_PAYMENT_BTN,pop.XPATH_HEADER,"Payment Option","Payment method")

def Final_Order_Confirmation():
    time.sleep(5)
    driver.quit()

driver_update(driver,file_name)
Confirm_Main_Page()
Go_to_JoinPage()
Go_To_PlanSelection_Page()
Go_To_Login_Page()
Got_To_Activation_Method()
Go_To_PaymentPage()
Go_To_PaymentOption_Page()
Final_Order_Confirmation()
csv_input(file_name)

# Tourist Plan