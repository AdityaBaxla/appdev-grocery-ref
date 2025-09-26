from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Enum

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True # should not create database in itself
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(BaseModel):
    name = db.Column(db.String(200))
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    # flask-security specific
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True) # if Active = False, then the user will not be able to login
    roles = db.Relationship('Role', backref = 'bearers', secondary='user_roles')

    # relations
    sales = db.relationship("Sale", back_populates = "user")

class Role(BaseModel, RoleMixin):
    name = db.Column(db.String, unique = True, nullable  = False)
    description = db.Column(db.String, nullable = False)

class UserRoles(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Section(BaseModel):
    name = db.Column(db.String(80), nullable=False)

    # relations
    products = db.relationship('Product', back_populates="section")

class Product(BaseModel):
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    price_type = db.Column(db.Enum("kg", "litre"))
    mfd = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)

    # Foreign Keys
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    section = db.relationship('Section', back_populates="products", )

class SaleItem(BaseModel):
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Numeric(10, 2), default = 0)
    price_at_sale = db.Column(db.Numeric(10, 2))
    sale_id = db.Column(db.ForeignKey("sale.id"))

    # relations
    sale = db.relationship("Sale", back_populates="sale_items")

class Sale(BaseModel):
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime)

    # relations
    sale_items = db.relationship("SaleItem", back_populates = "sale")
    user = db.relationship("User", back_populates="sales")