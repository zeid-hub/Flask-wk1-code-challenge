from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    hero_powers = db.relationship('HeroPower', back_populates="hero")

    # add serialization rules
    serialize_rules = ('-hero_powers.hero',)


    def __repr__(self):
        return f'<Hero {self.id}, {self.name}, {self.super_name}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(), nullable=False)

    # add relationship
    # hero_powers = db.relationship('HeroPower', back_populates="power")
    
    # add serialization rules
    serialize_rules = ('-hero_powers.power',)

    # add validation
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description
    
    def __repr__(self):
        return f'<Power {self.id}, {self.name}, {self.description}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10), nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # add relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    # power = db.relationship('Power', back_populates="hero_powers")

    # add serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)

    # add validation
    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        if value not in ["Strong", "Weak", "Average"]:
            raise ValueError("Strength must be one of 'Strong', 'Weak', or 'Average'.")
        self._strength = value

    def __repr__(self):
        return f'<HeroPower {self.id}, {self.strength}, {self.hero_id}, {self.power_id}>'
