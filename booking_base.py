import os
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


class BookingBase:
    def __init__(self):
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 1000)

        self.start_url = os.environ["URL"]
        self.court = os.environ["COURT"]
        self.court = "0" + str(self.court)
        self.date = os.environ["DATE"]
        timing = os.environ["TIMING"]
        index = int(timing)
        index /= 100
        index -= 8
        self.timing_index = int(index)

        self.username = os.environ["USERNAMENTU"]
        self.password = os.environ["PASSWORD"]
        self.wait_midnight = os.environ["WAIT_TILL_MIDNIGHT"]

    def start(self):
        self.driver.get(self.start_url)
        xpath_booking_for_students = "//font[text()='Full time NTU/NIE  UnderGrad Students']"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_booking_for_students)
            )
        ).click()

    def sign_in_ntu(self):
        xpath_username_ntu = "//input[@id='userNameInput']"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_username_ntu)
            )
        ).send_keys(self.username)
        xpath_password_ntu = "//input[@id='passwordInput']"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_password_ntu)
            )
        ).send_keys(self.password)
        xpath_confirm_ntu = "//span[text()='Sign in']"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_confirm_ntu)
            )
        ).click()

    def select_facilities(self):
        if self.wait_midnight == "True":
            current_time = time.localtime()
            time_until_midnight = (24 - current_time.tm_hour) * 3600 - current_time.tm_min * 60 - current_time.tm_sec
            # Wait until midnight
            time.sleep(time_until_midnight)
        xpath_badminton_facility = "//input[@type='radio' and @name='p_info' and @value='1BB26']"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_badminton_facility)
            )
        ).click()
        try:
            radio_button = self.driver.find_element(By.XPATH, xpath_badminton_facility)
            while radio_button:
                radio_button.click()
        except:
            pass

    def select_date(self):
        xpath_badminton_date = \
            f"//input[@type='radio' and @name='p_rec' and @value='1BB2BB{self.court}{self.date}{self.timing_index+1}']"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_badminton_date)
            )
        ).click()

    def select_confirm(self):
        xpath_confirm_court = "//input[@value='Confirm']"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_confirm_court)
            )
        ).click()

    def find_available_court(self, index=0):
        courts = ['01', '02', '03', '04', '05', '06']
        index = random.randint(0, 5)
        xpath_badminton_radio_button = []
        for court in courts:
            xpath_badminton_radio_button.append(
                f"//input[@type='radio' and @name='p_rec' and @value='1BB2BB{court}{self.date}{self.timing_index + 1}']"
            )
        while True:
            try:
                self.driver.find_element(By.XPATH, xpath_badminton_radio_button[index]).click()
                return
            except:
                index += 1
                if index > 5:
                    index = 0

    def execute(self):
        self.start()
        self.sign_in_ntu()
        self.select_facilities()
        if self.court == "0":
            self.find_available_court()
        else:
            self.select_date()
        self.select_confirm()
        self.driver.quit()
