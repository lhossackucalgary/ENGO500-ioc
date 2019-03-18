import logging
import os
import pickle
import requests
import geopy.distance

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}





def main():
    """
    Routing closest robot to each crew in chronological order
    """
    with open('./monitor_out.data', 'rb') as fin:
        data_in = pickle.load(fin)
    crew_list = data_in["crew_list"]
    broken_bots = data_in["broken_bots"]
    crew_coord = []
    broken_bot_coord = []
    crew_error = []
    bot_error = []


    """
    Obtain coordinates of crew and broken robots
    """
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

    print(crew_list)
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

    total_broken = len(broken_bots)
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
    Calculate distance of closest crew to robot
    """
    crew_routes = [[] for _ in range(0,len(crew_list))]
    crew_routes_dist = [[] for _ in range(0,len(crew_list))]
    route = []

    while len(broken_bots) != 0:
        for i in range(0,len(crew_list)):
            cb_dist = [[] for _ in range(0,len(broken_bots))]

            for j in range(0,len(broken_bots)):
                dist = geopy.distance.distance(broken_bot_coord[j],crew_coord[i]).km
                cb_dist[j] = [j,dist]

            cb_dist.sort(key=lambda x: x[1])

            if cb_dist[1][0] in crew_routes[:]:
                index = crew_routes.index(cb_dist[1][0])
                dist1 = geopy.distance.distance(broken_bot_coord[cb_dist[1][0]],crew_coord[index]).km
                dist2 = geopy.distance.distance(broken_bot_coord[cb_dist[1][0]],crew_coord[i]).km

                if dist1 <= dist2:
                    crew_routes[i].append(broken_bots[cb_dist[2][0]])
                    route.append(broken_bots[cb_dist[2][0]])
                else:
                    crew_routes[index].remove(broken_bots[cb_dist[1][0]])
                    crew_routes[i].append(broken_bots[cb_dist[1][0]])
                    for index2 in range(0,len(broken_bots)):
                        dist_new = geopy.distance.distance(broken_bot_coord[j],crew_coord[i]).km
                        cb_dist_new[index2] = [index2,dist_new]
                    cb_dist_new.remove(cb_dist_new[1][0])
                    cb_dist_new.sort(key=lambda x: x[1])
                    crew_routes[index].append(cb_dist_new[1][0])
                    route.append(cb_dist_new[1][0])


        for i in route:
            del broken_bots[cb_dist[i][0]]
            del broken_bot_coord[cb_dist[k][0]]













                if (len(crew_routes[i])) <= (total_broken/len(crew_list)):
                    crew_routes[i].append(broken_bots[cb_dist[k][0]])
                    crew_coord[i] = broken_bot_coord[cb_dist[k][0]]
                    break



        count = count + 1

        """
        for i in range(0,len(crew_routes_dist)):
            crew_routes_dist[i].sort(key=lambda x: x[1])
            for j in range(0,len(crew_routes_dist[i])):
                crew_routes[i].append(crew_routes_dist[i][j][0])
        """

        if len(broken_bots) == 0:
            break


    """
    Check if there are any crews with 0 robots, if so - assign closest robot to crew


    check_bot = []
    check_crew = []
    check_crew = [i for i,x in enumerate(crew_routes) if not x]
    for i in range(0,len(crew_routes)):
        if len(crew_routes[i]) > 1:
            check_bot = check_bot + crew_routes[i]
    check_dist = [[] for _ in range(0,len(check_bot))]


    if (len(broken_bots) > len(crew_list)):
        for i in range(0,len(check_crew)):

            check_bot = []
            for k in range(0,len(crew_routes)):
                if len(crew_routes[k]) > 1:
                    check_bot = check_bot + crew_routes[k]
                check_dist = [[] for _ in range(0,len(check_bot))]

            for j in range(0,len(check_bot)):
                check_dist[j] = [check_bot[j],geopy.distance.distance(broken_bot_coord[(broken_bots.index(check_bot[j]))],crew_coord[i]).km]
            min_check = min(check_dist, key=lambda x: x[1])

            for crew in crew_routes:
                try:
                    crew.remove(min_check[0])
                except ValueError:
                    pass

            crew_routes[check_crew[i]].append(min_check[0])
    """
    print(crew_routes)
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
