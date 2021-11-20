import os.path as path
from flask import send_file
from flask_restful import Resource


class ProductToImage(Resource):

    def get(self, product_id):
        image_path = 'data/images/products/{}.png'.format(product_id)
        if path.exists(image_path):
            return send_file('data/images/products/{}.png'.format(product_id), mimetype='image/gif')
        return send_file('data/images/products/{}.png'.format("placeholder"), mimetype='image/gif')