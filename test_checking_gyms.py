import time
from gyms import get_gym_information, gyms, GymName

# m = 2
# t = time.time() - m * 60
# TODO: test caching by optionally forcing refresh (by providing time or just force refresh)

def test_bouldergarten():
    get_gym_information(GymName.BOULDERGARTEN)
    return True

def test_boulderklub():
    get_gym_information(GymName.BOULDERKLUB)
    return True

def test_suedbloc():
    get_gym_information(GymName.SUEDBLOC)
    return True

def test_der_kegel():
    get_gym_information(GymName.DER_KEGEL)
    return True
