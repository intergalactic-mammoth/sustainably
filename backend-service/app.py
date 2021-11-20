from apis.Product import Product
from apis.ProductToImage import ProductToImage

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(Product,
                 '/product',
                 '/product/<product_id>'
                 )

api.add_resource(ProductToImage,
                 '/image/product/<product_id>',
                 )


if __name__ == '__main__':
    app.run(debug=True)
