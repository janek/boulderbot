from gyms import gyms, GymName, refresh_gym_information, refresh_all_gyms_information, process_slots_html
from pprint import pprint

# x = refresh_gym_information(gym = GymName.BOULDERGARTEN, days_to_fetch = {2})
# pprint(x)
# refresh_all_gyms_information()

with open("./fixtures/BG1.html", "r") as f:
    html = f.read()
    pprint(process_slots_html(html, GymName.BOULDERGARTEN))
