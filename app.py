from flask import Flask, abort, request
from flask_migrate import Migrate
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Account
from os import environ

# Make sure database URL is set
if not environ.get("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL not set")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
    "DATABASE_URL").replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/api/v1.0/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        if not request.json or not 'name' in request.json:
            abort(400)
        account = Account(name=request.json['name'])
        db.session.add(account)
        db.session.commit()
        return jsonify({'account': account.toJSON()}), 201
    elif request.method == 'GET':
        accounts = db.session.query(Account).all()
        return jsonify({'accounts': [account.toJSON() for account in accounts]})


@app.route('/api/v1.0/accounts/<account_id>', methods=['GET'])
def get_account(account_id):
    account = db.session.query(Account).get(account_id)
    return jsonify({'account': account.toJSON()})
