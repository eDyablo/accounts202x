from flask import Flask
from flask_migrate import Migrate
from flask.json import jsonify
from os import environ
from models import db

# Make sure database URL is set
if not environ.get("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL not set")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
    "DATABASE_URL").replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/api/v1.0/accounts', methods=['GET'])
def accounts():
    return jsonify({})
