import os
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait #XXX: Potentially unused
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

first_name = "Janek"
surname = "Szynal"
postcode = "00000"
mobile_number = "000000000"
landline_number = "000000000"
email = "jan.szynal+bouldergarten@gmail.com"
urbansports_number = "100047904"

inputs_group = [first_name, surname, postcode, mobile_number, landline_number, email]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#TODO: move
def program_is_running_on_heroku() -> bool:
    return ('IS_HEROKU' in os.environ)


def load_driver():
  # return webdriver.Firefox() # TEMP
  print(f"Running on Heroku: {program_is_running_on_heroku()}")
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox")
  service = Service(os.environ.get("CHROMEDRIVER_PATH"))
  driver = webdriver.Chrome(options=chrome_options, service=service)
  return driver

driver = load_driver()

def open_bookings(driver):
  driver.get("https://bouldergarten.de/")
  # XXX: JS "clicks" vs "mouse" clicks()
  # 1. the issue that forced our usage of JS click might be resolved by waits)
  # 2. JS "clicks" don't seem to work on non-clickable HTML elems, while "mouse" clicks() do
  # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen

  try:
    time.sleep(0.5)
    driver.find_element(By.ID, "cn-accept-cookie").click() # XXX: may be unnecessary
    print("Cookie accepted")
  except Exception as e:
    print(e)
    print("cookie not found")

  # XXX: Consider using Wselenium.common.exceptions.NoSuchElementExceptionebDriverWait instead of Python time.sleep() - should be faster to execute
  # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "eintritt-buchen")))
  element = driver.find_element(By.ID, "cn-accept-cookie")
  driver.execute_script("arguments[0].click();", element)

  # Book entry button
  element = driver.find_element(By.ID, "eintritt-buchen").click()
  # driver.execute_script("arguments[0].click();", element)

  time.sleep(0.5)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-list-item-eintritt-slot").click()

  time.sleep(1)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates").click()

def check():
  open_bookings(driver)
  # XXX: We might have to exclude the dates with the `drp-date-not-relevant` class, unless date is pre-set
  # Selenium has a not, but unclear how to apply it to the class of the containing elements.
  # https://www.qafox.com/selenium-locators-using-not-in-css-selectors/ (too long article)
  # items = driver.find_elements_by_css_selector("div.examplenameA:not(.examplenameB)")

  time.sleep(0.5)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
  dates = process_dates(element.get_attribute('innerHTML'))
  return dates

def book(user):
  if user == "rrszynka":
    open_bookings(driver)
    logger.info("Booking for user "+ user)
  return "Coming soon!"

def process_dates(dates):
  dates = re.sub('<[^>]*>', '', dates)
  lines = [line.strip() for line in dates.splitlines() if len(re.sub('\s*', '', line)) > 0 and not "Buchen" in line and not "begonnen" in line]
  date_strings = lines[2::3]
  status_strings = lines[::3]
  status_strings = [status.replace("freie Plätze", "slots").replace("freier Platz", "slot") for status in status_strings]
  data = [a + " → " + b for a, b in list(zip(date_strings, status_strings)) if not "ausgebucht" in b and not "abgelaufen" in b]
  return "\n".join(data)
