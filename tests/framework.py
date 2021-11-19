import json
from requests.models import Response
import unittest

from src.api import app

import pandas as pd
from pandas.core.frame import DataFrame


class Framework(unittest.TestCase):
    """Framework to base all other unit tests"""

    def setUp(self):
        """initialise shared resources"""
        self.base_url = r"http://127.0.0.1:5000/"
        self.id = '4'
        self.fell_name = 'scafell'
        self.grid_reference = 'NY369112'    # Hart Crag
        self.longitude = '-3.1485069114'    # Skiddaw
        self.latitude = '54.6506509377'     # Skiddaw

        app.config['TESTING'] = True
        self.app = app.test_client()
        

    def generate_query(self, **kwargs) -> str:
        """generates string of kwargs in form of GET request"""
        query='?'
        for kwarg in kwargs:
            query = query + f'{kwarg}={kwargs[kwarg]}&'
        return query[:-1]

    def check_lists_are_equal(self, list1: list, list2: list) -> bool:
        """returns true if two lists are the same, otherwise false"""
        return sorted(list1) == sorted(list2)

    def convert_request_to_df(self, r: Response) -> DataFrame:
        """takes response from requests and converts to dataframe"""
        raw_json = json.loads(r.get_data())
        dumps = json.dumps(raw_json)
        return pd.read_json(dumps)