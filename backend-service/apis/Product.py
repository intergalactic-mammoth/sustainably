from flask_restful import Resource
import csv


class Product(Resource):

    FILE_PATH = 'data/products.csv'

    def get(self, product_id=None):
        if product_id is not None:
            with open(Product.FILE_PATH, 'r') as file:
                # reader = csv.reader(file)
                reader = csv.DictReader(file)
                for record in reader:
                    if record['Id'] == product_id:
                        return record
        else:
            with open(Product.FILE_PATH, 'r') as file:
                # reader = csv.reader(file)
                reader = csv.DictReader(file)
                return list(reader)
