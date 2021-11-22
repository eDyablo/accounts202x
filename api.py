from flask import Blueprint, abort
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask.json import jsonify
from os import stat
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
            raise ValueError('Can contain only letters, numbers, hyphen or underscore')
        if value[0].isdigit():
            raise ValueError('Can not start with number')
        return value

    def get(self, account_id):
        account = models.db.session.query(models.Account).get(account_id)
        return jsonify({'account': publish_account(account)})


api.add_resource(Account, '/accounts/<string:account_id>')


class AccountList(Resource):
    def get(self):
        accounts = models.db.session.query(models.Account).all()
        return jsonify({'accounts': [publish_account(account) for account in accounts]})

    def post(self):
        parser = Account.args_parser()
        args = parser.parse_args(strict=True)
        account = models.db.session.query(models.Account).filter(
            models.Account.name == args['name']).first()
        if account:
            abort(400)
        account = models.Account(name=args['name'])
        models.db.session.add(account)
        models.db.session.commit()
        return jsonify({'account': publish_account(account)})


api.add_resource(AccountList, '/accounts')
