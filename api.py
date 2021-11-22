from flask import Blueprint
from flask_restful import Api, Resource, abort
from flask_restful.reqparse import RequestParser
from flask.json import jsonify
import models
import re

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)


def non_empty_string(value):
    if not str or not isinstance(value, str) or not len(value) > 0:
        raise ValueError('Must be non empty string')
    return value


def publish_account(account: models.Account):
    return account.serialized() | {
        'uri': api.url_for(Account, account_id=account.id, _external=True),
    }


@api.resource('/accounts/<string:account_id>')
class Account(Resource):
    @staticmethod
    def args_parser() -> RequestParser:
        parser = RequestParser()
        parser.add_argument('name', type=Account.valid_name, required=True,
                            nullable=False, case_sensitive=False, trim=True)
        return parser

    @staticmethod
    def valid_name(value):
        if not str or not isinstance(value, str) or not len(value) > 0:
            raise ValueError('Must be non empty string')
        if len(value) < 6:
            raise ValueError('Must be at least 6 symbols long')
        if re.search(r"[^a-zA-Z0-9-_]", value):
            raise ValueError(
                'Can contain only letters, numbers, hyphen or underscore')
        if value[0].isdigit():
            raise ValueError('Can not start with number')
        return value

    @staticmethod
    def valid_id(value):
        if not str or not isinstance(value, str) or not len(value) > 0:
            abort(400, message={'id': 'Must be non empty string'})
        if not len(value) == 36 or re.search(r"[^a-fA-F0-9-]", value):
            abort(400, message={'id': 'Has invalid format'})
        return value

    def get(self, account_id):
        account = models.db.session.query(
            models.Account).get(Account.valid_id(account_id))
        if not account:
            abort(404, message=f'Account {account_id} does not exist')
        return jsonify({'account': publish_account(account)})


@api.resource('/accounts')
class AccountList(Resource):
    def get(self):
        accounts = models.db.session.query(models.Account).all()
        return jsonify({'accounts': [publish_account(account) for account in accounts]})

    def post(self):
        parser = Account.args_parser()
        args = parser.parse_args(strict=True)
        name = args['name']
        account = models.db.session.query(models.Account).filter(
            models.Account.name == name).first()
        if account:
            abort(400, message=f'Account {name} already exits')
        account = models.Account(name=name)
        models.db.session.add(account)
        models.db.session.commit()
        return jsonify({'account': publish_account(account)})
