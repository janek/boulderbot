import os
import re
import time
import json
import logging
from selenium.webdriver.common.by import By
from selenium_helpers import get_driver
from enum import Enum

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# XXX: Consider support for non-USC (vide kegel link). Note: some gyms are free to book, some paid

class GymName(Enum):
  DER_KEGEL = "Der Kegel"
  SUEDBLOC = "Suedbloc"
  BOULDERGARTEN = "Bouldergarten"
  BOULDERKLUB = "Boulderklub"

gyms = {
    GymName.DER_KEGEL : {
        "emoji": "🔺",
        "link": "https://168.webclimber.de/de/booking/offer/bouldern-urban-sports-club",
    },
    GymName.SUEDBLOC : {
        "emoji": "⚪️",
        "link": "https://141.webclimber.de/de/booking/offer/boulderslots-gesamt",
    },
    GymName.BOULDERGARTEN : {
        "emoji": "🍃",
        "link": "https://bouldergarten.de",
    },
    GymName.BOULDERKLUB : {
        "emoji": "♣",
        "link": "https://boulderklub.de",
    },
}


def gym_is_webclimber(gym: GymName):
  return "webclimber" in gyms[gym]['link']

# XXX: where's the line between open bookings and check? Where's the line between selenium helpers and gyms?
# A: "helpers" should be independent of which gym it is. open bookings should be part of check and then go to process_dates

def check(gym: GymName):
  start_time = time.time()
  driver = get_driver()
  driver.get(gyms[gym]["link"])

  if gym_is_webclimber(gym):
    time.sleep(2) # TODO: test without
    element = driver.find_element(By.ID, "offerTimes")
    # TODO: extract the lines below (can outer be inner or sth? print after the base run works
    dates = element.get_attribute('outerHTML')
    dates = process_dates_webclimber(dates)
  else:
    if gym == GymName.BOULDERGARTEN:
      bouldergarten_extra_steps_for_checking(driver)
    element = driver.find_element(By.CSS_SELECTOR, ".drp-calendar-day-dates").click()
    logger.info("Cal-day-dates clicked")
    # XXX: We might have to exclude the dates with the `drp-date-not-relevant` class, unless date is pre-set
    # Selenium has a not, but unclear how to apply it to the class of the containing elements.
    # https://www.qafox.com/selenium-locators-using-not-in-css-selectors/ (too long article)
    # items = driver.find_elements_by_css_selector("div.examplenameA:not(.examplenameB)")
    element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
    dates = process_dates(element.get_attribute('innerHTML'))

  end_time = time.time()
  logger.info(f"Checked {gym} in {round(end_time - start_time, 2)}s")
  return dates


def bouldergarten_extra_steps_for_checking(driver):
    # XXX: JS "clicks" vs "mouse" clicks()
    # 1. the issue that forced our usage of JS click might be resolved by waits)
    # 2. JS "clicks" don't seem to work on non-clickable HTML elems, while "mouse" clicks() do
    # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
    try:
      logger.info("Cookie banner accepted")
      driver.find_element(By.ID, "cn-accept-cookie").click() # XXX: may be unnecessary
      # element = driver.find_element(By.ID, "cn-accept-cookie")
      # driver.execute_script("arguments[0].click();", element)
    except Exception as e:
      logger.info("Cookie banner not found, error: " + str(e))
    element = driver.find_element(By.ID, "eintritt-buchen").click()
    element = driver.find_element(By.CSS_SELECTOR, ".drp-course-list-item-eintritt-slot").click()
    logger.info("Eintritt-slot clicked")
    time.sleep(1)
    # Hand-tuned value for lowest sleep time that doesn't result in a crash.
    # XXX: Consider using selenium.common.exceptions.NoSuchElementExceptionebDriverWait instead of Python time.sleep()
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "eintritt-buchen")))
    # TODO Should try to replace with a function that waits for an element to appear
    return element


def process_dates_html(dates): # Dr plano
  # save_dates_to_fixture(dates, source="dr_plano")
  dates = re.sub('<[^>]*>', '', dates)
  # lines = [line.strip() for line in dates.splitlines() if len(re.sub('\s*', '', line)) > 0 and not "Buchen" in line and not "begonnen" in line]
  lines = dates
  date_strings = lines[2::3]
  status_strings = lines[::3]

  start_end_times = [tuple(line.split(" - ")) for line in date_strings]
  free_slots = [re.sub("[^0-9]", "", line) for line in status_strings]

  slots =  [
      { i :
        {
          "start_time": start,
          "end_time": end,
          "free_slots": (0 if number == "" else number)
        }
      } for i, ((start, end), number) in enumerate(zip(start_end_times, free_slots))
  ]

  slots_json = json.dumps(slots)
  with open("experiment_output_json_cache.py", "w+") as file:
      file.write(slots_json)
  return slots_json


def process_dates_html(dates: str, gym: GymName):
  # save_dates_html_to_fixture(dates, source=gym)
  if gym_is_webclimber(gym):
    dates = re.sub('<[^>]*>', '', dates)
    dates = re.sub('Buchen', '\n', dates)
    dates = re.sub('Uhr', '- ', dates)
    lines = [line.strip() for line in dates.splitlines() if line.strip() != '']
    # dates = re.sub('mehr als 10 Plätze verfügbar', '10+ places', dates) # TODO: note down somewhere that 10 is 10+
    # dates = re.sub(r'^\s*S', 'a', dates) # TODO: figure out what this means
  else:
    dates = re.sub('<[^>]*>', '', dates)
    lines = [
      line.strip() for line in dates.splitlines()
      if len(re.sub('\s*', '', line)) > 0 # Clean up whitespace lines
      and not "Buchen" in line and not "begonnen" in line # Filter out extra lines for a consistent output
    ]
    date_strings = lines[2::3]
    status_strings = lines[::3]
    lines = [date + " - " + status for (date, status) in zip(date_strings, status_strings)]

  info = [tuple(line.split(" - ")) for line in lines]
  info = [(start, end, re.sub("[^0-9]", "", num_slots)) for (start, end, num_slots) in info]

  slots =  [
      {
        "start_time": start,
        "end_time": end,
        "free_places": (0 if num_slots == "" else num_slots)
      } for (start, end, num_slots) in info
  ]

  slots_json = json.dumps(slots)
  filename = "cache/" + gym.value + ".json"
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  with open(filename, "w") as file:
      file.write(slots_json)
  return slots_json


def format_slot_information_for_telegram(slots_json):
  slots = json.loads(slots_json)
  n_places_str = lambda i: "10+" if i >= 10 else str(i)
  return [
    slot["start_time"] + " - " + slot["end_time"] + " → " + n_places_str(int(slot["free_places"]))
    for slot in slots if int(slot["free_places"]) > 0
  ]

def save_dates_html_to_fixture(dates, source):
  logger.info("saving?")
  filepath = "fixtures/dates_" + source + ".txt"
  with open(filepath, "w+") as file:
    file.write(dates)

def book(user):
  return "Coming soon!"
