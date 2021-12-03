import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium_helpers import get_driver, process_dates_webclimber

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Make a 'gym' struct shared across this project
# TODO: Consider support for non-USC (vide kegel link). Note: some gyms are free to book, some paid
gyms = {
  "Der Kegel": "https://168.webclimber.de/de/booking/offer/bouldern-urban-sports-club",
  "Suedbloc": "https://141.webclimber.de/de/booking/offer/boulderslots-gesamt"
}

def check(gym="Der Kegel"):
  start_time = time.time()
  driver = get_driver()
  driver.get(gyms[gym])
  time.sleep(2)
  element = driver.find_element(By.ID, "offerTimes")
  dates = element.get_attribute('outerHTML')
  dates = process_dates_webclimber(dates)
  end_time = time.time()
  logger.info(f"Checked {gym} in {round(end_time - start_time, 2)}s")
  return dates

def book(user):
  return "Coming soon!"
