"""
init_sim.py
Initializes simulator data on SensorThings API server.
This file runs ONCE at the beginning of a simulation. sim_main.py runs
repeatedly throughout the simulation.
- Creates crews with an initial location. Crews do not have data streams.
- Creates robots with initial location. Creates & initializes data streams
and sensors for robots.
"""
import logging
import os
import requests
import pickle
import random
from util import *


#Globals
NUM_ROBOTS = 1
NUM_CREW = 1
headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def init_datastreams(id):
    """
    TODO: Implement datastream creation for robot. If we need any information
    regarding this data stream to simulate info, return it. eg. iotid
    """
    pass

def init_sensors(id):
    """
    TODO: Implement sensor creation for robot. If we need any information
    regarding this data stream to simulate info, return it. eg. iotid
    """
    pass

def init_location(id):
    """
    Create an initial location in Calgary for a crew or a robot
    @param[in]  Thing id to give a random location
    @return     (lat,lon)
    """
    return set_location(id, (random.randint(-11420837, -11393371)/1.0e5,
                        random.randint(5091912, 5114782)/1.0e5))

def create_crews():
    """
    Creates crews with an initial location. Crews do not have data streams.
    """
    crew_list = []
    for i in range(0, NUM_CREW):
        crew = {"name": "Crew" + str(i)}
        data = {"name": "Crew" + str(i), "description": "Crew " + str(i), "properties": {"route": []}}
        try:
            r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things", json = data, headers = headers)
            logging.debug(r.json())
            if (r.status_code >= 200) and (r.status_code < 300):
                crew["iotid"] = r.json()["@iot.id"]
                logging.debug("Crew Thing %d created" % crew["iotid"])
        except:
            logging.exception("Request to create Crew %d failed." % i)
        crew["coordinates"] = init_location(crew["iotid"])
        crew_list.append(crew)
    with open(r'data/crew.data', 'wb') as fout:
        pickle.dump(crew_list, fout)


def create_robots():
    """
    Creates robots with initial location. Creates & initializes data streams
    and sensors for robots.
    """
    robot_list = []
    for i in range(0, NUM_ROBOTS):
        robot = {"name": "robot" + str(i)}
        data = {"name": "robot" + str(i), "description": "robot " + str(i), "properties": {"status": "Healthy"}}
        try:
            r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things", json = data, headers = headers)
            logging.debug(r.json())
            if (r.status_code >= 200) and (r.status_code < 300):
                robot["iotid"] = r.json()["@iot.id"]
                logging.debug("Robot Thing %d created" % robot["iotid"])
        except:
            logging.exception("Request to create robot %d failed." % i)
        init_location(robot["iotid"])

        # TODO: Encode datastream and sensor initialization output (if needed)
        # into robot dictionary for saving.. eg. iotid of datastream and sensors
        # and current values + any meta-data required for simulation model
        init_datastreams(robot["iotid"])
        init_sensors(robot["iotid"])
        robot_list.append(robot)
    with open(r'data/robot.data', 'wb') as fout:
        pickle.dump(robot_list, fout)


def main():
    create_crews()
    create_robots()


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
