import requests
from enum import Enum
from gyms import GymName, gyms

dr_plano_url = "https://backend.dr-plano.com"
class DrPlanoEndpoint(Enum):
  COURSES_DETAIL = "courses_detail"
  COURSES_DATES = "courses_dates"

def perform_dr_plano_request(endpoint: DrPlanoEndpoint, gym_name: GymName):
    if 'dr_plano_id' not in gyms[gym_name]:
        raise Exception("Not plano")
        # XXX: better error reporting

    shared_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br', # TODO: unzip, see jvns.ca
        'Origin' : gyms[gym_name]['link'], # (format is:) 'Origin': 'https://boulderklub.de',
        'Connection': 'keep-alive',
        'Referer' : gyms[gym_name]['link'] + "/", # (format is:) 'Referer': 'https://boulderklub.de/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Cache-Control': 'max-age=0' # This line was included in some requests, but not all. Keeping for now.
    }
    params = {'id' : gyms[gym_name]['dr_plano_id']}

    # TODO: Generate beginnings of the month in unix timestamp with extra zeros
    # Test values:
    # 1646089200000 - 1.03
    # 1648764000000 - 1.04
    # 1651356000000 - 1.05

    if endpoint == DrPlanoEndpoint.COURSES_DATES:
        additional_params = {
            'advanceToFirstMonthWithDates': None,
            'start': '1648764000000',
            'end': '1651356000000',
        }
        params = params | additional_params

    # This should be handled by requests, but isn't at the moment (b/c of the :None)
    # https://github.com/psf/requests/issues/2651
    param_to_string = lambda key, value: f"{key}={value}" if value != None else key
    url_params_as_string = list([param_to_string(key,value) for (key, value) in params.items()])
    url = dr_plano_url + "/" + endpoint.value + "?"  + "&".join(url_params_as_string)
    print(url)

# perform_dr_plano_request(DrPlanoEndpoint.COURSES_DETAIL, gym_name=GymName.DER_KEGEL)

perform_dr_plano_request(DrPlanoEndpoint.COURSES_DETAIL, gym_name=GymName.BOULDERGARTEN)
perform_dr_plano_request(DrPlanoEndpoint.COURSES_DATES, gym_name=GymName.BOULDERGARTEN)

perform_dr_plano_request(DrPlanoEndpoint.COURSES_DETAIL, gym_name=GymName.BOULDERKLUB)
perform_dr_plano_request(DrPlanoEndpoint.COURSES_DATES, gym_name=GymName.BOULDERKLUB)
