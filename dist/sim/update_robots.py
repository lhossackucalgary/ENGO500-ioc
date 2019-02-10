from util import *
import logging
import requests
import pickle


def update_robots():
    """
    Location is not updating, but sensor data & status will update
    """
    robots = load_data(r'./data/robot.data')
    # TODO: update robot data

    store_data(robots, r'data/robot.data')
