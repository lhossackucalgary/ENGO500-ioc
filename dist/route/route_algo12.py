import logging
import os
import pickle
import requests
import geopy.distance
import math
import copy

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def CalcDist(bot_list, crew_list, routes):
    cb_dist = []
    for crew in crew_list:
        for bot in bot_list:
            dist = geopy.distance.distance(bot['coord'],crew['coord']).m
            cb_dist.append({'crewid': crew['iotid'], 'robotid': bot['iotid'], 'dist': dist, 'botcoord': bot['coord']})

    cb_dist = sorted(cb_dist, key=lambda k: k['dist'])
    min_len = math.inf
    for crew in crew_list:
        if len(crew['route']) < min_len:
            min_len = len(crew['route'])

    for route in cb_dist:
        for crew in crew_list:
            if (route['crewid'] == crew['iotid']) and (len(crew['route']) < (min_len*2+1)):
                crew['route'].append(route['robotid'])
                crew['coord'] = route['botcoord']
                bot_list = [bot for bot in bot_list if bot['iotid'] != route['robotid']]
                return bot_list
                break
        else:
            continue
        break

def euclidean_dist(a,b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)

def tot_dist(gene, bots):
    total_distance = 0
    for i in range(len(gene)-1):
        total_distance = total_distance + euclidean_dist(bots[gene[i]], bots[gene[i+1]])
    return total_distance

def twoOpt(gene, bots):
    for i in range(len(gene)-1):
        temp_gene = []
        for j in range(0, i):
            temp_gene.append(gene[j])
        temp_gene.append(gene[i+1])
        temp_gene.append(gene[i])
        for j in range(i+2, len(gene)):
            temp_gene.append(gene[j])
        if tot_dist(temp_gene, bots) < tot_dist(gene, bots):
            gene = copy.deepcopy(temp_gene)
    return gene

def threeOpt(gene, bots):
    for i in range(len(gene)-2):
        temp_gene = []
        for j in range(0, i):
            temp_gene.append(gene[j])
        temp_gene.append(gene[i+2])
        temp_gene.append(gene[i+1])
        temp_gene.append(gene[i])
        for j in range(i+3, len(gene)):
            temp_gene.append(gene[j])
        if tot_dist(temp_gene, bots) < tot_dist(gene, bots):
            gene = copy.deepcopy(temp_gene)
    return gene

def dualOpt(gene, bots):
    gene = copy.deepcopy(twoOpt(gene, bots))
    # gene = copy.deepcopy(threeOpt(gene, bots))
    return gene

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
    Obtain crew description
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
                    index['route'] = []
            else:
                print("there was an error getting crew coordinate")
        except:
            logging.exception("Failed getting list of crew coordinates")

    crew_list = [crew for crew in crew_list if crew['iotid'] not in crew_error]


    for index in crew_list:
        try:
            crew_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index['iotid']) + ")", headers = headers)
            if (crew_loc.status_code >= 200) and (crew_loc.status_code < 300):
                responseJSON = crew_loc.json()
                index['desc'] = responseJSON['description']
            else:
                print("there was an error getting crew description")
        except:
            logging.exception("Failed getting list of crew description")


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
    If crew description is valid and not empty, add to crew route
    """
    for crew in crew_list:
        if not crew['desc']:
            continue
        else:
            crew_desc = crew['desc'][1:-1]
            crew_desc = crew_desc.split(',')
            try:
                crew_desc = list(map(int, crew_desc))
                crew['route'] = crew_desc
                for bot in broken_bots:
                    if crew_desc[-1] == bot['iotid']:
                        crew['coord'] = bot['coord']
                broken_bots = [bot for bot in broken_bots if bot['iotid'] not in crew_desc]
            except:
                crew['desc'] = [];


    """
    Calculate distance between crew and robot
    """
    bot_copy = copy.deepcopy(broken_bots)

    routes = []
    while broken_bots != []:
        broken_bots = CalcDist(broken_bots, crew_list, routes)


    """
    Route Optimization using 2 & 3-Opt
    """
    # print(bot_copy)
    # print(crew_list)
    bot_coord_dict = {}
    for bot in bot_copy:
        bot_coord_dict.update({bot['iotid']: bot['coord']})

    for crew in crew_list:
        crew["route"] = dualOpt(crew["route"], bot_coord_dict)


    """
    Updating 'Thing' description
    """
    for crew in crew_list:
        if not crew['route']:
            continue
        if not crew['desc']:
            crew['desc'] = '[' + str(crew['route'][0]) + ']'
        crew['desc'] = '[]'


    """
    Uploading routes to server
    """
    for crew in crew_list:
        try:
            data = {"description": crew['desc'], "properties": {"route": crew['route']}}
            r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%d)" % crew['iotid'], json = data, headers = headers)
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
