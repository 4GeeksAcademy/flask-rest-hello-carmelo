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
from models import db, User, Characters , Planets, Vehicles,FavoriteCharacter,FavoritePlanet,FavoriteVehicle
# from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager 

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


#Endopoints GET para obtener todos los resultados de las tablas
#Endopint GET ALL de user
@app.route('/user', methods=['GET'])
def get_users():

    users_query = User.query.all()
    results_users = list(map(lambda item: item.serialize(), users_query))
    # print(results_users)
   
    if results_users == []:
     return jsonify({"msg":"user not found"}),404
    else:
     return jsonify(results_users), 200


#Endpoint GET ALL de characters
@app.route('/characters', methods=['GET'])
def get_characters():

    characters_query = Characters.query.all()
    results_characters = list(map(lambda item: item.serialize(), characters_query))
   
    if results_characters == []:
     return jsonify({"msg":"Characters not found"}),404
    else:
     return jsonify(results_characters), 200
    
#Endopint GET ALL de planets
@app.route('/planets', methods=['GET'])
def get_planets():

    planets_query = Planets.query.all()
    results_planets = list(map(lambda item: item.serialize(), planets_query))
    print(results_planets)
   
    if results_planets == []:
     return jsonify({"msg":"Planets not found"}),404
    else:
     return jsonify(results_planets), 200


#Endopint GET ALL de vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():

    vehicles_query = Vehicles.query.all()
    results_vehicles = list(map(lambda item: item.serialize(), vehicles_query))
    print(results_vehicles)
   
    if results_vehicles == []:
     return jsonify({"msg":"Vehicles not found"}),404
    else:
     return jsonify(results_vehicles), 200
    
#Todos los endopints para obtener por id 
#Endopint GET by ID de user
@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):

    user_query = User.query.filter_by(id=user_id).first()
    
   
    if user_query is None:
        return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify(user_query.serialize()), 200
    

#Endpoint GET by ID de characters 
@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_character(characters_id):

    character_query = Characters.query.filter_by(id=characters_id).first()
    
   
    if character_query is None:
        return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify(character_query.serialize()), 200
    
#Endopint GET by ID de planets

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):

    planet_query = Planets.query.filter_by(id=planets_id).first()
    
   
    if planet_query is None:
        return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify(planet_query.serialize()), 200

#Endopint GET by ID de vehicles
@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_one_vehicle(vehicles_id):

    vehicle_query = Vehicles.query.filter_by(id=vehicles_id).first()
    
   
    if vehicle_query is None:
        return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify(vehicle_query.serialize()), 200   

#Todos los Endopoints POST
#Endopint POST de user
@app.route('/user/', methods=['POST'])
def create_user():
    body = request.json
    user_query = User.query.filter_by(name=body["name"]).first()
    
    if user_query is not None:
        return jsonify({"msg": "User already exists"}), 409
    
    new_user = User(name=body["name"], email=body["email"], password=body["password"],is_active=body["is_active"])
    db.session.add(new_user)
    db.session.commit()
    

    return jsonify({
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "password":new_user.password,
        "is_active":new_user.is_active
    }), 201

#Endpoint POST de characters
@app.route('/characters/', methods=['POST'])
def create_character():
    body = request.json
    character_query = Characters.query.filter_by(name=body["name"]).first()
    
    if character_query is not None:
        return jsonify({"msg": "Character already exists"}), 409
    
    new_character = Characters(name=body["name"], birth_year=body["birth_year"], eye_color=body["eye_color"],
                               gender=body["gender"], hair_color=body["hair_color"])
    db.session.add(new_character)
    db.session.commit()
    

    return jsonify({
        "id": new_character.id,
        "name": new_character.name,
        "birth_year": new_character.birth_year,
        "eye_color":new_character.eye_color,
        "gender":new_character.gender,
        "hair_color":new_character.hair_color,
    }), 201

#Endpoint POST de planets
@app.route('/planets/', methods=['POST'])
def create_planet():
    body = request.json
    planet_query = Planets.query.filter_by(name=body["name"]).first()
    
    if planet_query is not None:
        return jsonify({"msg": "Planets already exists"}), 409
    
    new_vehicle = Planets(name=body["name"], diameter=body["diameter"],
                          rotation_period=body["rotation_period"], orbital_period=body["orbital_period"])
    db.session.add(new_vehicle)
    db.session.commit()
    

    return jsonify({
        "id": new_vehicle.id,
        "name": new_vehicle.name,
        "diameter": new_vehicle.diameter,
        "orbital_period":new_vehicle.orbital_period,
        "rotation_period":new_vehicle.rotation_period
    }), 201

#Endpoint POST de vehicles
@app.route('/vehicles/', methods=['POST'])
def create_vehicle():
    body = request.json
    vehicle_query = Planets.query.filter_by(name=body["name"]).first()
    
    if vehicle_query is not None:
        return jsonify({"msg": "Vehicle already exists"}), 409
    
    new_vehicle = Vehicles(name=body["name"], model=body["model"],
                          vehicle_class=body["vehicle_class"], length=body["length"])
    db.session.add(new_vehicle)
    db.session.commit()
    

    return jsonify({
        "id": new_vehicle.id,
        "name": new_vehicle.name,
        "model": new_vehicle.model,
        "vehicle_class":new_vehicle.vehicle_class,
        "length":new_vehicle.length
    }), 201


