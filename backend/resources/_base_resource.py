from flask_restful import Resource, marshal
from flask import request


class BaseModelListResource(Resource):
    service = None  # Override in child
    parser = None   # Override in child
    marshal = None # Override in child

    def get(self):
        items = self.service.get_all()
        filters = request.args.to_dict()
        if (filters and hasattr(self.service, "get_filtered")): # if has query params then send to get_filtered() service
            return self.service.get_filtered(filters), 200
        return marshal(items, self.marshal), 200

    def post(self):
        args = self.parser.parse_args()
        item = self.service.create(**args)
        return marshal(item, self.marshal), 201


class BaseModelResource(Resource):
    service = None
    parser = None
    marshal = None

    def get(self, item_id):
        item = self.service.get_by_id(item_id)
        return marshal(item, self.marshal), 200

    def put(self, item_id):
        item = self.service.get_by_id(item_id)
        args = self.parser.parse_args()
        item = self.service.update(item, **args)
        return marshal(item, self.marshal), 200

    def delete(self, item_id):
        item = self.service.get_by_id(item_id)
        self.service.delete(item)
        return '', 204
