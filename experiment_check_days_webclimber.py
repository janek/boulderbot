from gyms import gyms, GymName, refresh_gym_information
from pprint import pprint


pprint(refresh_gym_information(gym = GymName.DER_KEGEL, days_to_fetch = {0, 1, 4}))
