import pytest
import time
import json
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bouldergarten import book, check, process_dates, load_driver, open_bookings

# TODO: pull from DB
first_name = "Janek"
surname = "Szynal"
postcode = "00000"
mobile_number = "000000000"
landline_number = "000000000"
email = "jan.szynal+bouldergarten@gmail.com"
urbansports_number = "100047904"

inputs_group = [first_name, surname, postcode, mobile_number, landline_number, email]
# driver = load_driver()
driver = webdriver.Firefox()
open_bookings(driver)

time.sleep(0.5)
desired_timeslot = "20:00"
# Limit to dates for normal bookings (excluding yoga and courses)
dates_wrapper = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
spans_with_text = dates_wrapper.find_elements(By.CSS_SELECTOR, ".drp-course-date-item")

def index_for_timeslot(timeslot: str) -> int:
  # TODO: Design a nicer function for this, after considering other halls (whether it generalizes)
  # NOTE: Alternative would be to use XPATH, currently broken version that used to work, below. Use "19:30 -", with dash
  # spans_with_text = dates_wrapper.find_elements_by_xpath(f".//*[contains(text(), '{desired_timeslot}')]")
  # span_and_button_common_parent = correct_span.find_element_by_xpath("../../..")
  # booking_button = span_and_button_common_parent.find_element(By.CSS_SELECTOR, ".drp-course-date-item-booking-button")
  # driver.execute_script("arguments[0].click();", booking_button)
  all_timeslots = [(datetime.datetime(1,1,1,10,0) + datetime.timedelta(minutes=n*30)).strftime("%H:%M") for n in range(0, 22)]
  return all_timeslots.index(timeslot)

slot_element = spans_with_text[index_for_timeslot(desired_timeslot)]
book_button = slot_element.find_element(By.CSS_SELECTOR, ".drp-course-date-item-booking-button")
driver.execute_script("arguments[0].click();", book_button)

# Filter to find the one where this is the start time, not the end time

# TODO: find_elements for all drp-row within their div wrapper
# Fill out the form
for i, value in enumerate(inputs_group):
  time.sleep(0.5)
  element = driver.find_element(By.CSS_SELECTOR, f".drp-row:nth-child({i+2}) > .drp-col-12 > input")
  driver.execute_script("arguments[0].click();", element)
  element.send_keys(inputs_group[i])

driver.find_element(By.ID, "drp-course-booking-person-email").send_keys("jan.szynal+bou@gmail.com")
dropdown = driver.find_element(By.CSS_SELECTOR, ".drp-course-booking-tariff-select > .drp-w-100")
time.sleep(0.5)
# Works until now
# dropdown.find_element(By.XPATH, "//option[. = 'USC-Mitglied (Urban Sports Club)']").click()
# driver.find_element(By.CSS_SELECTOR, "option:nth-child(8)").click()
# driver.find_element(By.CSS_SELECTOR, ".drp-col-8:nth-child(6) > .drp-w-100").click()
# driver.find_element(By.CSS_SELECTOR, ".drp-col-8:nth-child(6) > .drp-w-100").send_keys("100047904")
# driver.find_element(By.ID, "drp-course-booking-client-terms-cb").click()
# driver.find_element(By.ID, "drp-course-booking-data-processing-cb").click()
#driver.find_element(By.CSS_SELECTOR, ".drp-course-booking-continue").click()
