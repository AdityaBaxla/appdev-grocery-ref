from flask import Flask
from config import LocalDevelopmentConfig
from models import db

app = Flask(__name__)

app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)

@app.route("/")
def test():
    return {"message" : "hello"}

if (__name__ == "__main__"):
    app.run(debug=True)