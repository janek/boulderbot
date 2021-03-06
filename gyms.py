import os
import re
import time
from datetime import date, datetime, timedelta
import json
import logging
from selenium.webdriver.common.by import By
from selenium_helpers import get_driver
from enum import Enum

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

last_cached_timestamp = 0
MAX_CACHE_AGE_MINUTES = 5

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
        "dr_plano_id": "67359814",
    },
    GymName.BOULDERKLUB : {
        "emoji": "♣",
        "link": "https://boulderklub.de",
        "dr_plano_id": "67361411",
    },
}


def gym_is_webclimber(gym: GymName):
  return "webclimber" in gyms[gym]['link']

# XXX: where's the line between open bookings and check? Where's the line between selenium helpers and gyms?
# A: "helpers" should be independent of which gym it is. open bookings should be part of check and then go to process_dates

# XXX: Gym information should probably be stored in a single JSON file and not multiple,
# also consider a database.
# XXX: force_last_cached_timestamp can be removed or reframed as force_refresh?
def get_gym_information(gym: GymName, days_to_fetch: {int} = {0}, force_last_cached_timestamp=None):
  """ Checks cache for gym info. If cache is too old, refreshes the info"""
  assert days_to_fetch >= 0 and days_to_fetch <= 6, "We can only process 7 days"
  cached_timestamp = force_last_cached_timestamp if force_last_cached_timestamp != None else last_cached_timestamp
  cache_age_minutes = round((time.time() - cached_timestamp)/60)
  logger.info("Cache age: " + str(cache_age_minutes) + " min")
  if cache_age_minutes > MAX_CACHE_AGE_MINUTES:
    logger.info("Refreshing gym information")
    slots = refresh_gym_information(gym, days_to_fetch=days_to_fetch)
  else:
    logger.info("Loading gym information from cache")
    with open(cache_location(gym), "r") as file:
      slots = json.loads(file.read())
  return format_slot_information_for_telegram(slots)

def cache_location(gym):
  return "cache/" + gym.value + ".json"

def refresh_all_gyms_information():
  # custom_gyms = [GymName.BOULDERGARTEN, GymName.BOULDERKLUB]
  # custom_gyms = [GymName.DER_KEGEL, GymName.SUEDBLOC]
  custom_gyms = gyms
  all_gyms_information = {gym.value: refresh_gym_information(gym, days_to_fetch={0,1,2}) for gym in custom_gyms}
  all_info_json = json.dumps(all_gyms_information, indent=4)
  with open("cache/all.json", "w+") as f:
    f.write(all_info_json)
  return all_info_json

def refresh_gym_information(gym: GymName, days_to_fetch: {int} = {0}):
  # assert days_to_fetch == {0,1,2,3,4,5,6}, "Currently only supporting refreshing info for all week, for simplicity"
  gym_information = {}
  start_time = time.time()
  driver = get_driver()
  driver.get(gyms[gym]["link"])
  time.sleep(2) # TODO: test without

  if gym == GymName.BOULDERGARTEN:
    prepare_bouldergarten(driver)

  for day_offset in days_to_fetch:
    date_to_check = date.today() + timedelta(days=day_offset)
    slots_per_day_html = []
    if gym_is_webclimber(gym):
      element = driver.find_element(By.XPATH, f"//td[text()='{date_to_check.day}']").click()
      time.sleep(2)
      element = driver.find_element(By.ID, "offerTimes")
      time.sleep(2)
      slots_html = element.get_attribute('outerHTML')
    else:
      element = driver.find_element(By.XPATH, f"//div[text()='\n\t\t\t\t\t\t\t\t{date_to_check.day}\n\t\t\t\t\t\t\t']").click()
      logger.info(f"{gym.value}: Opened slots for day {date_to_check}")
      element = driver.find_element(By.CSS_SELECTOR, ".drp-course-dates-list-wrap")
      slots_html = element.get_attribute('innerHTML')
    # save_slots_html_to_fixture(slots_html, gym, date_to_check)
    gym_information[str(date_to_check)] = process_slots_html(slots_html, gym)
  end_time = time.time()
  last_cached_timestamp = end_time
  logger.info(f"Checked {gym.value} for {len(days_to_fetch)} day(s) in {round(end_time - start_time, 2)}s")
  return gym_information


def prepare_bouldergarten(driver):
    # XXX: JS "clicks" vs "mouse" clicks()
    # 1. the issue that forced our usage of JS click might be resolved by waits)
    # 2. JS "clicks" don't seem to work on non-clickable HTML elems, while "mouse" clicks() do
    # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
    try:
      # XXX: The cookies banner was causing problems, but perhaps not on this webdriver.
      # Try without, otherwise note also that body has a class revealing cookie banner info
      driver.find_element(By.ID, "cn-accept-cookie").click()
      logger.info("Cookie banner accepted")
      # Older version below:
      # element = driver.find_element(By.ID, "cn-accept-cookie")
      # driver.execute_script("arguments[0].click();", element)
    except Exception as e: # XXX: Do not catch every exception
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


