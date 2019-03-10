"""
Polls the server checking data from all robot Things
Updates robot's properties > status ("Healthy" | "Warning" | "Error")?
"""
import os
import logging
import requests
import random
import pickle

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def breakMeMaybe(id):
    if random.randint(0,100) < 50:
        try:
            data = {"properties" : {"status":"SICK AF"}}
            r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%s)" % id, json = data, headers = headers)
            if (r.status_code >= 200) and (r.status_code < 300):
                return True
                logging.debug("Broke robot %s" % id)
        except:
            logging.exception("Monitor breakMeMaybe failed")
    else:
        try:
            data = {"properties" : {"status":"Healthy"}}
            r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%s)" % id, json = data, headers = headers)
            if (r.status_code >= 200) and (r.status_code < 300):
                logging.debug("Healthy robot %s" % id)
        except:
            logging.exception("Monitor breakMeMaybe failed")



def main():
    """ break some bots (Please improve when... possible) """
    # Make list of all robots
    bot_list = []
    crew_list = []
    try:
        r = requests.get(url = "http://routescout.sensorup.com/v1.0/Things", headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            responseJSON = r.json()
            things = responseJSON["value"]
            for thing in things:
                if "status" in thing["properties"]:
                    bot_list.append(thing["@iot.id"])
                elif "route" in thing["properties"]:
                    crew_list.append(thing["@iot.id"])
    except:
        logging.exception("Failed getting list of robots")

    broken_bots = []

    # Update this part.. (don't break randomly - do some data analysis/ logic)
    for robot in bot_list:
        if breakMeMaybe(robot):
            broken_bots.append(robot)


    # Don't change: Output crew_list and broken_bots
    route_info = {"crew_list": crew_list, "broken_bots": broken_bots}
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd+'/../route/monitor_out.data', 'wb') as fout:
        pickle.dump(route_info, fout)


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/monitor.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Monitor service task started")
    main()
    logging.info("Monitor service task ended")
