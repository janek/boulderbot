from enum import Enum

class GymName(Enum):
  DER_KEGEL = "Der Kegel"
  SUEDBLOC = "Suedbloc"
  BOULDERGARTEN = "Bouldergarten"
  BOULDERKLUB = "Boulderklub"

gyms = {
    GymName.DER_KEGEL : {
        "emoji": "🔺",
        "link": "https://168.webclimber.de/de/booking/offer/bouldern-urban-sports-club",
    },
    GymName.SUEDBLOC : {
        "emoji": "⚪️",
        "link": "https://141.webclimber.de/de/booking/offer/boulderslots-gesamt",
    },
    GymName.BOULDERGARTEN : {
        "emoji": "🍃",
        "link": "https://bouldergarten.de",
        "dr_plano_id": "67359814",
    },
    GymName.BOULDERKLUB : {
        "emoji": "♣",
        "link": "https://boulderklub.de",
        "dr_plano_id": "67361411",
    },
}

def gym_is_webclimber(gym: GymName):
  return "webclimber" in gyms[gym]['link']
