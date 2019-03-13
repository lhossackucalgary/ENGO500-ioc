"""
Main update file for simulator
Just initialized logger, calls update_crews() and update_robots()
**Run init_sim.py before running this script!!
"""
import logging
import os
import requests
from update_crews import update_crews
from update_robots import getUrgentDatastreams
from update_robots import getWarningDatastreams
from update_robots import update_robots
import random
import csv
import pickle
import datetime
import re
from util import *

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}
    
def test():
    test = load_data(r'data/robot.data')
    print(test)

def main():
    """
    Update crew and robot simulated information
    """
    try:
        update_crews()
        logging.info("Crews update complete.")
    except:
        logging.exception("Crews update failed.")

    try:
        update_robots()
        logging.info("Robots updated complete.")
    except:
        logging.exception("Robots update failed.")


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
