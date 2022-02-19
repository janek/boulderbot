from gyms import group_full_slots, rec
import json
from pprint import pprint

with open("cache/Suedbloc.json", "r") as f:
    slots = f.read()
    slots = json.loads(slots)

# print(group_full_slots(slots))

multislots = rec(slots, current_multislot=None, multislots=[])
pprint(multislots)
