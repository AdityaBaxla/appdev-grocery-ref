from ._base_resource import BaseModelResource, BaseModelListResource
from flask_restful import reqparse, fields
from .serialize import marshall_role

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)
parser.add_argument("email", required=True)
parser.add_argument("password", required=True)



marshall_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "roles": fields.Nested(marshall_role)
}

class UserResource(BaseModelResource):
    parser = parser
    marshal = marshall_fields
