from selenium_helpers import process_dates, process_dates_webclimber
from pprint import pprint
import re
import json

with open("fixtures/dates_dr_plano.html") as file:
    dates_html = file.read()

with open("fixtures/dates_webclimber.html") as file:
    dates_html_webclimber = file.read()

def process_dates(dates):
  # save_dates_to_fixture(dates, source="dr_plano")
  dates = re.sub('<[^>]*>', '', dates)
  lines = [line.strip() for line in dates.splitlines() if len(re.sub('\s*', '', line)) > 0 and not "Buchen" in line and not "begonnen" in line]
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

  with open("outtest.json", "w+") as file:
      file.write(json.dumps(slots))

process_dates(dates_html)
