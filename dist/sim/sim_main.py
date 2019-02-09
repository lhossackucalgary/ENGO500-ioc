import logging
import os
import requests
import pickle


headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def load_data(fin_name):
    with open(fin_name, 'rb') as fin:
        data = pickle.load(fin)
    return data

def update_crews():
    crews = load_data(r'./data/crew.data')


def update_robots():
    robots = load_data(r'./data/robot.data')


def main():
    """
    Update crew and robot simulated information
    """
    update_crews()
    logging.info("Crews update complete")

    update_robots()
    logging.info("Robots updated complete")

    # Create location (Change iot user's location to new location..)
    # data = {"name": "", "description": "crew 1 location", "encodingType": "application/vnd.geo+json","location": {"type": "Point","coordinates": [18, -10]}}
    # try:
    #     r = requests.post(url = "http://routescout.sensorup.com/v1.0/Things(2)/Locations", json = data, headers = headers)
    #     print(r.text)
    # except:
    #     print("rip")
    #     exit()


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
