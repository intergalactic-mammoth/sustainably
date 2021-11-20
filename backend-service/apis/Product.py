from flask_restful import Resource
import csv


class Product(Resource):

    PRODUCT_SOURCE = 'data/products.csv'
    BRAND_SOURCE = 'data/brands.csv'

    def __init__(self):
        self.brands_cache = {}
        self.products_cache = {}

    def get_brand_data(self, brand_id):
        if brand_id in self.brands_cache.keys():
            return self.brands_cache[brand_id]

        brand_data = None
        with open(Product.BRAND_SOURCE, 'r') as file:
            reader = csv.DictReader(file)
            for record in reader:
                if record['Id'] == brand_id:
                    brand_data = record
                    break
        self.brands_cache[brand_id] = brand_data
        return brand_data

    def get(self, product_id=None):
        if product_id is not None:
            if product_id in self.products_cache.keys():
                return self.products_cache[product_id]

            with open(Product.PRODUCT_SOURCE, 'r') as p_file:
                reader = csv.DictReader(p_file)
                for record in reader:
                    if record['Id'] == product_id:
                        record['brand'] = self.get_brand_data(record['Brand_Id'])
                        self.products_cache[product_id] = record
                        return record
            return {}
        else:
            records = []
            with open(Product.PRODUCT_SOURCE, 'r') as file:
                reader = csv.DictReader(file)
                for record in reader:
                    record['brand'] = self.get_brand_data(record['Brand_Id'])
                    records.append(record)
            return records
