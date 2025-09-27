from ._base_resource import BaseModelResource, BaseModelListResource
from flask_restful import reqparse, fields
from .serialize import marshall_product
from services.section_service import SectionService

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)

marshall_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "products": fields.List(fields.Nested(marshall_product)),
}


class SectionResource(BaseModelResource):
    parser = parser
    marshal = marshall_fields
    service = SectionService

class SectionListResource(BaseModelListResource):
    parser = parser
    marshal = marshall_fields
    service = SectionService