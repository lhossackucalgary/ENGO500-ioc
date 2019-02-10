"""
Crew updates
"""
from util import *
import logging
import requests
import pickle


def update_crews():
    crews = load_data(r'./data/crew.data')
    for crew in crews:
        # GET next robot crew is moving to
        logging.debug("Getting crew props..")
        id = crew["iotid"]
        try:
            r = requests.get(url = "http://routescout.sensorup.com/v1.0/Things(%d)" % id, headers = headers)
            if (r.status_code >= 200) and (r.status_code < 300):
                props = r.json()["properties"]
                logging.debug(props)
                if ("route" in props) and (len(props["route"]) > 0):
                    nextbot = props["route"][0]
                else:
                    nextbot = -1
            else:
                nextbot = -1
            logging.debug("Next robot for crew %d: %d" % (id, nextbot))
        except:
            logging.exception("Failed getting crew (Thing %d's) destination" % id)
            continue

        # ifexists, GET location of next robot in line, else set next_robot_loc to current_loc
        try:
            r = requests.get(url = "http://routescout.sensorup.com/v1.0/Things(%d)/Locations" % nextbot, headers = headers)
            if (r.status_code >= 200) and (r.status_code < 300):
                loc = r.json()["value"][0]["location"]
                logging.debug(loc)
                if ("coordinates" in loc) and (len(loc["coordinates"]) == 2):
                    destination = loc["coordinates"]
                else:
                    destination = crew["coordinates"]
            else:
                destination = crew["coordinates"]
        except:
            logging.exception("Failed getting crew (Thing %d's) destination" % id)
            continue

        # calc new location
        print(destination)
        print(crew["coordinates"])

        # POST new location
