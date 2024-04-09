#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route("/heroes")
def list_heroes():
    my_heroes = Hero.query.all()
    heroes_list = [
        {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        for hero in my_heroes
    ]
    response = make_response(jsonify(heroes_list), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route("/heroes/<int:id>")
def get_heroe(id):
    hero = Hero.query.filter_by(id=id).first()
    
    if hero:
        response = make_response(
            hero.to_dict(),
            200
        )
        return response
    else:
        return make_response(
            {'error': 'Hero not found'},
             404
             )

@app.route("/powers")
def list_powers():
    my_powers = Power.query.all()

    my_power_list = []
    for power in my_powers:
        my_power_list.append(power.to_dict())

    response = make_response(
        my_power_list,
        200
    )
    return response

@app.route("/powers/<int:id>")
def get_power_by(id):
    power = Power.query.filter_by(id=id).first()

    if power:
        response = make_response(
            power.to_dict(),
            200
        )
        return response
    else:
        return make_response(
            {"error": "Power Not Found"},
             404
             )

@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.filter_by(id=id).first()
    data = request.get_json()
    
    if not power:
        return make_response({"error": "Power not found."}, 404)
    
    # Check if the description is provided and its length is at least 20 characters
    if "description" in data:
        if len(data["description"]) < 20:
            return make_response({"error": "Description must be at least 20 characters long."}, 404)
        else:
            power.description = data["description"]
    
    db.session.commit()
    
    return make_response(power.to_dict(), 200)
    

@app.route("/hero_powers", methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if "strength" not in data or data["strength"] not in ["Strong", "Weak", "Average"]:
        return make_response({"error": "Strength must be one of 'Strong', 'Weak', or 'Average'."}, 400)
    

    new_hero_power = HeroPower(strength=data["strength"], hero_id=data["hero_id"], power_id=data["power_id"])
    db.session.add(new_hero_power)
    db.session.commit()

    return make_response(
        new_hero_power.to_dict(),
        200
    )

if __name__ == '__main__':
    app.run(port=5555, debug=True)
