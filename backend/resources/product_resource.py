from ._base_resource import BaseModelResource, BaseModelListResource
from flask_restful import reqparse, fields
from .serialize import marshall_product
from services.product_service import ProductService
from .utils import iso_datetime

parser = reqparse.RequestParser()
parser.add_argument("price", required=True)
parser.add_argument("name", type=str, required=True)
parser.add_argument("in_stock", type=bool)
parser.add_argument("price_type", type=str)
parser.add_argument("mfd", type=iso_datetime)
parser.add_argument("expiry", type=iso_datetime)
parser.add_argument("section_id", type=int)


class ProductResource(BaseModelResource):
    parser = parser
    marshal = marshall_product
    service = ProductService

class ProductListResource(BaseModelListResource):
    parser = parser
    marshal = marshall_product
    service = ProductService