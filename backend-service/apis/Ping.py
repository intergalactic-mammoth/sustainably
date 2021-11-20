from apis.utils.ChartUtils import *
from flask_restful import Resource


class Ping(Resource):

    def get(self):
        product_sustainability_breakdown("001", 10)
