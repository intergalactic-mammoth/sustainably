from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import csv

app = Flask(__name__)
api = Api(app)


class Product(Resource):
    def get(self, product_id=None):
        file_path = 'data/products.csv'

        if product_id is not None:
            with open(file_path, 'r') as file:
                # reader = csv.reader(file)
                reader = csv.DictReader(file)
                for record in reader:
                    if record['Id'] == product_id:
                        return record
        else:
            print("here")
            with open(file_path, 'r') as file:
                # reader = csv.reader(file)
                reader = csv.DictReader(file)
                return list(reader)


api.add_resource(Product,
                 '/product',
                 '/product/<product_id>')

if __name__ == '__main__':
    app.run(debug=True)
