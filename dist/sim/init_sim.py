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
NUM_ROBOTS = 200
NUM_CREW = 0
headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def init_datastreams(id):
    #print("creating datastream for %d" %id)
    datas = [
        {
            "name": "CPU_TEMP_stream_%d" %id,
            "description": "Datastream for recording temperature",
            "observationType": r'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
            "unitOfMeasurement": {
                "name": "Degree Celsius",
                "symbol": "degC",
                "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius"
            },
            "Thing":{"@iot.id":id},
            "ObservedProperty":{"@iot.id":848},
            "Sensor":{"@iot.id":846}
        },
        {
            "name": "POWER_DRAW_stream_%d" %id,
            "description": "Datastream for recording pressure",
            "observationType": r'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
            "unitOfMeasurement": {
                "name": "kiloPascal",
                "symbol": "kPa",
                "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#KiloPascal"
            },
            "Thing":{"@iot.id":id},
            "ObservedProperty":{"@iot.id":849},
            "Sensor":{"@iot.id":847}
        },
        {
            "name": "HP_stream_%d" %id,
            "description": "Health percentage",
            "observationType": r'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
            "unitOfMeasurement": {
                "name": "percentage",
                "symbol": "%",
                "definition": "https://en.wikipedia.org/wiki/Percentage"
            },
            "Thing":{"@iot.id":id},
            "ObservedProperty":{"@iot.id":9854},
            "Sensor":{"@iot.id":9851}
        }
    ]

    for data in datas:
        try:
            r = requests.post(url = "http://routescout.sensorup.com/v1.0/Datastreams", json = data, headers = headers)
            logging.debug(r.json())
            if (r.status_code >= 200) and (r.status_code < 300):
                ds = r.json()["name"]
                #print(ds)
                logging.debug("Datastream %s created" % ds)
        except:
            logging.exception("Request to create Datastream %s failed." % data["name"])
            print("error creating datastream %s" %data["name"])

def init_sensors():
    datas = [
        {
            "name": "THERMOMETER",
            "description": "THERMOMETER temperature sensor in celcius ",
            "encodingType": "application/pdf",
            "metadata": "https://en.wikipedia.org/wiki/Thermometer"
        },
        {
            "name": "BAROMETER",
            "description": "BAROMETER pressure sensor in kPa",
            "encodingType": "application/pdf",
            "metadata": "https://en.wikipedia.org/wiki/Barometer"
        },
        {
            "name": "HP",
            "description": "HEALTH PERCENTAGE calculated by monitor",
            "encodingType": "application/pdf",
            "metadata": "https://en.wikipedia.org/wiki/Percentage"
        }
    ]

    for data in datas:
        try:
            r = requests.post(url = "http://routescout.sensorup.com/v1.0/Sensors", json = data, headers = headers)
            logging.debug(r.json())
            if (r.status_code >= 200) and (r.status_code < 300):
                sensor = r.json()["name"]
                #print(sensor)
                logging.debug("Sensor %s created" % sensor)
        except:
            logging.exception("Request to create Sensor %s failed." % data["name"])
            print(data["name"])

def init_observedProperties():
    datas = [
        {
            "name": "Area Temperature",
            "description": "The degree or intensity of heat present in the area",
            "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AreaTemperature"
        },
        {
            "name": "Air pressure",
            "description": "The degree or intensity of pressure in the air",
            "definition": "https://en.wikipedia.org/wiki/Atmospheric_pressure"
        },
        {
            "name": "Robot Health",
            "description": "The percentage health of a robot",
            "definition": "https://en.wikipedia.org/wiki/Percentage"
        }
    ]

    for data in datas:
        try:
            r = requests.post(url = "http://routescout.sensorup.com/v1.0/ObservedProperties", json = data, headers = headers)
            logging.debug(r.json())
            if (r.status_code >= 200) and (r.status_code < 300):
                op = r.json()["name"]
                #print(op)
                logging.debug("ObsProp %s created" % op)
        except:
            logging.exception("Request to create ObsProp %s failed." % data["name"])
            print("error creating %s" % data["name"])

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
        data = {"name": "Crew" + str(i), "description": "[]", "properties": {"route": []}}
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
        robot_list.append(robot)
    with open(r'data/robot.data', 'wb') as fout:
        pickle.dump(robot_list, fout)

""" initialize dataSim.data file """
""" fills dataSim.data with the iotid of all datastreams and psn: 0 """
def initSimData():
    #get all datastreams from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Datastreams?$top=50000", headers = headers)      
        #print("getting datastreams")
    except:
        print("error: datastreams at 1")
        exit()

    #get all datastreams in json form
    datastreams = rd.json()["value"]

    #empty list for initializing datastream id's in pickle
    ds_list = []

    for datastream in datastreams:
        #get id of datastream
        id = datastream["@iot.id"]
        rand = random.randint(0,17)
        ds = {"iotid": id, "psn": rand }
        ds_list.append(ds)
    
    #print(ds_list)
    with open(r'data/dataSim.data', 'wb') as f:
        pickle.dump(ds_list, f)

def initRobotStatusData():
    # Make list of all robots
    bot_list = []
    try:
        r = requests.get(url = "http://routescout.sensorup.com/v1.0/Things?$top=1000", headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            responseJSON = r.json()
            things = responseJSON["value"]
            for thing in things:
                if "status" in thing["properties"]:
                    bot = {"iotid": thing["@iot.id"], "status": thing["properties"]["status"], "count": 10}
                    bot_list.append(bot)                 
    except:
        logging.exception("Failed getting list of robots")
    
    #save in data file
    with open(r'data/robotStatus.data', 'wb') as f:
        pickle.dump(bot_list, f)

def initRobotStatus():
    # Make list of all robots
    bot_id = []
    try:
        r = requests.get(url = "http://routescout.sensorup.com/v1.0/Things?$top=1000", headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            responseJSON = r.json()
            things = responseJSON["value"]
            for thing in things:
                if "status" in thing["properties"]:
                    bot_id.append(thing["@iot.id"])                 
    except:
        logging.exception("Failed getting list of robots")
       
    #change all robot status to healthy
    for id in bot_id:
        try:
            data = {"properties" : {"status":"Healthy"}}
            r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%s)" % id, json = data, headers = headers)
            if (r.status_code >= 200) and (r.status_code < 300):
                logging.debug("Healed robot %s" % id)
        except:
            logging.exception("Init_sim initRobotStatus() failed")


def main():
    """
    please only initialize sensors and observed properties once!
    Running them more than once will create dublicates only that have diff iot.id's
    """
    init_sensors()
    init_observedProperties()
    create_crews()
    create_robots()
    initSimData()
    initRobotStatusData()
    initRobotStatus()

    


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
