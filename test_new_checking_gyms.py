import time
from gyms import get_gym_information, gyms, GymName

m = 2
t = time.time() - m * 60

a = get_gym_information(GymName.DER_KEGEL, force_last_cached_timestamp=t)
# TODO: test all halls with caching
# TODO: run boulderbot and test in practice

print(a)
