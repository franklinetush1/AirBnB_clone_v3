#!/usr/bin/python3
"""Flask App for AirBNB clone web static"""
from flask import Flask,make_response,jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)

# flask server environmental setup
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0",
            "title": "HBNB API",
            "endpoint": 'v1_views',
            "description": 'HBNB REST API',
            "route": '/v1/views',
        }
    ]
}
swagger = Swagger(app)

@app.teardown_appcontext
def tear(self):
    """this method calls .close()"""
    storage.close()

@app.errorhandler(404)
def err(error):
    """ Returns 404 status """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    """Flask app"""
    app.run(host=host, port=port, threaded=True)
