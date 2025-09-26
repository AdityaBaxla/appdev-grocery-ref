from app import app, db
from models import *

with app.app_context():

    db.create_all()

    if not User.query.filter_by(name = "admin").first():
        user = User(name = "admin", email = "admin@gmail.com", password = "how", fs_uniquifier="bla")
        db.session.add(user)
    db.session.commit()
