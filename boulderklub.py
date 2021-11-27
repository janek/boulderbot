from selenium.webdriver.common.by import By
from selenium_helpers import get_driver, process_dates

driver = get_driver()

def open_bookings():
  driver.get("https://boulderklub.de/")
  element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates").click()

def check():
  open_bookings()
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
  dates = process_dates(element.get_attribute('innerHTML'))
  return dates

def book(user):
  return "Coming soon!"
