"""
Utilities for simulator
"""
import pickle
import math
import logging
import requests

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def load_data(fin_name):
    with open(fin_name, 'rb') as fin:
        data = pickle.load(fin)
    return data

def store_data(obj, fout_name):
    with open(fout_name, 'wb') as fout:
        pickle.dump(obj, fout)
    return True

def unit_vector(start, end):
    """
    @param[in]  2d coordinate tuple or list (origin)
    @param[in]  2d coordinate tuple or list (destination)
    @return     unit vector tuple (lon, lat, distance)
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = math.sqrt((dx * dx) + (dy * dy))
    return (dx/dist, dy/dist, dist)


def set_location(id, coords):
    """
    set the location for a Thing
    @param id   Thing id in SensorThings database
    @param coords   2-tuple or list (lon, lat) of coordinates to set loc
    """
    data = {"name": "Thing " + str(id) + " location",
              "description": "Thing " + str(id) + " location",
              "encodingType": "application/vnd.geo+json",
              "location": {
                "type": "Point",
                "coordinates": [coords[0], coords[1]]
              }
             }
    try:
        r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things(%d)/Locations"
                           % id, json = data, headers = headers)
        logging.debug(r.json())
        if (r.status_code >= 200) and (r.status_code < 300):
            coords = r.json()["location"]["coordinates"]
            logging.debug("Thing %d location updated: (%f, %f)"
                         % (id, coords[0], coords[1]))
            return (coords[0], coords[1])
        return (0.0,0.0)
    except:
        logging.exception("Request to give Thing %d a location failed." % id)
        return (0.0,0.0)
