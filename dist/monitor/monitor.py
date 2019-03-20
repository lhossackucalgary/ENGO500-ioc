"""
Polls the server checking data from all robot Things
Updates robot's properties > status ("Healthy" | "Warning" | "Error")?
"""
import os
import logging
import requests
import random
import csv
import pickle
import datetime
import re
from util import *

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

""" grabs all robot status from API """
def grabAllRobotStatus():
    # Make list of all robots and status
    bot_list = []
    try:
        r = requests.get(url = "http://routescout.sensorup.com/v1.0/Things", headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            responseJSON = r.json()
            things = responseJSON["value"]
            for thing in things:
                if "status" in thing["properties"]:
                    bot = {"iotid": thing["@iot.id"], "status": thing["properties"]["status"]}
                    bot_list.append(bot)
    except:
        logging.exception("Failed getting list of robots")

    #save in data file
    #print(bot_list)
    with open(r'../sim/data/robotStatus.data', 'wb') as f:
        pickle.dump(bot_list, f)

""" patch robot status to Healthy on API """
def switchtoHealthy(stat):
    try:
        id = stat["iotid"]
        data = {"properties" : {"status":"Healthy"}}
        r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%s)" % id, json = data, headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            logging.debug("Robot %s switched to: Healthy" % id)
    except:
        logging.exception("Monitor switchtoHealthy failed")

""" patch robot status to Warning on API """
def switchtoWarning(stat):
    try:
        id = stat["iotid"]
        data = {"properties" : {"status":"Warning"}}
        r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%s)" % id, json = data, headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            logging.debug("Robot %s switched to: Warning" % id)
    except:
        logging.exception("Monitor switchtoWarning failed")

""" patch robot status to Urgent on API """
def switchtoUrgent(stat):
    try:
        id = stat["iotid"]
        data = {"properties" : {"status":"Urgent"}}
        r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%s)" % id, json = data, headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            logging.debug("Robot %s switched to: Urgent" % id)
    except:
        logging.exception("Monitor switchtoUrgent failed")

""" updates all robot status depending on set probabilities """
def updateRobotStatus():
    #get updated robot status data
    #cwd = os.path.dirname(os.path.realpath(__file__))
    robotStats = load_data(r'../sim/data/robotStatus.data')

    # Make list of all robots
    for stat in robotStats:
        if (stat["status"] == "Healthy"):
            if random.randint(1,100) > 80:
                switchtoWarning(stat)
            if random.randint(1,100) > 95:
                switchtoUrgent(stat)

        if (stat["status"] == "Warning"):
            if random.randint(1,100) > 70:
                switchtoUrgent(stat)

        if (stat["status"] == "Unknown"):
            if random.randint(1,100) > 60:
                switchtoHealthy(stat)
            else:
                switchtoWarning(stat)

    #update robotStatus.data
    grabAllRobotStatus()

""" reset all Robot Status to Healthy """
def resetRobotStatus():
    #get updated robot status data
    robotStats = load_data(r'../sim/data/robotStatus.data')

    # Make list of all robots
    for stat in robotStats:
        switchtoHealthy(stat)

    #update robotStatus.data
    grabAllRobotStatus()

""" get all robots with Urgent status from robotStatus.data """
def getUrgentRobots():
    robotStats = load_data(r'../sim/data/robotStatus.data')
    urgentBots = []

    for stat in robotStats:
        if stat["status"] == "Urgent":
            urgentBots.append(stat["iotid"])

    #print(urgentBots)
    return urgentBots

""" get all robots with Warning status from robotStatus.data """
def getWarningRobots():
    robotStats = load_data(r'../sim/data/robotStatus.data')
    warningBots = []

    for stat in robotStats:
        if stat["status"] == "Warning":
            warningBots.append(stat["iotid"])

    #print(warningBots)
    return warningBots

def getRobotDatastreams(id):
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Things(%d)/Datastreams" %id, headers = headers)      
        #print("getting datastreams")
    except:
        print("error: datastreams at 1")
        exit()

    #get all datastreams in json form
    datastreams = rd.json()["value"]
    return datastreams

