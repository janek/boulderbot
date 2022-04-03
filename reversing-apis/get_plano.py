import os
import json
import requests
from enum import Enum
from gyms import GymName, gyms
from pprint import pprint
from datetime import datetime, date

### Request information
# https://backend.dr-plano.com/courses_dates?id=67359814&advanceToFirstMonthWithDates=&start=1646089200000&end=1648764000000
# id = 67359814 -> hall ID of Bouldergarten
# advanceToFirstMonthWithDates -> ???
# start = 1646089200000, GMT +1 -> March 1, 00:00:00
# end = 1648764000000, GMT +2 (because of daylifght savings time) -> April 1, 00:00:00

### Logic
# 1. Length for all requests (in March) seems to be the same per hall (543 for Bouldergarten, 561 for Boulderklub)
# 2. As of 13.03.22, there are 22(?) slots in a day at Bouldergarten, 24 at Boulderklub
# 3. (slot nrs side note) 561 - 543 == 18. (24 - 22) * 31 == 61. 18 != 61, so something's off, but whatever
# 4. For Bouldergarten, after filtering for 'active dates' slots, there are 161 left. 161/22 == 7.31, but 161/23 == 7

dr_plano_url = "https://backend.dr-plano.com"
class DrPlanoEndpoint(Enum):
  COURSES_DETAIL = "courses_detail"
  COURSES_DATES = "courses_dates"

class SlotStates(Enum):
  BOOKABLE = "BOOKABLE"
  NOT_BOOKABLE_ANYMORE = "NOT_BOOKABLE_ANYMORE"
  FULLY_BOOKED = "FULLY_BOOKED"
  NOT_YET_BOOKABLE = "NOT_YET_BOOKABLE"

def perform_dr_plano_request(endpoint: DrPlanoEndpoint, gym_name: GymName):
    if 'dr_plano_id' not in gyms[gym_name]:
        raise Exception("Not plano")
        # XXX: better error reporting

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br', # TODO: unzip, see jvns.ca
        'Origin' : gyms[gym_name]['link'], # (format is:) 'Origin': 'https://boulderklub.de',
        'Connection': 'keep-alive',
        'Referer' : gyms[gym_name]['link'] + "/", # (format is:) 'Referer': 'https://boulderklub.de/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Cache-Control': 'max-age=0' # This line was included in some requests, but not all. Keeping for now.
    }

    params = {'id' : gyms[gym_name]['dr_plano_id']}

    # TODO:DATES: Generate beginnings of the month in unix timestamp with extra zeros
    # Test values:
    # 1646089200000 - 1.03
    # 1648764000000 - 1.04
    # 1651356000000 - 1.05

    if endpoint.value == DrPlanoEndpoint.COURSES_DATES.value:
        # TODO: comparing by value is a workaround for https://stackoverflow.com/questions/26589805/python-enums-across-modules
        # It should not be necessary outside of testing, so this can be changed to "endpoint is endpoint"
        additional_params = {
            'advanceToFirstMonthWithDates': None,
            'start': '1648764000000',
            'end': '1651356000000',
        }
        params = params | additional_params

    # Adding parameters to the url
    # This should be handled by requests, but isn't at the moment (b/c of the :None)
    # https://github.com/psf/requests/issues/2651
    param_to_string = lambda key, value: f"{key}={value}" if value != None else key
    url_params_as_string = list([param_to_string(key,value) for (key, value) in params.items()])
    url = dr_plano_url + "/" + endpoint.value + "?"  + "&".join(url_params_as_string)
    print("Performing or simulating request for url: "+ url)
    res = requests.get(url, headers=headers)
    slots_info = json.loads(res.text)
    return slots_info

# perform_dr_plano_request(DrPlanoEndpoint.COURSES_DETAIL, GymName.BOULDERKLUB)
# perform_dr_plano_request(DrPlanoEndpoint.COURSES_DATES, GymName.BOULDERKLUB)

def convert_plano_schema_to_our_schema(slot_info: dict, gym: GymName):
  # Set a timezone for correctly interpretting timestamps regardless of physical location of the server
  os.environ['TZ'] = 'Europe/Berlin'

  # XXX: This would probably read cleaner as a filter and a helper "bookable?" function
  slot_info = [slot for slot in slot_info if slot['state'] not in [SlotStates.NOT_BOOKABLE_ANYMORE.value, SlotStates.NOT_YET_BOOKABLE.value]]
  new_slots_info = {}

  for slot in slot_info:
      start_timestamp = slot['dateList'][0]['start']/1000
      start_time_str = datetime.fromtimestamp(start_timestamp).strftime('%H:%M')

      end_timestamp = slot['dateList'][0]['end']/1000
      end_time_str = datetime.fromtimestamp(end_timestamp).strftime('%H:%M')

      free_places = slot['maxCourseParticipantCount'] - slot['currentCourseParticipantCount']
      slot_date_str = str(date.fromtimestamp(start_timestamp))
      free_places = max(free_places, 0) # Negative places are possible if they have a glitch, it seems
      save_slot(slot_date_str, start_time_str, end_time_str, free_places, new_slots_info)

  slots_info_per_hall = { gym.value : new_slots_info }
  return slots_info_per_hall

def save_slot(date_string, start_time, end_time, free_places, gym_info):
    slot_info = { 'start_time': start_time, 'end_time': end_time, 'free_places': free_places}
    if date_string not in gym_info:
          gym_info[date_string] = [slot_info]
    else:
          tmp = gym_info[date_string]
          tmp.append(slot_info)
          gym_info[date_string] = tmp
          # gym_info[date_string] = gym_info[date_string].append(slot_info)

# pprint(json_info)
def get_mock_data():
  FILENAME = 'bouldergarten_course_dates_2.json'
  with open(FILENAME, "r") as f:
      json_info = json.load(f)
      return json_info

def cache_slots_info(slots_info: dict):
  with open("../cache/all.json", "w+") as cache_file:
    json.dump(slots_info, cache_file, indent=4)

def cache_plano_slots_info(plano_slots_info: dict):
  with open("plano_stash.json", "w+") as f:
    json.dump(plano_slots_info, f, indent=4)

def update():
  gym = GymName.BOULDERGARTEN
  perform_dr_plano_request(DrPlanoEndpoint.COURSES_DETAIL, gym) # Perform this request to look more natural, ignore the result
  dr_plano_slots_info = perform_dr_plano_request(DrPlanoEndpoint.COURSES_DATES, gym)
  cache_plano_slots_info(dr_plano_slots_info)
  slots = convert_plano_schema_to_our_schema(dr_plano_slots_info, gym)
  cache_slots_info(slots)
