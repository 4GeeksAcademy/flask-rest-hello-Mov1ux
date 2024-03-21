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
from models import db, User, Person, Planet, Starships, Favorite_person, Favorite_planet
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

#----------------------------------------------------User-----------------------------------------------------------------------
@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    print(user)
    user_serialized=[]
    for x in user:
        user_serialized.append(x.serialize())
    return jsonify({"msg":"ok", "result": user_serialized}), 200

@app.route('/user/favorites', methods=['GET'])
def favorites_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if 'user_id' not in body:
        return jsonify({'msg': 'El campo user_id es obligatorio'}), 400
    user = User.query.get(body['user_id'])
    if user is None:
        return jsonify({'msg': "El usuario con el id: {} no existe".format(body['user_id'])}), 404
    favorite_planets = db.session.query(Favorite_planet, Planet).join(Planet).filter(Favorite_planet.user_id == body['user_id']).all()
    favorite_people = db.session.query(Favorite_person, Person).join(Person).filter(Favorite_person.user_id == body['user_id']).all()
    favorite_planets_serialized = []
    favorite_people_serialized = []
    print(favorite_planets)
    for favorite_item, planet_item in favorite_planets:
        favorite_planets_serialized.append({'favorite_planet_id': favorite_item.id, 'planet': planet_item.serialize()})
    for favorite_item, people_item in  favorite_people:
       favorite_people_serialized .append({'favorite_people_id': favorite_item.id, 'character': people_item.serialize()})
    return jsonify({'msg':'ok', 'results': {'favorite_planets': favorite_planets_serialized, 'favorite_people': favorite_people_serialized}})

#----------------------------------------------------Person-------------------------------------------------------------------------
@app.route('/person', methods= ['GET'])
def get_person():
    person = Person.query.all()
    print(person)
    person_serialized=[]
    for x in person:
        person_serialized.append(x.serialize())
    return jsonify({"msg": "ok", "results": person_serialized}), 200

@app.route('/person/<int:id>', methods= ['GET'])
def get_single_person(id):
    person = Person.query.get(id)
    if person is None:
        return jsonify({"Character dosen't exist"})
    print (person)
    return jsonify({"msg": "Name of the character is: ", "person": person.serialize()}), 200

@app.route("/favorite/person/<int:person_id>/<int:user_id>", methods=["POST"])
def add_favorite_people(user_id, person_id):
    body = request.get_json(silent=True)
    character = Person.query.get(person_id)
    user = User.query.get(user_id)
    if body is None:
        return jsonify("You must send information in the body."), 400
    if user is None:
        return jsonify("The user not found."), 404
    if character is None:
        return jsonify("The character not found."), 404

    favorite_person = Favorite_person(user_id=user_id, person_id=person_id)
    db.session.add(favorite_person)
    db.session.commit()
    return jsonify("Favorite character added successfully.")

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(person_id):
    favorite_people = Favorite_person.query.filter_by(person_id=person_id).first()
    if favorite_people:
        db.session.delete(favorite_people)
        db.session.commit()
        return jsonify("Favorite character removed successfully.")
    else:
        return jsonify("No favorite character was found for the specified ID."), 404

#----------------------------------------------------Planet------------------------------------------------------------------------------
@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    print(planets)
    planets_serialized=[]
    for x in planets:
        planets_serialized.append(x.serialize())
    return jsonify({"msg": "ok", "results": planets_serialized}), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({"Planet dosen't exist"})
    print(planet)
    return jsonify({"msg": "Name of your:", "results": planet.serialize()})

@app.route("/favorite/planet/<int:planet_id>/<int:user_id>", methods=["POST"])
def add_favorite_planet(user_id,planet_id):
    body = request.get_json(silent=True)
    planet = Planet.query.get(planet_id)
    user = User.query.get(user_id)
    if body is None:
        return jsonify("You must send information in the body."), 400
    if user is None:
        return jsonify("The user not found"), 404
    if planet is None:
        return jsonify("The planet not found."), 404

    new_favorite_planet = Favorite_planet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify("Favorite planet added successfully.")

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    favorite = Favorite_planet.query.filter_by(planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify("Favorite planet removed successfully.")
    else:
        return jsonify("No favorite planet was found for the specified ID."), 404
    
#-----------------------------------------------------Starship------------------------------------------------------------------------------
@app.route('/starship', methods= ['GET'])
def get_starship():
    starships = Starships.query.all()
    print(starships)
    starship_serialize=[]
    for x in starships:
        starship_serialize.append(x.serialize())
    return jsonify({"msg": "ok", "results": starship_serialize}), 200

@app.route('/starship/<int:id>', methods=['GET'])
def get_single_starship(id):
    starship = Starships.query.get(id)
    if starship is None:
        return jsonify({"Starship dosen't exist"})
    print(starship)
    return jsonify({"Name and id starship": starship.serialize()})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
