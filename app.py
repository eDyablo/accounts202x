from flask import Flask
from flask.json import jsonify

app = Flask(__name__)


@app.route('/api/v1.0/accounts', methods=['GET'])
def accounts():
    return jsonify({})
