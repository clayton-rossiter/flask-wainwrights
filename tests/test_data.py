import pandas as pd
from OSGridConverter.base import OSGridError

from src.data import Calculator

from .framework import Framework


class TestCalculator(Framework):
    """"""

    def setUp(self):
        super().setUp()
        self.df = pd.read_csv('wainwrights.csv')
        self.lon2 = -3.1674900937       # bowfell
        self.lat2 = 54.4473534456       # bowfell

    def test_longlat_calculated_from_grid_reference(self):
        """test longitude and latitude are calculated from valid grid reference"""
        longitude, latitude = Calculator.get_longlat(self.grid_reference)
        self.assertIsNot(longitude, None)
        self.assertIsNot(latitude, None)

    def test_longlat_not_calculated_from_invalid_grid_reference(self):
        """test longitude and latitude are not calculated from invalid grid reference"""
        grid_references = [
            self.grid_reference[-1],    # string too short
            123,                        # numeric
        ]
        for grid_reference in grid_references:
            self.assertRaises(Exception, Calculator.get_longlat, grid_reference)

    def test_grid_reference_calculated_from_longlat(self):
        """tests grid reference is correctly calculated from longitude&latitude pair"""
        longitude = float(self.longitude)
        latitude = float(self.latitude)
        grid_reference = Calculator.convert_longlat_to_grid(longitude, latitude)
        self.assertTrue(grid_reference is not None)

    def test_grid_reference_not_calculated_if_not_float(self):
        """checks error is raised if longlat pair are strings"""
        self.assertRaises(OSGridError, Calculator.convert_longlat_to_grid, self.longitude, self.latitude)

    def test_calculate_distance_with_pairs_of_longlat(self):
        """checks distance is correctly calculated with genuine couple of longlat pairs"""
        lon1 = float(self.longitude)
        lat1 = float(self.latitude)
        distance = Calculator.calculate_distance(lon1, lat1, self.lon2, self.lat2)
        self.assertTrue(distance is not None)

    def test_distance_not_calculated_if_not_float(self):
        """checks exception is raised if longitude or latitude is not numeric"""
        lon1 = self.longitude
        lat1 = self.latitude
        self.assertRaises(Exception, Calculator.calculate_distance, lon1=lon1,lat1=lat1,lon2=self.lon2,lat2=self.lat2)
    
    def test_nearest_fells_calculated_with_longlat(self):
        """checks the longitude and latitude of a known fell returns that fell as the nearest"""
        df = Calculator.calculate_nearest_fells(self.df, float(self.longitude), float(self.latitude))
        nearest_fell = df.iloc[0]['Name']
        self.assertEqual(nearest_fell, 'Skiddaw')

        