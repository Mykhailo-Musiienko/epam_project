from models import db, ma
from flask_marshmallow.fields import fields


class University(db.Model):
    __tablename__ = 'university'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    location = db.Column('location', db.String(50))
    average_salary = db.Column('average_salary', db.Integer, nullable=True, default=0)
    teacher = db.relationship('Teacher', backref='university', passive_deletes=True)

    def __init__(self, name, location, average_salary=0):
        self.name = name
        self.location = location
        self.average_salary = average_salary


class UniversitySchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    average_salary = fields.Int()
