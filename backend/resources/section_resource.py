from ._base_resource import BaseModelResource, BaseModelListResource
from flask_restful import reqparse, fields, marshal
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

def get_unapproved_sections():
    sections = SectionService.get_filtered({"approved": False})
    return marshal(sections, marshall_fields)

def approve_section(section_id):
    section = SectionService.get_by_id(section_id)
    updated_section =  SectionService.update(section, approved=True)
    return marshal(updated_section, marshall_fields)