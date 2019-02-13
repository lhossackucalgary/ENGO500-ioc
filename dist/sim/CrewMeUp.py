"""
Make a crew (login through phone, not simulated -- add ids to database after running)
"""
import os
import logging
import requests
from util import *

def go():
    headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

    crew = {"name": "Lucas Hossack"}
    data = {"name": "%s" % crew["name"], "description": "%s lhossack" % crew["name"], "properties": {"route": []}}
    try:
        r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things", json = data, headers = headers)
        print(r.json())
        if (r.status_code >= 200) and (r.status_code < 300):
            crew["iotid"] = r.json()["@iot.id"]
            logging.debug("Adding crew: %s as iotid: %s" % (crew["name"], crew["iotid"]))
    except:
        logging.exception("Request to create Crew %d failed." % crew["name"])

    crew["coordinates"] = set_location(crew["iotid"], [0,0])


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Adding crew")
    go()
    logging.info("Add crew complete")
