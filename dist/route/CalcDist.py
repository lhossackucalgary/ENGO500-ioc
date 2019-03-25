import os
import pickle
import requests
import geopy.distance

def main():
    """
    Crew & Broken Bots data from monitor_out.data
    """
    with open('./monitor_out.data', 'rb') as fin:
        data_in = pickle.load(fin)
    crew_list = data_in["crew_list"]
    broken_bots = data_in["broken_bots"]
