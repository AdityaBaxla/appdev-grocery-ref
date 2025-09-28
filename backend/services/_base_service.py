from .errors import ForeignKeyConstraintError

class BaseService:
    model = None  # Override in child class
    foreign_key_models = {} # Override in child {key: Model}
    @staticmethod
    def get_db():
        from app import db
        return db
    
    @classmethod
    def validate_foreign_keys(cls, **kwargs):
        if not cls.foreign_key_models:
            return
        for field_name, Model in cls.foreign_key_models.items():
            if field_name in kwargs:
                fk_value = kwargs[field_name]
                if not (Model.query.get(fk_value)):
                    raise ForeignKeyConstraintError()

    @classmethod
    def get_all(cls):
        return cls.model.query.order_by(cls.model.id.desc()).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.model.query.get_or_404(id)
    
    @classmethod
    def get_filtered(cls, filters: dict):
        query = cls.model.query

        for key, value in filters.items():
            # Only apply filter if column exists in model
            if hasattr(cls.model, key):
                query = query.filter(getattr(cls.model, key) == value)

        return query.all()


    @classmethod
    def create(cls, **kwargs):
        cls.validate_foreign_keys(**kwargs)
        obj = cls.model(**kwargs)
        db = cls.get_db()
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def update(cls, obj, **kwargs):
        cls.validate_foreign_keys(**kwargs)
        db = cls.get_db()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    @classmethod
    def delete(cls, obj):
        db = cls.get_db()
        db.session.delete(obj)
        db.session.commit()
