import logging
import os
import requests

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def deleteAllThings():
    #id delete exceptions
    ex = [290, 293, 296, 299]

    #get all things from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Things", headers = headers)
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
        
def deleteAllLocations():
    #get all locations from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Locations", headers = headers)
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
        try:
            r = requests.delete(url = "http://routescout.sensorup.com/v1.0/Locations(%d)" %id, headers = headers)
        except:
            print("error: locations at 2")
            exit()

def deleteAllHistLocs():
    #get all locations from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/HistoricalLocations", headers = headers)
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
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Datastreams", headers = headers)
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
    #get all sensors from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Sensors", headers = headers)
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
        try:
            r = requests.delete(url = "http://routescout.sensorup.com/v1.0/Sensors(%d)" %id, headers = headers)
        except:
            print("error: sensors at 2")
            exit()

def deleteAllObsProps():
    #get all observed properties from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/ObservedProperties", headers = headers)
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
        try:
            r = requests.delete(url = "http://routescout.sensorup.com/v1.0/ObservedProperties(%d)" %id, headers = headers)
        except:
            print("error: obs props at 2")
            exit()

def deleteAllObservations():
    #get all observations from api
    try:
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/Observations", headers = headers)
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
        rd = requests.get(url = "http://routescout.sensorup.com/v1.0/FeaturesOfInterest", headers = headers)
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
    deleteAllSensors()
    deleteAllObsProps()
    deleteAllObservations()
    deleteAllFeatOfInt()


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")