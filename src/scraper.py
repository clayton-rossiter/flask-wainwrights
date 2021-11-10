from enum import Enum

import pandas as pd

from src.data import Calculator


class WainwrightTables(Enum):
    """Enum class to cover the different table IDs from the URL in the Scraper class"""
    fells: int = 1
    outlying_fells: int = 2


class Scraper:
    """class to scrape the Wainwright fells information from a webpage using pandas"""
    url: str = r"https://en.wikipedia.org/wiki/List_of_Wainwrights"
    tables: WainwrightTables = WainwrightTables
    latitude: list=[]
    longitude: list=[]

    def scrape_wikipedia(self):
        """gets raw table data from wikipedia url"""
        df = pd.read_html(self.url)
        self.fells = df[self.tables.fells.value]
        self.outlying_fells = df[self.tables.outlying_fells.value]

    def convert_grid_references(self):
        """converts OS grid reference to longitude & latitude then appends to list"""
        for grid in self.fells['OS Grid Reference']:
            long,lat = Calculator.get_longlat(grid)
            self.latitude.append(long)
            self.longitude.append(lat)
    
    def append_df(self):
        """appends longitude and latitude to existing pandas dataframe of fells"""
        self.fells['Latitude'] = self.latitude
        self.fells['Longitude'] = self.longitude
        return self.fells
