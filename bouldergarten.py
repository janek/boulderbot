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

def load_driver():
  # chrome_options = webdriver.ChromeOptions()
  # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  # chrome_options.add_argument("--headless")
  # chrome_options.add_argument("--disable-dev-shm-usage")
  # chrome_options.add_argument("--no-sandbox")
  # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox")
  service = Service(os.environ.get("CHROMEDRIVER_PATH"))
  driver = webdriver.Chrome(options=chrome_options, service=service)

  # options = webdriver.ChromeOptions()
  # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  # options.add_argument("--remote-debugging-port=9222")
  # options.add_argument("--headless")
  # options.add_argument("--disable-gpu")
  # options.add_argument("--no-sandbox")
  # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
  return driver

driver = load_driver()

def open_bookings():
  driver.get("https://bouldergarten.de/")

  # XXX: consider replacing JS clicks with clearer syntax clicks()
  # (the issue that forced our usage of JS click might be resolved by waits)
  # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen

  # XXX: Consider using WebDriverWait instead of Python time.sleep() - should be faster to execute
  # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "eintritt-buchen")))

  # Book entry button
  element = driver.find_element(By.ID, "eintritt-buchen")
  driver.execute_script("arguments[0].click();", element)

  time.sleep(0.5)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-list-group-halleneintritt:nth-child(3) a")
  driver.execute_script("arguments[0].click();", element)

  time.sleep(0.5)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates")
  driver.execute_script("arguments[0].click();", element)

def check():
  open_bookings()
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
    open_bookings()
    logger.info("Booking for user "+ user)
  return "Coming soon!"
  # element = driver.find_element(By.CSS_SELECTOR, ".drp-course-date-item:nth-child(9) .drp-course-date-item-booking-button > span")
  # driver.execute_script("arguments[0].click();", element)

  # # Fill out the form
  # for i, value in enumerate(inputs_group):
  #   time.sleep(0.5)
  #   element = driver.find_element(By.CSS_SELECTOR, f".drp-row:nth-child({i+2}) > .drp-col-12 > input")
  #   driver.execute_script("arguments[0].click();", element)
  #   element.send_keys(inputs_group[i])

  # select = Select(driver.find_element(By.CSS_SELECTOR, ".drp-course-booking-tariff-select > .drp-w-100"))
  # select.select_by_value("68083827")
  # time.sleep(0.5)
  # driver.find_element(By.CSS_SELECTOR, ".drp-col-8:nth-child(6) > .drp-w-100").send_keys("100047904")
  # driver.find_element(By.ID, "drp-course-booking-client-terms-cb").click()
  # driver.find_element(By.ID, "drp-course-booking-data-processing-cb").click()

  # # Be careful not to spam reservations!
  # # driver.find_element(By.CSS_SELECTOR, ".drp-course-booking-continue").click()
  # return True


def process_dates(dates):
  dates = re.sub('<[^>]*>', '', dates)
  lines = [line.strip() for line in dates.splitlines() if len(re.sub('\s*', '', line)) > 0 and not "Buchen" in line and not "begonnen" in line]
  date_strings = lines[1::2]
  status_strings = lines[::2]
  status_strings = [status.replace("freie Plätze", "slots").replace("freier Platz", "slot") for status in status_strings]
  data = [a + " → " + b for a, b in list(zip(date_strings, status_strings)) if not "ausgebucht" in b and not "abgelaufen" in b]
  return "\n".join(data)
