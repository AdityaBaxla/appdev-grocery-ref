from ._base_service import BaseService
from models import Product, Section

class ProductService(BaseService):
    model = Product
    foreign_key_models = {"section_id": Section}