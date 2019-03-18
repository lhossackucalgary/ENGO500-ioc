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
    crew_data = data_in["crew_list"]

    crew_list = []
    for crew in crew_data:
        crew_list.append({'iotid': crew})


    """
    Broken bots status data from monitor_out2.data
    """
    with open('./monitor_out2.data', 'rb') as fin:
        broken_bots = pickle.load(fin)

    broken_bots = [bot for bot in broken_bots if bot['status'] != 'Healthy']


    """
    Obtain coordinates of crew and broken robots
    """
    crew_error = []

    for index in crew_list:
        try:
            crew_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index['iotid']) + ")/Locations", headers = headers)
            if (crew_loc.status_code >= 200) and (crew_loc.status_code < 300):
                responseJSON = crew_loc.json()
                if responseJSON['@iot.count'] == 0:
                    crew_error.append(index['iotid'])
                else:
                    index['coord'] = responseJSON['value'][0]['location']['coordinates']
            else:
                print("there was an error")
        except:
            logging.exception("Failed getting list of crew coordinates")

    crew_list = [crew for crew in crew_list if crew['iotid'] not in crew_error]


    for index in broken_bots:
        try:
            broken_bot_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index['iotid']) + ")/Locations", headers = headers)
            if (broken_bot_loc.status_code >= 200) and (broken_bot_loc.status_code < 300):
                responseJSON = broken_bot_loc.json()
                index['coord'] = responseJSON['value'][0]['location']['coordinates']
            else:
                print("there was an error")
        except:
            logging.exception("Failed getting list of broken bots coordinates")


    """
    Swap coordinate format to [lat,long]
    """
    for crew in crew_list:
        lon, lat = crew['coord'][0], crew['coord'][1]
        crew['coord'] = lat, lon

    for bot in broken_bots:
        lon, lat = bot['coord'][0], bot['coord'][1]
        bot['coord'] = lat, lon


    """
    Calculate distance between crew and robot
    """
    routes = []
    bot_urgent = []
    bot_warning = []

    for bot in broken_bots:
        if bot['status'] == 'Urgent':
            bot_urgent.append(bot)
        elif bot['status'] == 'Warning':
            bot_warning.append(bot)
        else:
            continue

    while bot_urgent != []:
        cb_dist = []
        for crew in crew_list:
            for bot in bot_urgent:
                dist = geopy.distance.distance(bot['coord'],crew['coord']).m
                cb_dist.append({'crewid': crew['iotid'], 'robotid': bot['iotid'], 'dist': dist, 'botcoord': bot['coord']})

        min_dist = math.inf
        for route in cb_dist:
            if route['dist'] < min_dist:
                min_dist = route['dist']
                min_route = route

        for crew in crew_list:
            if crew['iotid'] == min_route['crewid']:
                crew['coord'] = min_route['botcoord']

        bot_urgent = [bot for bot in bot_urgent if bot['iotid'] != min_route['robotid']]
        routes.append(min_route)


    while bot_warning != []:
        cb_dist = []
        for crew in crew_list:
            for bot in bot_warning:
                dist = geopy.distance.distance(bot['coord'],crew['coord']).m
                cb_dist.append({'crewid': crew['iotid'], 'robotid': bot['iotid'], 'dist': dist, 'botcoord': bot['coord']})

        min_dist = math.inf
        for route in cb_dist:
            if route['dist'] < min_dist:
                min_dist = route['dist']
                min_route = route

        for crew in crew_list:
            if crew['iotid'] == min_route['crewid']:
                crew['coord'] = min_route['botcoord']

        bot_warning = [bot for bot in bot_warning if bot['iotid'] != min_route['robotid']]
        routes.append(min_route)


    """
    Append crew routes
    """
    crew_id = []
    for crew in crew_list:
        crew_id.append(crew['iotid'])

    crew_routes = [[] for _ in range(0,len(crew_list))]
    for r in routes:
        crew_routes[crew_id.index(r['crewid'])].append(r['robotid'])


    """
    Uploading routes to server
    """

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
Logging data
"""
if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/route.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Router started")
    main()
    logging.info("Router ended")
