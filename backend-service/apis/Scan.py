"""
Upload Scan EAN numbers and attach them to the user database.
"""

from flask_restful import Resource
import csv
import pandas as pd

import datetime


class Scan(Resource):

	def get(self, user_id, product_id):
		time_stamp = str(datetime.datetime.now())

		user_data = pd.read_csv(f"data/user/{user_id:}.csv")
		user_data = user_data.append(
			{
				"datetime": time_stamp,
				"Id": product_id,
			},
			ignore_index=True,
		)
		user_data.to_csv(f"data/user/{user_id:}.csv", index=False)

		return time_stamp
