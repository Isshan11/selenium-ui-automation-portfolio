import random
import string
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from csv_handler import append_to_csv



XPATH_HEADER = '//*[@id="vmo-onboarding-page"]/div/div/div/div/div/div[2]/div[1]/h2/span'
XPATH_HEADER_HOME_INTERNET = '//*[@id="vmo"]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/h2/span'
XPATH_EMAIL_INPUT = '//*[@id="userEmail"]'
XPATH_PASSWORD_INPUT = '//*[@id="userPassword"]'
XPATH_CONFIRM_EMAIL_BTN = '//*[@id="btn_confirm_email_yes"]'
XPATH_CONFIRM_EMAIL_HEADER = '//*[@id="vmo-onboarding-page"]/div[2]/div[2]/div/div/h2'
XPATH_CONFIRM_EMAIL_HEADER_HOME_INTERNET = '//*[@id="vmo"]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div/h2'

def AutoMatic_Login(self):
    filename = "Email_to_del.csv"

    while True:
        email = Genrate_Random_Email()
        if not Read_Email(email, filename):
            break


    self.find_element(By.XPATH, XPATH_EMAIL_INPUT).send_keys(email, Keys.RETURN)
    self.find_element(By.XPATH, XPATH_PASSWORD_INPUT).send_keys(os.environ["TEST_ACCOUNT_PASSWORD"], Keys.RETURN)


    Save_Email_To_Del(email, filename)

def Genrate_Random_Email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}@mailinator.com"

def Read_Email(email, filename):

    if not os.path.isfile(filename):
        return False
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('Email') == email:
                return True
    return False

def Save_Email_To_Del(email, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Email'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Email': email})
    print("Data Stored:", email)
