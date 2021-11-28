import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium_helpers import get_driver

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def check():
  driver = get_driver()
  driver.get("https://141.webclimber.de/de/booking/offer/boulderslots-gesamt")
  start_time = time.time()
  time.sleep(0.5)
  element = driver.find_element(By.ID, "offerTimes")
  dates = element.get_attribute('outerHTML')
  dates = process_dates(dates)
  end_time = time.time()
  logger.info(f"Checked Suedbloc in {round(end_time - start_time, 2)}s")
  return dates

def book(user):
  return "Coming soon!"

def process_dates(dates):
  dates = re.sub('<[^>]*>', '', dates)

  return dates

check()
