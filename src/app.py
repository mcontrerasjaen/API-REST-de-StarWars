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
from models import db, User, Personajes, Planetas, Favoritos
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Personajes.query.all()
    return jsonify([p.serialize() for p in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Personajes.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200

@app.route('/people', methods=['POST'])
def create_person():
    body = request.get_json() # Captura el JSON que envíes desde Insomnia
    new_person = Personajes(
        name=body['name'],
        height=body.get('height', "unknown"), # .get() evita errores si falta el campo
        hair_color=body.get('hair_color', "unknown"),
        description=body.get('description', "")
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"msg": "Personaje creado", "id": new_person.id}), 201

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    body = request.get_json()
    person = Personajes.query.get(people_id)
    if not person:
        return jsonify({"msg": "No existe"}), 404
    
    person.name = body.get('name', person.name)
    person.height = body.get('height', person.height)
    db.session.commit()
    return jsonify({"msg": "Personaje actualizado"}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = Personajes.query.get(people_id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"msg": "Personaje borrado"}), 200
    return jsonify({"msg": "No encontrado"}), 404

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planetas.query.all()
    return jsonify([p.serialize() for p in planets]), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planetas(
        name=body['name'],
        climate=body.get('climate', "temperate"),
        population=body.get('population', "0"),
        diameter=body.get('diameter', "0")
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg": "Planeta creado", "id": new_planet.id}), 201

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planetas.query.get(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"msg": "Planeta borrado"}), 200
    return jsonify({"msg": "No encontrado"}), 404


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1
    favorites = Favoritos.query.filter_by(user_id=user_id).all()
    return jsonify([f.serialize() for f in favorites]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1     
    exists = Favoritos.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if exists:
        return jsonify({"msg": "Ya está en favoritos"}), 400
        
    new_fav = Favoritos(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planeta guardado"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = 1
    exists = Favoritos.query.filter_by(user_id=user_id, people_id=people_id).first()
    if exists:
        return jsonify({"msg": "Ya está en favoritos"}), 400

    new_fav = Favoritos(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Personaje guardado"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    fav = Favoritos.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"msg": "Planeta eliminado de favoritos"}), 200
    return jsonify({"msg": "No encontrado"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user_id = 1
    fav = Favoritos.query.filter_by(user_id=user_id, people_id=people_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"msg": "Personaje eliminado de favoritos"}), 200
    return jsonify({"msg": "No encontrado"}), 404

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planetas.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

