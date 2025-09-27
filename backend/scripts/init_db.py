from app import app, db
from models import *
from flask_security.utils import hash_password

with app.app_context():
    db.drop_all()
    db.create_all()
    userdatastore = app.datastore

    admin_role = userdatastore.find_or_create_role('admin', description='superuser')
    customer_role = userdatastore.find_or_create_role('customer', description='general user')
    manager_role = userdatastore.find_or_create_role('manager', description='controller of store')

    if not userdatastore.find_user(email='admin@study.iitm.ac.in'):
        userdatastore.create_user(
            name="admin",
            email='admin@study.iitm.ac.in',
            password=hash_password('pass'),
            roles=[admin_role]
        )

    if not userdatastore.find_user(email='manager@study.in'):
        userdatastore.create_user(
            name="manager",
            email='manager@study.in',
            password=hash_password('pass'),
            roles=[manager_role]
        )
    if not userdatastore.find_user(email='customer@study.in'):
        userdatastore.create_user(
            name="customer1",
            email='customer1@study.in',
            password=hash_password("pass"),
            roles=[manager_role]
        )

    db.session.commit()
