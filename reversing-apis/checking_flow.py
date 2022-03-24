import requests
from enum import Enum
# TODO: check other halls for max-age

def first_boulderklub():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://boulderklub.de',
        'Connection': 'keep-alive',
        'Referer': 'https://boulderklub.de/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Cache-Control': 'max-age=0',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'id': '67361411',
    }

    response = requests.get('https://backend.dr-plano.com/courses_detail', headers=headers, params=params)


class DrPlanoEndpoint(Enum):
  COURSES_DETAIL = "courses_detail"
  COURSES_DATES = "courses_dates"

def perform_dr_plano_request(endpoint: DrPlanoEndpoint, gym_name: GymName):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        # 'Origin': 'https://boulderklub.de',
        'Origin' : gyms[gym_name]['link'],
        'Connection': 'keep-alive',
        # 'Referer': 'https://boulderklub.de/',
        'Referer' : gyms[gym_name]['link'] + "/",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        # 'Cache-Control': 'max-age=0', XXX: do we want this always? prob not
    }
    params = {} if
