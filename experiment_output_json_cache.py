from gyms import process_dates_html, GymName, format_slot_information_for_telegram
from pprint import pprint
import re
import json

with open("fixtures/dates_dr_plano.html") as file:
    dates_html = file.read()

with open("fixtures/dates_webclimber.html") as file:
    dates_html_webclimber = file.read()

a = process_dates_html(dates_html, GymName.BOULDERGARTEN)
b = process_dates_html(dates_html_webclimber, GymName.DER_KEGEL)

# pprint(a)
# pprint(b)

with open("check_cache_test.json", "r") as file:
    slots = file.read()

print(format_slot_information_for_telegram(slots))
