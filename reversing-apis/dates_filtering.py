import json
from pprint import pprint
from enum import Enum
from datetime import datetime, date
import os

FILENAME = 'bouldergarten_course_dates_2.json'
with open(FILENAME, "r") as f:
     json_info = json.load(f)

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

# Set a timezone for correctly interpretting timestamps regardless of physical location of the server
os.environ['TZ'] = 'Europe/Berlin'

class SlotStates(Enum):
  BOOKABLE = "BOOKABLE"
  NOT_BOOKABLE_ANYMORE = "NOT_BOOKABLE_ANYMORE"
  FULLY_BOOKED = "FULLY_BOOKED"
  NOT_YET_BOOKABLE = "NOT_YET_BOOKABLE"

json_info = [slot for slot in json_info if slot['state'] not in [SlotStates.NOT_BOOKABLE_ANYMORE.value, SlotStates.NOT_YET_BOOKABLE.value]]

# pprint(json_info)
gym_info = {}

def save_slot(date_string, start_time, end_time, free_places):
     slot_info = { 'start_time': start_time, 'end_time': end_time, 'free_places': free_places}
     if date_string not in gym_info:
          gym_info[date_string] = [slot_info]
     else:
          tmp = gym_info[date_string]
          tmp.append(slot_info)
          gym_info[date_string] = tmp
          # gym_info[date_string] = gym_info[date_string].append(slot_info)

for slot in json_info:
     start_timestamp = slot['dateList'][0]['start']/1000
     start_time_str = datetime.fromtimestamp(start_timestamp).strftime('%H:%M')

     end_timestamp = slot['dateList'][0]['end']/1000
     end_time_str = datetime.fromtimestamp(end_timestamp).strftime('%H:%M')

     free_places = slot['maxCourseParticipantCount'] - slot['currentCourseParticipantCount']
     slot_date_str = str(date.fromtimestamp(start_timestamp))
     if free_places < 0:
          print(start_time_str, slot_date_str)
          print(f"wtf, {slot['maxCourseParticipantCount']}, {slot['currentCourseParticipantCount']}")
          # XXX: remove comments, use min()
          free_places = 0
     save_slot(slot_date_str, start_time_str, end_time_str, free_places)

pprint(gym_info)
# with open('tmp.json', 'w') as ff:
#      ff.write(json.dumps(json_info))
