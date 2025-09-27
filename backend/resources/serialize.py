from flask_restful import fields

marshall_role = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
}

marshall_product = {
    "id": fields.Integer,
    "price": fields.Float,
    "name": fields.String,
    "in_stock": fields.Boolean,
    "price_type": fields.String,
    "mfd": fields.DateTime(dt_format='iso8601'),
    "expiry": fields.DateTime(dt_format='iso8601'),
}