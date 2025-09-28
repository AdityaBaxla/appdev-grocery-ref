from .auth import auth_bp
from flask import Blueprint
from flask_restful import Api
from .section_resource import SectionResource, SectionListResource, get_unapproved_sections, approve_section
from .product_resource import ProductResource, ProductListResource


api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(SectionListResource, "/sections")
api.add_resource(SectionResource, "/sections/<int:item_id>")

api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:item_id>")

# get unapproved items
api_bp.add_url_rule("/sections/unapproved", view_func=get_unapproved_sections, methods=['GET'])
api_bp.add_url_rule("/sections/<int:section_id>/approve",view_func=approve_section,  methods=['PATCH'])