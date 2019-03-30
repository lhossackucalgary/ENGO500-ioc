import logging
import os
import requests

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}


def cleanRoutesFromNondeletedCrews(id):
    data = {"properties": {"route": []}, "description": "[]"}
    try:
        r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%d)" % id, json = data, headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            print("cleaning route for crew %d" % id)
            return
        print("error: cleaning route")
    except:
        print("error: cleaning route")

def deleteAllThings():
    #id delete exceptions
    ex = [290, 293, 296, 299]

    #get all things from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Things?$top=10000", headers = headers)
        print("deleting things")
    except:
        print("error: delete things at 1")
        exit()

    #get all things in json form
    things = rd.json()["value"]

    for thing in things:
        #get id of thing
        id = thing["@iot.id"]
        #Delete current thing using id
        #print(id)
        if id not in ex:
            try:
                r = requests.delete(url = "http://routescout.sensorup.com/v1.0/Things(%d)" %id, headers = headers)
            except:
                print("error: delete things at 2")
                exit()
        else:
            cleanRoutesFromNondeletedCrews(id)


def deleteAllLocations():
    #thing id of delete exceptions
    ex = [290, 293, 296, 299]

    #get location of thing id exceptions
    ex_loc = []
    for id in ex:
        try:
            rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Thing(%d)/Locations?$top=50000" %id, headers = headers)
        except:
            print("error: getting location of thing id delete exceptions")
            exit()
        locations = rd.json()["value"]
        for location in locations:
            loc_id = location["@iot.id"]
        ex_loc.append(loc_id)

    #get all locations from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Locations?$top=50000", headers = headers)
        print("deleting locations")
    except:
        print("error: locations at 1")
        exit()

    #get all locations in json form
    locations = rd.json()["value"]

    for location in locations:
        #get id of location
        id = location["@iot.id"]
        #Delete current location using id
        #print(id)
        if id not in ex_loc:
            try:
                r = requests.delete(url = "http://routescout.sensorup.com/v1.0/Locations(%d)" %id, headers = headers)
            except:
                print("error: locations at 2")
                exit()

def deleteAllHistLocs():
    #get all locations from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/HistoricalLocations?$top=50000", headers = headers)
        print("deleting historical locations")
    except:
        print("error: hist loc at 1")
        exit()

    #get all historical locations in json form
    histlocs = rd.json()["value"]

    for histloc in histlocs:
        #get id of location
        id = histloc["@iot.id"]
        #Delete current historical location using id
        #print(id)
        try:
            r = requests.delete(url = "http://routescout.sensorup.com/v1.0/HistoricalLocations(%d)" %id, headers = headers)
        except:
            print("error: hist loc at 2")
            exit()

def deleteAllDatastreams():
    #get all datastreams from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Datastreams?$top=50000", headers = headers)
        print("deleting datastreams")
    except:
        print("error: datastreams at 1")
        exit()

    #get all datastreams in json form
    datastreams = rd.json()["value"]

    for datastream in datastreams:
        #get id of datastream
        id = datastream["@iot.id"]
        #Delete current datastream using id
        #print(id)
        try:
            r = requests.delete(url = "http://routescout.sensorup.com/v1.0/Datastreams(%d)" %id, headers = headers)
        except:
            print("error: datastreams at 2")
            exit()

def deleteAllSensors():
    """
    put iot.id of any sensors that should be kept in the following exceptions array named ex
    """
    ex = [846, 847, 9851]
    #get all sensors from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Sensors?$top=50000", headers = headers)
        print("deleting sensors")
    except:
        print("error: sensors at 1")
        exit()

    #get all sensors in json form
    sensors = rd.json()["value"]

    for sensor in sensors:
        #get id of sensor
        id = sensor["@iot.id"]
        #Delete current sensor using id
        #print(id)
        if id not in ex:
            try:
                r = requests.delete(url = "http://routescout.sensorup.com/v1.0/Sensors(%d)" %id, headers = headers)
            except:
                print("error: sensors at 2")
                exit()

def deleteAllObsProps():
    """
    put iot.id of any Observed Properties that should be kept in the following exceptions array named ex
    """
    ex = [848, 849, 9854]
    #get all observed properties from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/ObservedProperties?$top=500", headers = headers)
        print("deleting observed properties")
    except:
        print("error: obs props at 1")
        exit()

    #get all observed properties in json form
    obsprops = rd.json()["value"]

    for obsprop in obsprops:
        #get id of obsprop
        id = obsprop["@iot.id"]
        #Delete current obsprop using id
        #print(id)
        if id not in ex:
            try:
                r = requests.delete(url = "http://routescout.sensorup.com/v1.0/ObservedProperties(%d)" %id, headers = headers)
            except:
                print("error: obs props at 2")
                exit()

def deleteAllObservations():
    #get all observations from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Observations?$top=50000", headers = headers)
        print("deleting observations")
    except:
        print("error: observations at 1")
        exit()

    #get all observations in json form
    observations = rd.json()["value"]

    for observation in observations:
        #get id of observation
        id = observation["@iot.id"]
        #Delete current observation using id
        #print(id)
        try:
            r = requests.delete(url = "http://routescout.sensorup.com/v1.0/Observations(%d)" %id, headers = headers)
        except:
            print("error: observations at 2")
            exit()

def deleteAllFeatOfInt():
    #get all features of interest from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/FeaturesOfInterest?$top=500", headers = headers)
        print("deleting features of interest")
    except:
        print("error: feats at 1")
        exit()

    #get all feats in json form
    feats = rd.json()["value"]

    for feat in feats:
        #get id of feat
        id = feat["@iot.id"]
        #Delete current feat using id
        #print(id)
        try:
            r = requests.delete(url = "http://routescout.sensorup.com/v1.0/FeaturesOfInterest(%d)" %id, headers = headers)
        except:
            print("error: feats at 2")
            exit()

def main():

    deleteAllThings()
    deleteAllLocations()
    deleteAllHistLocs()
    deleteAllDatastreams()
    deleteAllObservations()
    deleteAllFeatOfInt()
    """
    REMEMBER: put all iot.id's of crews, sensors, and observable properties into 
    designmated exception arrays before deleting OR IOT.ID's WILL BE REASSIGNED!!!
    """
    deleteAllSensors()
    deleteAllObsProps()


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
