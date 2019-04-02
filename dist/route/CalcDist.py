import logging
import os
import pickle
import requests
import geopy.distance

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def main():

    """
    Obtain crew id
    """
    crew_list = []
    try:
        crew_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things?$top=5000", headers = headers)
        if (crew_loc.status_code >= 200) and (crew_loc.status_code < 300):
            responseJSON = crew_loc.json()
            for thing in responseJSON['value']:
                if 'route' in thing['properties']:
                    crew_list.append({'iotid': thing['@iot.id']})
    except:
        logging.exception("Failed getting list of crew id")


    """
    Obtain crew location from server
    """
    for crew in crew_list:
        try:
            crew_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(crew['iotid']) + ")/Locations", headers = headers)
            if (crew_loc.status_code >= 200) and (crew_loc.status_code < 300):
                responseJSON = crew_loc.json()
                crew['coord'] = responseJSON['value'][0]['location']['coordinates']
            else:
                print("there was an error getting crew coordinate")
        except:
            logging.exception("Failed getting list of crew coordinates")

    """
    Obtain crew route from server
    """
    for crew in crew_list:
        try:
            crew_route = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(crew['iotid']) + ")", headers = headers)
            if (crew_route.status_code >= 200) and (crew_route.status_code < 300):
                responseJSON = crew_route.json()
                crew['route'] = responseJSON['properties']['route']
            else:
                print("there was an error getting crew routes")
        except:
            logging.exception("Failed getting list of crew routes")

    """
    Get list of broken bots
    """
    broken_bots = []
    for crew in crew_list:
        for bot in crew['route']:
            broken_bots.append({'iotid': bot})

    """
    Obtain coordinates of bots
    """
    for bot in broken_bots:
        try:
            broken_bot_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(bot['iotid']) + ")/Locations", headers = headers)
            if (broken_bot_loc.status_code >= 200) and (broken_bot_loc.status_code < 300):
                responseJSON = broken_bot_loc.json()
                bot['coord'] = responseJSON['value'][0]['location']['coordinates']
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
    Calculate Distance
    """
    total_dist = 0
    for crew in crew_list:
        crew_dist = 0
        for botid in crew['route']:
            for bot in broken_bots:
                if botid == bot['iotid']:
                    crew_dist = crew_dist + geopy.distance.distance(bot['coord'],crew['coord']).km
                    crew['coord'] = bot['coord']
                    break
        crew['dist'] = crew_dist
        total_dist = total_dist + crew_dist
        #print(crew)
    print('Total Dist: ' + str(total_dist))



if __name__ == "__main__":
    main()