#Todos los Endopoints DELETE
#Endopint DELETE de user 
@app.route('/user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):

    remove_user = User.query.get(user_id)
    
    if remove_user is None:
        return jsonify({"msg": "User not found"}), 404
    
    db.session.delete(remove_user)
    db.session.commit()
    
    return jsonify({"msg": "User deleted successfully"}), 200

#Endopint DELETE de characters
@app.route('/characters/<int:characters_id>/', methods=['DELETE'])
def delete_character(characters_id):

    remove_character = Characters.query.get(characters_id)
    
    if remove_character is None:
        return jsonify({"msg": "Character not found"}), 404
    
    db.session.delete(remove_character)
    db.session.commit()
    
    return jsonify({"msg": "Character deleted successfully"}), 200

#Endopint DELETE de planets
@app.route('/planets/<int:planets_id>/', methods=['DELETE'])
def delete_planet(planets_id):

    remove_planet = Planets.query.get(planets_id)
    
    if remove_planet is None:
        return jsonify({"msg": "Planets not found"}), 404
    
    db.session.delete(remove_planet)
    db.session.commit()
    
    return jsonify({"msg": "Planets deleted successfully"}), 200

#Enpoint DELETE de vehicles
@app.route('/vehicles/<int:vehicles_id>/', methods=['DELETE'])
def delete_vehicle(vehicles_id):

    remove_vehicle = Vehicles.query.get(vehicles_id)
    
    if remove_vehicle is None:
        return jsonify({"msg": "User not found"}), 404
    
    db.session.delete(remove_vehicle)
    db.session.commit()
    
    return jsonify({"msg": "User deleted successfully"}), 200


#Endpoint get favorites de User 



#Endopoints Post Favorite
#Endpoint post favorite Character
@app.route('/favoritecharacter/', methods=['POST'])
def create_favorite_character():
    body = request.json
    favorite_character_query = FavoriteCharacter.query.filter_by(character_id=body["character_id"]).first()

    if favorite_character_query is not None:
        return jsonify({"msg": "Favorite already exists"}), 409
    
    new_character_favorite = FavoriteCharacter(character_id=body["character_id"], user_id=body["user_id"])
    db.session.add(new_character_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite create"}), 200

#Endpoint Post favorite planet
@app.route('/favoriteplanet/', methods=['POST'])
def create_favorite_planet():
    body = request.json
    favorite_planet_query = FavoritePlanet.query.filter_by(planet_id=body["planet_id"]).first()

    if favorite_planet_query is not None:
        return jsonify({"msg": "Favorite already exists"}), 409
    
    new_planet_favorite = FavoritePlanet(planet_id=body["planet_id"], user_id=body["user_id"])
    db.session.add(new_planet_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite create"}), 200

#Endopoint Post favorite vehicle
@app.route('/favoritevehicle/', methods=['POST'])
def create_favorite_vehicle():
    body = request.json
    favorite_vehicle_query = FavoriteVehicle.query.filter_by(vehicle_id=body["vehicle_id"]).first()

    if favorite_vehicle_query is not None:
        return jsonify({"msg": "Favorite already exists"}), 409
    
    new_vehicle_favorite = FavoriteVehicle(vehicle_id=body["vehicle_id"], user_id=body["user_id"])
    db.session.add(new_vehicle_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite create"}), 200


#Endopoints DELETE Favorite
#Endpoint Delete favorite Character
@app.route('/favoritecharacter/<int:favoritecharacter_id>/', methods=['DELETE'])
def delete_favorite_character(favoritecharacter_id):

    remove_favorite_character = FavoriteCharacter.query.get(favoritecharacter_id)
    
    if remove_favorite_character is None:
        return jsonify({"msg": "Favorite not found"}), 404
    print(remove_favorite_character)
    
    db.session.delete(remove_favorite_character)
    db.session.commit()
    
    return jsonify({"msg": "Favorite deleted successfully"}), 200

#Endpoint Delete favorite Planet
@app.route('/favoriteplanet/<int:favoriteplanet_id>/', methods=['DELETE'])
def delete_favorite_planet(favoriteplanet_id):

    remove_favorite_planet = FavoritePlanet.query.get(favoriteplanet_id)
    
    if remove_favorite_planet is None:
        return jsonify({"msg": "Favorite not found"}), 404
    print(remove_favorite_planet)
    
    db.session.delete(remove_favorite_planet)
    db.session.commit()
    
    return jsonify({"msg": "Favorite deleted successfully"}), 200
#Endpoint Delete favorite vehicle
@app.route('/favoritevehicle/<int:favoritevehicle_id>/', methods=['DELETE'])
def delete_favorite_vehicle(favoritevehicle_id):

    remove_favorite_vehicle = FavoriteVehicle.query.get(favoritevehicle_id)
    
    if remove_favorite_vehicle is None:
        return jsonify({"msg": "Favorite not found"}), 404
    print(remove_favorite_vehicle)
    
    db.session.delete(remove_favorite_vehicle)
    db.session.commit()
    
    return jsonify({"msg": "Favorite deleted successfully"}), 200






 







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
