from .auth import auth_bp
from flask import Blueprint
from flask_restful import Api
from .section_resource import SectionResource, SectionListResource
from .product_resource import ProductResource, ProductListResource

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(SectionListResource, "/sections")
api.add_resource(SectionResource, "/sections/<int:item_id>")

api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:item_id>")