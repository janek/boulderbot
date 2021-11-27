import time
from selenium.webdriver.common.by import By
from selenium_helpers import get_driver, process_dates


# TODO: Move to selenium_helpers, maybe also rename that file
def check():
  driver = get_driver()
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
  return "Coming soon!"

def open_bookings(driver, for_real=False):
  driver = get_driver()
  driver.get("https://bouldergarten.de/")
  # XXX: JS "clicks" vs "mouse" clicks()
  # 1. the issue that forced our usage of JS click might be resolved by waits)
  # 2. JS "clicks" don't seem to work on non-clickable HTML elems, while "mouse" clicks() do
  # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
  try:
    time.sleep(0.5)
    driver.find_element(By.ID, "cn-accept-cookie").click() # XXX: may be unnecessary
  except Exception as e:
    print(e)
    print("Cookie banner not found")

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
