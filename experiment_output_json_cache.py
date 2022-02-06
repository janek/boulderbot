from gyms import process_dates, process_dates_webclimber
from pprint import pprint
import re
import json

with open("fixtures/dates_dr_plano.html") as file:
    dates_html = file.read()

with open("fixtures/dates_webclimber.html") as file:
    dates_html_webclimber = file.read()

process_dates(dates_html)
