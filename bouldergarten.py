import pytest
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait #XXX: Potentially unused
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options


first_name = "Janek"
surname = "Szynal"
postcode = "00000"
mobile_number = "000000000"
landline_number = "000000000"
email = "jan.szynal+bouldergarten@gmail.com"
urbansports_number = "100047904"

inputs_group = [first_name, surname, postcode, mobile_number, landline_number, email]

options = Options()
options.headless = False # TODO: true
driver = webdriver.Firefox(options=options)

def book():
  driver.get("https://bouldergarten.de/")
  driver.set_window_size(982,752) # XXX: may be unnecessary
  driver.find_element(By.ID, "cn-accept-cookie").click() # XXX: may be unnecessary
  driver.execute_script("window.scrollTo(0,8)") # XXX: may be unnecessary
  print("hi")

  # XXX: consider replacing JS clicks with clearer syntax clicks()
  # (the issue that forced our usage of JS click might be resolved by waits)
  # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen

  # XXX: Consider using WebDriverWait instead of Python time.sleep() - should be faster to execute
  # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "eintritt-buchen")))

  # Book entry button
  element = driver.find_element(By.ID, "eintritt-buchen")
  driver.execute_script("arguments[0].click();", element)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-list-group-halleneintritt:nth-child(3) a")
  driver.execute_script("arguments[0].click();", element)

  time.sleep(1)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates.drp-calendar-day:nth-child(7)")
  driver.execute_script("arguments[0].click();", element)
  print("oy")

  # XXX: We might have to exclude the dates with the `drp-date-not-relevant` class, unless date is pre-set
  # Selenium has a not, but unclear how to apply it to the class of the containing elements.
  # https://www.qafox.com/selenium-locators-using-not-in-css-selectors/ (too long article)
  # items = driver.find_elements_by_css_selector("div.examplenameA:not(.examplenameB)")

  time.sleep(1)
  element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
  html_with_dates = element.get_attribute('innerHTML')

  # XXX: consider merging into one line with a combined regex (using ors)
  dates = re.sub(r'<[^>]*>', '', html_with_dates)
  dates = re.sub(r'\t|\n', '', dates)
  return dates
  # element = driver.find_element(By.CSS_SELECTOR, ".drp-course-date-item:nth-child(9) .drp-course-date-item-booking-button > span")
  # driver.execute_script("arguments[0].click();", element)

  # # Fill out the form
  # for i, value in enumerate(inputs_group):
  #   time.sleep(1)
  #   element = driver.find_element(By.CSS_SELECTOR, f".drp-row:nth-child({i+2}) > .drp-col-12 > input")
  #   driver.execute_script("arguments[0].click();", element)
  #   element.send_keys(inputs_group[i])

  # select = Select(driver.find_element(By.CSS_SELECTOR, ".drp-course-booking-tariff-select > .drp-w-100"))
  # select.select_by_value("68083827")
  # time.sleep(1)
  # driver.find_element(By.CSS_SELECTOR, ".drp-col-8:nth-child(6) > .drp-w-100").send_keys("100047904")
  # driver.find_element(By.ID, "drp-course-booking-client-terms-cb").click()
  # driver.find_element(By.ID, "drp-course-booking-data-processing-cb").click()

  # # Be careful not to spam reservations!
  # # driver.find_element(By.CSS_SELECTOR, ".drp-course-booking-continue").click()
  # return True