def getDatastreamObs(id):
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Datastreams(%d)/Observations" %id, headers = headers)      
    except:
        print("error: getting datastream obs in getDatastreamObs(id) for %d" %id)
        exit()

    #get all obs in json form
    obs = rd.json()["value"]
    return obs

def getObsResult(id):
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Observations(%d)" %id, headers = headers)      
    except:
        print("error: getting result in getObsResult(id) for %d" %id)
        exit()

    #get all obs in json form
    obs = float(rd.json()["result"])
    return obs

def calcRobotHP():
    #before writing, need to create datastream and obsType for health
    time = datetime.datetime.now().replace(microsecond=0).isoformat()
    """ get list of all robots """
    robotStats = load_data(r'../sim/data/robotStatus.data')
    """ for each robot, get list of datastreams """
    for bot in robotStats:
        datastreams = getRobotDatastreams(bot["iotid"])
        """ for each datastream, check type of sensor (pressure, temp, etc) """
        hp_total = None
        hp_temp = None
        hp_pres = None
        for datastream in datastreams:
            desc = datastream["description"]
            id = datastream["@iot.id"]
            if (desc == "Datastream for recording pressure"):
                obs = getDatastreamObs(id)
                r = getObsResult(obs[0]["@iot.id"])
                """ calculate hp for pressure """
                """ compare to ideal pressure/temp value to get a percentage """
                a = 5.0 #ideal value
                b = 36.0 #nonideal value
                hp_pres = (( b - a) - abs(r - a))/(b - a)*100.0

            if (desc == "Datastream for recording temperature"):
                obs = getDatastreamObs(id)
                r = getObsResult(obs[0]["@iot.id"])
                """ calculate hp for pressure """
                """ compare to ideal pressure/temp value to get a percentage """
                a = 20.0
                b = 36.0
                hp_temp = ((b-a) - abs(r-a))/(b-a)*100.0
        
        """ average all percentages from all datastreams from the robot """
        hp_total = (hp_pres + hp_temp)/2

        """ post resulting percentage as HP of robot as Observation """
        data = {
                "phenomenonTime": "%s.000Z" %time,
                "resultTime" : "%s.000Z" %time,
                "result" : hp_total,
                "Datastream":{"@iot.id":id}
            }
        try:
            r = requests.post(url = "http://routescout.sensorup.com/v1.0/Observations", json = data, headers = headers)
            logging.debug(r.json())
            if (r.status_code >= 200) and (r.status_code < 300):
                ds = r.json()["Datastream"]
                #print(ds)
                logging.debug("Obs created for datastream id: %s" % ds)
        except:
            #print("error: could not post observation of value: %d to datastream id: %d" %(sid[rand], id))
            #error occurs because feature of interest is not defined (is mandatory but has default value)
            logging.debug("Obs created for datastream id: %s but contains error (no feature of interest?)" % id)

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

    """caclulate health of robots as observation"""
    """(this is done before updateRobotStatus, as it should correlate to prior robot sim data)"""
    calcRobotHP()
    """grab current robot status from API"""
    grabAllRobotStatus()
    """run this to reset robot status to healthy"""
    #resetRobotStatus()
    """make some robots sick"""
    updateRobotStatus()

    """get ids of broken bots (aka bots with warning and urgent status)"""
    broken_bots = getUrgentRobots()
    warning_bots = getWarningRobots()
    for botid in warning_bots:
        broken_bots.append(botid)

    """ UPDATE LATER: should probably seperate warning_bots in monitor_out at some point!! """

    # Don't change: Output crew_list and broken_bots
    route_info = {"crew_list": crew_list, "broken_bots": broken_bots}
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd+'/../route/monitor_out.data', 'wb') as fout:
        pickle.dump(route_info, fout)

    """ add file of robotStats to routing """
    robotStats = load_data(r'../sim/data/robotStatus.data')
    with open(cwd+'/../route/monitor_out2.data', 'wb') as fout:
        pickle.dump(robotStats, fout)

if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/monitor.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Monitor service task started")
    main()
    logging.info("Monitor service task ended")
