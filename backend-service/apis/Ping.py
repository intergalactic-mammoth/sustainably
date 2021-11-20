from apis.utils.ChartUtils import *
from flask_restful import Resource


class Ping(Resource):

    def get(self):
        co2_footprint("001", 3)
