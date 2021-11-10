from pathlib import Path
from typing import List
import json

from flask import Flask, abort, request
from flask_restful import Api, Resource
import pandas as pd

from src.data import Calculator


# configure flask app
app = Flask(__name__)
api = Api(app)


# download raw data
filepath = Path("/Users/claytonrossiter/Python/wainwright/wainwrights.csv")
df = pd.read_csv('wainwrights.csv', encoding='utf-8')


# Authentication Checks
def abort_if_fell_does_not_exist(id:int):
    """simple check to see if Fell id exists within dataframe index range"""
    if not id in df.index:
        abort(404, message="Fell ID is not valid")

def abort_if_not_a_number(text: List[str]):
    """check to see if the argument passed into text can be converted into a number"""
    if text is []:
        abort(404, message="Parameter is empty!")
    try:
        text = [float(t) for t in text]
    except:
        abort(404, message="Parameter is not a number")
        


# Resources
class Fell(Resource):
    """returns single instance of a fell"""
    def get(self, id:int):
        abort_if_fell_does_not_exist(id)
        return json.loads(df.iloc[id].to_json())


class Fells(Resource):
    """returns all instances that satisfy arguments provided"""
    def get(self):
        data=df
        # filter by name
        name = request.args.getlist('name')
        if name != []:
            data = data[data['Name'].str.contains('|'.join(name), case=False, regex=True)]
        
        # filter by above (in metres)
        # TODO: add metres/feet option
        above = request.args.get('above', None)
        if above is not None:
            abort_if_not_a_number([above])
            data = data[data['Height (m)'] > float(above)]
        
        # filter by below (in metres)
        # TODO: add metres/feet option
        below = request.args.get('below', None)
        if below is not None:
            abort_if_not_a_number([below])
            data = data[data['Height (m)'] < float(below)]

        # filter by nearest to this grid reference
        grid_reference = request.args.get('gridref', None)
        longitude = request.args.get('longitude', None)
        latitude = request.args.get('latitude', None)
        if grid_reference is not None:
            longitude, latitude = Calculator.get_longlat(grid_reference)
            data = Calculator.calculate_nearest_fells(data, longitude, latitude)

        # OR if grid reference is not provided, check if latitude/longitude is provided
        condition1 = grid_reference is None
        condition2 = latitude is not None
        condition3 = longitude is not None
        if all((condition1, condition2, condition3)):
            abort_if_not_a_number([longitude, latitude])
            data = Calculator.calculate_nearest_fells(data, float(longitude), float(latitude))

        return json.loads(data.to_json(orient="records"))


# configure api links
api.add_resource(Fell, "/fell/<int:id>")
api.add_resource(Fells, "/fells/")


if __name__ == '__main__':
    app.run(debug=True)