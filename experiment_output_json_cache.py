from gyms import process_dates, process_dates_webclimber, process_dates_html, GymName
from pprint import pprint
import re
import json

with open("fixtures/dates_dr_plano.html") as file:
    dates_html = file.read()

with open("fixtures/dates_webclimber.html") as file:
    dates_html_webclimber = file.read()

a = process_dates_html(dates_html, GymName.BOULDERGARTEN)
b = process_dates_html(dates_html_webclimber, GymName.DER_KEGEL)

pprint(a)
pprint(b)
