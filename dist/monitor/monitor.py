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
allData = []

""" grabs all robot status from API """
def grabAllRobotStatus():
    # Make list of all robots and status
    bot_list = []
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Things?$top=1000", headers = headers)      
        things = rd.json()["value"]
        for thing in things:
            if "status" in thing["properties"]:
                bot = {"iotid": thing["@iot.id"], "status": thing["properties"]["status"]}
                bot_list.append(bot)
    except:
        print("error: datastreams at 1")
        exit()

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
            if random.randint(1,100) > 90:
                switchtoWarning(stat)
            if random.randint(1,100) > 97:
                switchtoUrgent(stat)

        if (stat["status"] == "Warning"):
            if random.randint(1,100) > 85:
                switchtoUrgent(stat)

        if (stat["status"] == "Unknown"):
            if random.randint(1,100) > 92:
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
    datastreams = None
    for thing in allData:
        if (thing["@iot.id"] == id):
            datastreams = thing["Datastreams"]
    if (datastreams == None): 
        print("error in getRobotDatastreams(id)")
        exit()
    return datastreams

def getDatastreamObs(id):
    obs = None
    for thing in allData:
        for ds in thing["Datastreams"]:
            if (ds["@iot.id"] == id):
                obs = ds["Observations"]
    if (obs == None):
        print("error in DatastreamObs")
        exit()
    return obs

def getObsResult(id):
    result = None
    for thing in allData:
        for ds in thing["Datastreams"]:
            for obs in ds["Observations"]:
                if (obs["@iot.id"] == id):
                    result = obs["result"] #may need float(obs["result"])
    if (result == None):
        print("error in getObsResult(id)")
        exit()
    return result

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
        HP_id = None
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

            if (desc == "Health percentage"):
                HP_id = id

        """ average all percentages from all datastreams from the robot """
        hp_total = (hp_pres + hp_temp)/2
        hp_total =float("{0:.2f}".format(hp_total))
        if (hp_total < 0):
            hp_total = 0
        #print(hp_total)

        if (HP_id != None):
            """ post resulting percentage as HP of robot as Observation """
            data = {
                    "phenomenonTime": "%s.000Z" %time,
                    "resultTime" : "%s.000Z" %time,
                    "result" : hp_total,
                    "Datastream":{"@iot.id":HP_id}
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
                logging.debug("Obs created for datastream id: %s but contains error (no feature of interest?)" % HP_id)
        else:
            print("error retreiving HP datastream iotid for %d" %bot["iotid"])

def getAllData():

    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Things?$top=1000&$expand=Datastreams", headers = headers)      
        all_th_ds = rd.json()["value"]
    except:
        print("error: datastreams at 1")
        exit()
    
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Datastreams?$top=5000&$expand=Observations&$top=50000", headers = headers)      
        all_ds_ob = rd.json()["value"]
    except:
        print("error: datastreams at 2")
        exit()
    
    c1 = 0
    c2 = 0
    for th_ds in all_th_ds:
        for ds in th_ds["Datastreams"]:
            for ds_ob in all_ds_ob:
                if (ds["@iot.id"] == ds_ob["@iot.id"]):
                    all_th_ds[c1]["Datastreams"][c2] = ds_ob
            c2 = c2 + 1
        c2 = 0
        c1 = c1 + 1
    
    global allData
    allData = all_th_ds  

def main():

    """ break some bots (Please improve when... possible) """
    # Make list of all robots
    bot_list = []
    crew_list = []
    try:
        r = requests.get(url = "http://routescout.sensorup.com/v1.0/Things?$top=1000", headers = headers)
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

    """get all data from API"""
    #print("getting all data")
    getAllData()
    """grab current robot status from API"""
    #print("grabbing all robot status")
    grabAllRobotStatus()
    """run this to reset robot status to healthy"""
    #resetRobotStatus()
    """caclulate health of robots as observation"""
    """(this is done before updateRobotStatus, as it should correlate to prior robot sim data)"""
    #print("calculating Robot HP")
    calcRobotHP()
    """make some robots sick"""
    #print("updating robot status")
    updateRobotStatus()

    """get ids of broken bots (aka bots with warning and urgent status)"""
    #print("getting broken & warning bots")
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