def process_slots_html(slots: str, gym: GymName):
  if gym_is_webclimber(gym):
    slots = re.sub('<[^>]*>', '', slots)
    slots = re.sub('Buchen', '\n', slots)
    slots = re.sub('Uhr', '- ', slots)
    lines = [line.strip() for line in slots.splitlines() if line.strip() != '']
    # slots = re.sub('mehr als 10 Plätze verfügbar', '10+ places', slots) # TODO: note down somewhere that 10 is 10+
    # slots = re.sub(r'^\s*S', 'a', slots) # TODO: figure out what this means
  else:
    slots = re.sub('<[^>]*>', '', slots)
    lines = [
      line.strip() for line in slots.splitlines()
      if len(re.sub(r'\s*', '', line)) > 0 # Clean up whitespace lines
      and not "Buchen" in line and not "begonnen" in line # Filter out extra lines for a consistent output
    ]
    date_strings = lines[2::3]
    status_strings = lines[::3]
    lines = [date + " - " + status for (date, status) in zip(date_strings, status_strings)]

  # XXX: this seems to refer to webclimber only
  if "keine plätze" in lines[0].lower():
    logger.info("caught no slots")
    slots_string = "None"
  else:
    def clean_num_slots(num_slots):
      num_slots = re.sub("[^0-9]", "", num_slots)
      return (0 if num_slots == "" else int(num_slots))

    info = [tuple(line.split(" - ")) for line in lines]
    info = [(start, end, clean_num_slots(num_slots)) for (start, end, num_slots) in info]
    info = filter(lambda i: i[2] != 0, info)

    if info == []:
      # XXX: Consider merging gaps just as multislots are merged. Depends on how data is presented later.
      slots_string = "None"
    else:
      slots =  [
          {
            "start_time": start,
            "end_time": end,
            "free_places": (0 if num_slots == "" else int(num_slots))
          } for (start, end, num_slots) in info
      ]

      slots = merge_slots_into_mutlislots(slots, None, [])
      slots_string = json.dumps(slots, indent=4)
  filename = cache_location(gym)
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  with open(filename, "w") as file:
      file.write(slots_string)
  return slots

def merge_slots_info_multislots_iterative(slots):
  # TODO: remove after playing with it (or not)
  """ Take a JSON-like list of slots and combine slots that are full (10+ places) into multi-slots"""
  multislots = []
  i = 0
  while i < len(slots) - 2:
    # Open a multislot
    multislot_start_time = slots[i]["start_time"]
    # Advance while on a slot that should be grouped (one with 10+ places)

    while slots[i]["free_places"] >= 10:
      print("  slot included")
      i += 1

    # When you reach one that shouldn't, the group should close before it
    multislots.append({
      "start_time": multislot_start_time,
      "end_time": slots[i-1]["end_time"],
      "free_places": slots[i-1]["free_places"] # Assigns from last in group, which is fine
    })

    i += 1

  return multislots

def merge_slots_into_mutlislots(slots, current_multislot, multislots):
  if slots == []:
    return multislots
  head, *tail = slots

  if head["free_places"] >= 10:
    # This slot should be added to a group, or open one
    # Open up a multislot, if it's not open yet
    if current_multislot == None:
      current_multislot = head
    else:
      # If a multislot is open, update its end_time
      current_multislot["end_time"] = head["end_time"]

    # If this is the last slot, close the multislot
    if tail == []:
      multislots.append(current_multislot)
    # Move on, removing one slot
    return merge_slots_into_mutlislots(tail, current_multislot, multislots)

  if head["free_places"] < 10:
    # This slot does not belong to a group
    # If there's an open mutlislot, close and save it
    if current_multislot != None:
      multislots.append(current_multislot)
      # print("Closed and appended a multislot")
    # print(f"On a normal slot, appending {head} to {multislots}")
    multislots.append(head)
    # Close the multislot by passing None, add current slot
    return merge_slots_into_mutlislots(tail, None, multislots)


def format_slot_information_for_telegram(slots):
  n_places_str = lambda i: "10+" if i >= 10 else str(i)
  return [
    slot["start_time"] + " - " + slot["end_time"] + " → " + n_places_str(int(slot["free_places"]))
    for slot in slots if int(slot["free_places"]) > 0
  ]


def save_slots_html_to_fixture(slots, gym, date):
  logger.info(f"Saving info for {gym.value} on {str(date)} to fixture")
  filepath = "fixtures/slots_" + gym.value + "_" + str(date) + ".html"
  with open(filepath, "w+") as file:
    file.write(slots)

def book(user):
  return "Coming soon!"
