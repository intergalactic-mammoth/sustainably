"""
Create Statistics based on the user's database
"""

from flask_restful import Resource


class Statistic(Resource):
	def get(self, user_id):

		statistic_json = {
			"carbon_footprint": 8.0,
			"total_scanned_items": 12,
		}

		return statistic_json