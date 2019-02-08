import logging
import os
import requests

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def store_crew_data():
    """
    iot_id  -> current location
            -> destination location
    """
    pass

def store_robot_data():
    """
    iot_id  -> array of sensor data (current)
            -> array of sensor data (target?) (reduce random noise..idk how we want to do this)
    """
    pass

def main():
    # store_crew_data()
    # store_robot_data()

    for i in range(0, 10):
        # Create crew (only needs to be run once per crew)
        data = {"name": "Crew" + str(i), "description": "Crew " + str(i), "properties": {"route": []}}
        try:
            r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things", json = data, headers = headers)
            print(data)
        except:
            print("rip")
            exit()



if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
