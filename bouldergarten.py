import time
import logging
from selenium.webdriver.common.by import By
from selenium_helpers import get_driver, process_dates

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO: Move to selenium_helpers, maybe also rename that file
def check(gym="Bouldergarten"):
  start_time = time.time()
  driver = get_driver()
  open_bookings(driver)
  # XXX: We might have to exclude the dates with the `drp-date-not-relevant` class, unless date is pre-set
  # Selenium has a not, but unclear how to apply it to the class of the containing elements.
  # https://www.qafox.com/selenium-locators-using-not-in-css-selectors/ (too long article)
  # items = driver.find_elements_by_css_selector("div.examplenameA:not(.examplenameB)")
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
  dates = process_dates(element.get_attribute('innerHTML'))
  end_time = time.time()
  logger.info(f"Checked Bouldergarten in {round(end_time - start_time, 2)}s")
  return dates

def book(user):
  if user == "rrszynka":
    return "Coming soon, " + user
  return "Coming soon!"

def open_bookings(driver, for_real=False):
  driver = get_driver()
  driver.get("https://bouldergarten.de/")

  # XXX: JS "clicks" vs "mouse" clicks()
  # 1. the issue that forced our usage of JS click might be resolved by waits)
  # 2. JS "clicks" don't seem to work on non-clickable HTML elems, while "mouse" clicks() do
  # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
  try:
    logger.info("Cookie banner accepted")
    driver.find_element(By.ID, "cn-accept-cookie").click() # XXX: may be unnecessary
  except Exception as e:
    logger.info("Cookie banner not found, error: " + str(e))

  # element = driver.find_element(By.ID, "cn-accept-cookie")
  # driver.execute_script("arguments[0].click();", element)

  element = driver.find_element(By.ID, "eintritt-buchen").click()
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-list-item-eintritt-slot").click()

  logger.info("Eintritt-slot clicked")
  time.sleep(1)
  # Hand-tuned value for lowest sleep time that doesn't result in a crash.
  # XXX: Consider using selenium.common.exceptions.NoSuchElementExceptionebDriverWait instead of Python time.sleep()
  # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "eintritt-buchen")))
  # TODO Should try to replace with a function that waits for an element to appear

  element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates").click()
  logger.info("Cal-day-dates clicked")
