"""
Utilities for simulator
"""
import pickle


headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

def load_data(fin_name):
    with open(fin_name, 'rb') as fin:
        data = pickle.load(fin)
    return data
