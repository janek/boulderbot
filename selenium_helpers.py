import os
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

driver = None

def get_driver():
  global driver
  if driver:
      logger.info("Returning existing driver")
  else:
      logger.info("Loading driver")
      driver = load_driver()
  return driver

def load_driver():
  # TODO: logger.info logs are not showing up in pytest
  print(f"Running on Heroku: {program_is_running_on_heroku()}")
  logger.info(f"Running on Heroku: {program_is_running_on_heroku()}")
  start_time = time.time()
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox")
  service = Service(os.environ.get("CHROMEDRIVER_PATH"))
  driver = webdriver.Chrome(options=chrome_options, service=service)
  end_time = time.time()
  logger.info(f"Loaded driver in {round(end_time - start_time, 2)}s")
  return driver

def process_dates(dates):
  dates = re.sub('<[^>]*>', '', dates)
  lines = [line.strip() for line in dates.splitlines() if len(re.sub('\s*', '', line)) > 0 and not "Buchen" in line and not "begonnen" in line]
  date_strings = lines[2::3]
  status_strings = lines[::3]
  status_strings = [status.replace("freie Plätze", "slots").replace("freier Platz", "slot") for status in status_strings]
  data = [a + " → " + b for a, b in list(zip(date_strings, status_strings)) if not "ausgebucht" in b and not "abgelaufen" in b]
  return "\n".join(data)

def program_is_running_on_heroku() -> bool:
    return ('IS_HEROKU' in os.environ)
