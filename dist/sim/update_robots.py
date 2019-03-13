import logging
import os
import requests
import random
import csv
import pickle
import datetime
import re
from util import *

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def update_robots():
    """
    Location is not updating, but sensor data & status will update
    """
    robots = load_data(r'./data/robot.data')
    
    """
    import simulator input data in csv
    """
    sid = []
    with open('data/simInputData.csv', newline='') as csvfile:
        sid = list(csv.reader(csvfile))
    #print(sid)

    """
    import current datastream positions in .data file
    """
    ds_list = load_data(r'data/dataSim.data')

    """
    get all datastreams from api
    """
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Datastreams", headers = headers)      
        print("getting datastreams")
    except:
        print("error: datastreams at 1")
        exit()

    #get all datastreams in json form
    datastreams = rd.json()["value"]
    

    for datastream in datastreams:
        """
        get id of datastream
        """
        id = datastream["@iot.id"]
        desc = datastream["description"]
        
        """
        get current time
        for utc: datetime.datetime.utcnow().isoformat()
        """
        time = datetime.datetime.now().replace(microsecond=0).isoformat()

        """
        use description to determine data type and which col it should be grabbing dataset from
        can use this section to assign bad data as well...
        col => column correlating to dataset
        rmax => max range (row) of dataset
        """
        col = None 
        rmax = None 
        if (desc == "Datastream for recording pressure"):
            col = 0
            rmax = 17
        if (desc == "Datastream for recording temperature"):
            col = 1
            rmax = 24

        psn = None
        i = 0
        for ds in ds_list:
            #get current position of datastream
            if (ds["iotid"] == id):
                psn = ds["psn"]

                #update datastream index position
                if (psn == rmax):
                    ds["psn"] = 0
                else:
                    ds["psn"] = psn + 1
                ds_list[i] = ds

            i = i + 1
        if (psn == None):
            print("could not find ds:%d" %id)
            exit()

        val = re.findall("-?\d+\.\d+", sid[psn][col])
        if val:
            val = list(map(float, val))
            #print(val[0])
        else:
            print("error: val not decimal at [%d][%d]" %psn %col)
            exit()

        data = {
            "phenomenonTime": "%s.000Z" %time,
            "resultTime" : "%s.000Z" %time,
            "result" : val[0],
            "Datastream":{"@iot.id":id}
        }
        #print("time(%s) id(%d) result(%d)" %(time, id, sid[rand]))

        """
        post datastream observation
        """
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

    print(ds_list)
    with open(r'data/dataSim.data', 'wb') as f:
        pickle.dump(ds_list, f)

    store_data(robots, r'data/robot.data')
