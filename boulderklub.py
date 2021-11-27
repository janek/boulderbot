import time
import logging
from selenium.webdriver.common.by import By
from selenium_helpers import get_driver, process_dates

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def check():
  start_time = time.time()
  driver = get_driver()
  open_bookings()
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
  dates = process_dates(element.get_attribute('innerHTML'))
  end_time = time.time()
  logger.info(f"Checked Boulderklub in {round(end_time - start_time, 2)}s")
  return dates

def book(user):
  return "Coming soon!"

def open_bookings():
  driver = get_driver()
  driver.get("https://boulderklub.de/")
  element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates").click()
