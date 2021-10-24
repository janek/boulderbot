import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait #XXX: Potentially unused
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# TODO: replace sleeps with waits
# TODO: unpack from pytest
# XXX: consider replacing JS clicks with clearer syntax clicks()

class TestBouldergartenBookingTest():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_bouldergarten(self):
    # Test name: v3
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("https://bouldergarten.de/")
    # 2 | setWindowSize | 982x752 | 
    self.driver.set_window_size(982,752)
    # 3 | click | id=cn-accept-cookie |
    self.driver.find_element(By.ID, "cn-accept-cookie").click()
    # 4 | runScript | window.scrollTo(0,8) | 
    self.driver.execute_script("window.scrollTo(0,8)")
    # 5 | click | id=eintritt-buchen |
    # JANEK: https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
    element = self.driver.find_element(By.ID, "eintritt-buchen")
    self.driver.execute_script("arguments[0].click();", element)
    # 6 | click | css=.drp-course-list-group:nth-child(3) strong |
    element = self.driver.find_element(By.CSS_SELECTOR, ".drp-course-list-group-halleneintritt:nth-child(3) a")
    self.driver.execute_script("arguments[0].click();", element)
    # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "eintritt-buchen")))
    time.sleep(1)
    # # 7 | click | css=.drp-calendar-week:nth-child(4) > .drp-calendar-day:nth-child(6) |
    element = self.driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates")
    self.driver.execute_script("arguments[0].click();", element)
    # 8 | runScript | window.scrollTo(0,3879) |
    # self.driver.execute_script("window.scrollTo(0,3879)")

    # items = driver.find_elements_by_css_selector("div.examplenameA:not(.examplenameB)")
    # 9 | click | css=.drp-course-date-item:nth-child(21) .drp-course-date-item-booking-button > span |
    time.sleep(1)
    element = self.driver.find_element(By.CSS_SELECTOR, ".drp-course-date-item:nth-child(5) .drp-course-date-item-booking-button > span")
    # TODO: exclude the dates with the `drp-date-not-relevant` class.
    # Selenium has a not, but unclear how to apply it to the class of the containing elements.
    # https://www.qafox.com/selenium-locators-using-not-in-css-selectors/ (too long article)
    self.driver.execute_script("arguments[0].click();", element)
    # 10 | click | css=.drp-row:nth-child(2) > .drp-col-12 > input |
    time.sleep(1)
    element = self.driver.find_element(By.CSS_SELECTOR, ".drp-row:nth-child(2) > .drp-col-12 > input")
    self.driver.execute_script("arguments[0].click();", element)
    # 11 | type | css=.drp-row:nth-child(2) > .drp-col-12 > input | Janek
    time.sleep(1)
    element = self.driver.find_element(By.CSS_SELECTOR, ".drp-row:nth-child(2) > .drp-col-12 > input")
    element.send_keys("Janek")
    time.sleep(1)
    
