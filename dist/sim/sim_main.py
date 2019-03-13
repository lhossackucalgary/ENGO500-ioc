"""
Main update file for simulator
Just initialized logger, calls update_crews() and update_robots()
**Run init_sim.py before running this script!!
"""
import logging
import os
import requests
from update_crews import update_crews
from update_robots import update_robots
import random
import csv
import pickle
import datetime
from util import *

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def updateDatastream():

    #import simulator input data in csv
    with open('data/simInputData.csv', newline='') as csvfile:
        sid = list(csv.reader(csvfile))
    sid = list(map(int, sid[0]))
    #print(sid)

    #import current datastream positions in .data file
    ds_list = load_data(r'data/dataSim.data')

    #get all datastreams from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Datastreams", headers = headers)      
        print("getting datastreams")
    except:
        print("error: datastreams at 1")
        exit()

    #get all datastreams in json form
    datastreams = rd.json()["value"]
    

    for datastream in datastreams:
        #get id of datastream
        id = datastream["@iot.id"]
        
        #get current time
        #for utc: datetime.datetime.utcnow().isoformat()
        time = datetime.datetime.now().replace(microsecond=0).isoformat()

        #get random row number (change later to include pickle) "%s" % "%d" % sid[rand]
        #rand = random.randint(0,17)
        psn = None
        i = 0
        for ds in ds_list:
            #get current position of datastream
            if (ds["iotid"] == id):
                psn = ds["psn"]

                #update datastream index position
                if (psn == 17):
                    ds["psn"] = 0
                else:
                    ds["psn"] = psn + 1
                ds_list[i] = ds

            i = i + 1
        if (psn == None):
            print("could not find ds:%d" %id)
            exit()

        data = {
            "phenomenonTime": "%s.000Z" %time,
            "resultTime" : "%s.000Z" %time,
            "result" : sid[psn],
            "Datastream":{"@iot.id":id}
        }
        #print("time(%s) id(%d) result(%d)" %(time, id, sid[rand]))

        #post datastream observation
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


def temp():
    """
    Update crew and robot simulated information
    """
    try:
        update_crews()
        logging.info("Crews update complete.")
    except:
        logging.exception("Crews update failed.")

    try:
        update_robots()
        logging.info("Robots updated complete.")
    except:
        logging.exception("Robots update failed.")

def test():
    test = load_data(r'data/dataSim.data')
    print(test)

def main():
    #updateDatastream
    updateDatastream()
    #test()


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
