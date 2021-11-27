import time
from selenium_helpers import get_driver, process_date

def check():
  driver = get_driver()
  open_bookings()
  time.sleep(0.5)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
  dates = process_dates(element.get_attribute('innerHTML'))
  return dates

def book(user):
  return "Coming soon!"

def open_bookings():
  driver = get_driver()
  driver.get("https://boulderklub.de/")
  element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates").click()
