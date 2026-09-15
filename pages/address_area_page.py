import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

XPATH_HEADER = '//*[@id="vmo-onboarding-page"]/div/div/div/div/div/div[2]/div[1]/div/h2/span[1]'
XPATH_HEADER_HOME_INTERNET = '//*[@id="vmo"]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/h2/span'
XPATH_VILLA_HOME_INTERNET_BTN = '//*[@id="vmo"]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]'
XPATH_VILLA_BTN = '//*[@id="vmo-onboarding-page"]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]'
XPATH_VILLA_HEADER = '//*[@id="vmo-onboarding-page"]/div/div/div/div/div/div[2]/div[2]/div[3]/div[1]/div/div[5]'
XPATH_VILLA_HEADER_HOME_INTERNET = '//*[@id="vmo"]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[3]/div[1]/div/div[5]'
XPATH_ADRESS_HOME_INTERNET_INPUT = '//*[@id="delivery_address"]'
XPATH_ADRESS_HOME_INTERNET_OPTION = '/html/body/div[9]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[3]/div[1]/div/div[1]/div/div/div[2]'
XPATH_STREET_INPUT = '//*[@id="street"]'
XPATH_HOUSE_NO_INPUT = '//*[@id="building"]'
XPATH_NAME_INPUT = '//*[@id="customer_name"]'
XPATH_PHONE_INPUT = '//*[@id="phone"]'
XPATH_CONTINUE_BTN = '//*[@id="btn_delivery_form_continue"]'

def AutoMatic_Address_Area(self):
    time.sleep(3)
    self.find_element(By.XPATH, XPATH_STREET_INPUT).clear()
    self.find_element(By.XPATH, XPATH_STREET_INPUT).send_keys("test")
    self.find_element(By.XPATH, XPATH_HOUSE_NO_INPUT).send_keys("test")
    self.find_element(By.XPATH, XPATH_NAME_INPUT).send_keys("test")
    self.find_element(By.XPATH, XPATH_PHONE_INPUT).send_keys("000000000")
    time.sleep(1)