"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters , Planets, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():

    users_query = User.query.all()
    results_users = list(map(lambda item: item.serialize(), users_query))
    print(results_users)
   
    if results_users == []:
     return jsonify({"msg":"user not found"}),404
    else:
     return jsonify(results_users), 200
    
@app.route('/characters', methods=['GET'])
def get_characters():

    characters_query = Characters.query.all()
    results_characters = list(map(lambda item: item.serialize(), characters_query))
   
    if results_characters == []:
     return jsonify({"msg":"Characters not found"}),404
    else:
     return jsonify(results_characters), 200
    

@app.route('/planets', methods=['GET'])
def get_planets():

    planets_query = Planets.query.all()
    results_planets = list(map(lambda item: item.serialize(), planets_query))
    print(results_planets)
   
    if results_planets == []:
     return jsonify({"msg":"Planets not found"}),404
    else:
     return jsonify(results_planets), 200
    
@app.route('/vehicles', methods=['GET'])
def get_vehicles():

    vehicles_query = Vehicles.query.all()
    results_vehicles = list(map(lambda item: item.serialize(), vehicles_query))
    print(results_vehicles)
   
    if results_vehicles == []:
     return jsonify({"msg":"Vehicles not found"}),404
    else:
     return jsonify(results_vehicles), 200
    

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):

    user_query = User.query.filter_by(id=user_id).first()
    
   
    if user_query is None:
        return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify(user_query.serialize()), 200
    







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
