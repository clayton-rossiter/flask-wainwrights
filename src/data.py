from abc import ABC, abstractmethod
from math import sqrt, radians, cos, sin, asin
from pandas import DataFrame

from OSGridConverter import grid2latlong, latlong2grid




class Calculator(ABC):
    """envelope class to contain all dataframe-based calculations"""

    @abstractmethod
    def get_longlat(grid_reference:str):
        """takes the OS ordnance grid reference and converts to a longitude, latitude pair"""
        l = grid2latlong(grid_reference)
        return l.longitude, l.latitude

    @abstractmethod
    def convert_longlat_to_grid(longitude: float, latitude:float) -> str:
        """takes longtitude and latitude co-ordinates to return as OS grid reference"""
        return latlong2grid(latitude, longitude)

    @abstractmethod
    def calculate_distance(lon1:float, lat1:float, lon2:float, lat2:float) -> float:
        """calculate straight-line distance in km between two fells using Haversine formula"""
        # convert decimal degrees to radians 
        lon1,lat1,lon2,lat2 = map(radians, [lon1,lat1,lon2,lat2])
        delta_lon = lon2-lon1
        delta_lat = lat2-lat1
        # calculate distance taking curvature into account
        a = sin(delta_lat/2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # radius of the earth in km
        # return circular distance * angle in radians
        return c*r
    
    @abstractmethod
    def calculate_nearest_fells(df: DataFrame, longitude: float, latitude: float) -> DataFrame:
        """takes provided wainwrights dataframe and calculates nearest fells against provided longitude and latitude"""
        df['Nearest'] = df[['Longitude','Latitude']].apply(lambda x: Calculator.calculate_distance(*x, longitude, latitude), axis=1)
        return df.sort_values(by=['Nearest'])