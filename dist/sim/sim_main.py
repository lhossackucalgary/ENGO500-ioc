import logging
import os
import requests

def load_sim_data():
    pass

def update_locations():
    pass

def update_status():
    pass

def store_sim_data():
    pass

def main():
    # load_sim_data()
    # update_locations()
    # update_things()
    # update_datastreams()
    # store_sim_data()


    headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

    # Create crew (only needs to be run once..)
    # data = {"name": "Crew 1", "description": "Crew 1..", "properties": {"route": [19123901, 712312, 31231, 41232]}}
    # try:
    #     r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things", json = data, headers = headers)
    #     print(r.text)
    # except:
    #     print("rip")
    #     exit()

    # Create


    # Create create location (Change iot user's location to new location..)
    data = {"name": "Crew 1 location 19:47", "description": "crew 1 location", "encodingType": "application/vnd.geo+json","location": {"type": "Point","coordinates": [18, -10]}}
    try:
        r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things(2)/Locations", json = data, headers = headers)
        print(r.text)
    except:
        print("rip")
        exit()

    # # Create
    # data = {"Locations": [{"@iot.id": 2662853}]}
    # try:
    #     r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Locations", json = data)
    #     print(r.text)
    # except:
    #     print("rip")
    #     exit()

    # data = {"Locations": [{"@iot.id":3}]}
    # try:
    #     r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(2)", json = data, headers = headers)
    #     print(r.text)
    # except:
    #     print("rip")
    #     exit()


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
