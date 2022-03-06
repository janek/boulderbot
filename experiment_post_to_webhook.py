from gyms import gyms, GymName, refresh_gym_information, refresh_all_gyms_information, process_slots_html
from pprint import pprint
import requests
import json
import schedule
import logging
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

info = {"Janek": "cool", "Heroku" : "also cool"}
info_json = json.dumps(info, indent=4)
# info_json = refresh_all_gyms_information()
# print(res)
# curl https://typedwebhook.tools/webhook/2f6ade5e-a382-43cc-b860-a92c3f0a1f4e -X POST --data '{"name":"Test event","data":{"id":1,"name":"Tester McTestFace","by":"Inngest","at":"2022-03-06T08:23:17.172Z"},"user":{"email":"tester@example.com"},"ts":1646554997172}'

def job():
    res = requests.post('https://webhook.site/51beee18-e899-48b2-9d54-1b8120ecedde', data=info_json)
    logger.info("Job done, " + str(res))

schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
