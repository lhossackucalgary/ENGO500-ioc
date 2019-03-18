import logging
import os
import pickle
import requests
import geopy.distance
import math

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def main():
    """
    Crew data from monitor_out.data
    """
    with open('./monitor_out.data', 'rb') as fin:
        data_in = pickle.load(fin)
    crew_list = data_in["crew_list"]


    """
    Broken Bots Status data from monitor_out2.data
    """
    with open('./monitor_out2.data', 'rb') as fin:
        bot_stat = pickle.load(fin)

    bot_urgent = []
    bot_warning = []

    for bot in bot_stat:
        if bot['status'] == 'Urgent':
            bot_urgent.append(bot['iotid'])
        elif bot['status'] == 'Warning':
            bot_warning.append(bot['iotid'])
        else:
            continue

    print(bot_urgent)
    print(bot_warning)
    """
    Obtain coordinates of crew and broken robots
    """
    crew_coord = []
    broken_bot_coord = []
    crew_error = []
    bot_error = []

    for index in crew_list:
        try:
            crew_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index) + ")/Locations", headers = headers)
            if (crew_loc.status_code >= 200) and (crew_loc.status_code < 300):
                responseJSON = crew_loc.json()
                if responseJSON['@iot.count'] == 0:
                    crew_error.append(index)
                else:
                    crew_coord.append(responseJSON['value'][0]['location']['coordinates'])
            else:
                print("there was an error")
        except:
            logging.exception("Failed getting list of crew coordinates")

    for item in crew_error:
        while item in crew_list:
            crew_list.remove(item)


    for index in broken_bots:
        try:
            broken_bot_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index) + ")/Locations", headers = headers)
            if (broken_bot_loc.status_code >= 200) and (broken_bot_loc.status_code < 300):
                responseJSON = broken_bot_loc.json()
                if responseJSON['@iot.count'] == 0:
                    bot_error.append(index)
                else:
                    broken_bot_coord.append(responseJSON['value'][0]['location']['coordinates'])
            else:
                print("there was an error")
        except:
            logging.exception("Failed getting list of broken bots coordinates")

    for item in bot_error:
        while item in broken_bots:
            broken_bots.remove(item)


    """
    Swap coordinate format to [lat,long]
    """
    for i in range(0,len(crew_list)):
        lon = crew_coord[i][0]
        lat = crew_coord[i][1]
        crew_coord[i][0] = lat
        crew_coord[i][1] = lon

    for i in range(0,len(broken_bots)):
        lon = broken_bot_coord[i][0]
        lat = broken_bot_coord[i][1]
        broken_bot_coord[i][0] = lat
        broken_bot_coord[i][1] = lon


    """
    Calculate distance between crew and robot
    """
    routes = []
    crew_routes = [[] for _ in range(0,len(crew_list))]

    while len(broken_bots)!=0:
        cb_dist = []
        for i in range(0,len(crew_list)):
            for j in range(0,len(broken_bots)):
                dist = geopy.distance.distance(broken_bot_coord[j],crew_coord[i]).km
                cb_dist.append({'crewid': crew_list[i],'robotid': broken_bots[j], 'dist': dist})

        min_dist = math.inf
        for route in cb_dist:
            if route['dist'] < min_dist:
                min_dist = route['dist']
                min_route = route

        crew_coord[crew_list.index(min_route['crewid'])] = broken_bot_coord[broken_bots.index(min_route['robotid'])]
        del broken_bot_coord[broken_bots.index(min_route['robotid'])]
        broken_bots.remove(min_route['robotid'])
        routes.append(min_route)


    """
    Append crew routes
    """
    for r in routes:
        crew_routes[crew_list.index(r['crewid'])].append(r['robotid'])


    """
    Uploading routes to server


    for index in range(0, len(crew_routes)):
        try:
            data = {"properties": {"route": crew_routes[index]}}
            r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%d)" % crew_list[index], json = data, headers = headers)
            if (r.status_code >= 200) and (r.status_code < 300):
                logging.debug("Adding route to crew %d" % crew_list[index])
            else:
                logging.warning("HTTP Error code while adding route for crew %d" % crew_list[index])
        except:
                logging.exception("Exception thrown generating route")
    """

"""
Logging data
"""
if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/route.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Router started")
    main()
    logging.info("Router ended")
