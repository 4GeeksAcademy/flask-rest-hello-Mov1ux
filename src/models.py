from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__: 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return "Usuario con id: {} con email: {}".format (self.id, self.email)

    def serialize(self): 
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__: 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    
    def __repr__(self):
        return "Planeta con id : {} con nombre: {}".format (self.id, self.name)
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
        }

class Starships(db.Model):
    __tablename__: 'starships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    
    def __repr__(self):
        return "Asignacion de nave con nombre : {}, Id de flota: {}".format(self.name, self.id)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Person(db.Model):
    __tablename__: 'person'
    column_list = ('name','planet_relationshiop','starship_relationship')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    planet =db.Column(db.Integer,db.ForeignKey('planet.id'), nullable=False)
    planet_relationship = db.relationship(Planet)
    starship =db.Column(db.Integer,db.ForeignKey('starships.id'), nullable=True)
    starship_relationship = db.relationship(Starships)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return "Personaje de id: {} con nombre: {}".format(self.id, self.name)
    
    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Favorite_person(db.Model):
    __tablename__: 'favorite_person'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_relationship = db.relationship(User)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person_relationship = db.relationship(Person)

    def __repr__(self):
        return "Al usuario {} le gusta el personaje {}".format(self.user_id, self.person_id)
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id
        }

class Favorite_planet(db.Model):
    __tablename__: 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_relationship = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    planet_relationship = db.relationship(Planet)

    def __repr__(self):
        return "Al usuario {} le gusta el planeta {}".format(self.user_id, self.planet_id)
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.planet_id
        }
