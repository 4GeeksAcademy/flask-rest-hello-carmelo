from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites_characters = db.relationship('FavoriteCharacter', backref='users', lazy=True)
    favorites_planets = db.relationship('FavoritePlanet', backref='users', lazy=True)
    favorites_vehicles = db.relationship('FavoriteVehicle', backref='users', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=False, nullable=False)
    birth_year = db.Column(db.String(250),unique=False, nullable=False)
    eye_color = db.Column(db.String(250),unique=False, nullable=False)
    gender = db.Column(db.String(250),unique=False, nullable=False)
    hair_color = db.Column(db.String(250),unique=False, nullable=False)
    favorites_characters = db.relationship('FavoriteCharacter', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year":self.birth_year,
            "eye_color":self.eye_color,
            "gender":self.gender,
            "hair_color":self.hair_color
            
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=False, nullable=False)
    diameter = db.Column(db.String(250),unique=False,nullable=False)
    rotation_period = db.Column(db.String(250),unique=False, nullable=False)
    orbital_period = db.Column(db.String(250),unique=False, nullable=False)
    favorites_planets = db.relationship('FavoritePlanet', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period
            
        }
    

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=False, nullable=False)
    model = db.Column(db.String(250),unique=False,nullable=False)
    vehicle_class = db.Column(db.String(250),unique=False,nullable=False)
    length = db.Column(db.String(250),unique=False,nullable=False)
    favorites_vehicles = db.relationship('FavoriteVehicle', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model":self.model,
            "vehicle_class":self.vehicle_class,
            "length":self.length
        }
    
# class FavoriteUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<FavoriteUser %r>' % self.user_id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id":self.user_id
#         }
    
class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.character_id

    def serialize(self):
        return {
            "id": self.id,
            "character_id":self.character_id,
            "user_id":self.user_id
        }
    
class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.planet_id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id":self.planet_id,
            "user_id":self.user_id
        }
    
class FavoriteVehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<FavoriteVehicles %r>' % self.vehicle_id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id":self.vehicle_id,
            "user_id":self.user_id
        }




