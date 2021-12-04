"""
This module represents model University and class UniversitySchema for serialization and deserialization.

This module has class University and class UniversitySchema.
This model imports such libraries like: flask_marshmallow.fields, app, models.teacher, models.university
"""
from models import db, ma
from flask_marshmallow.fields import fields


class University(db.Model):
    """
    The class represents the model university.
    Attributes :
    id: int - identification of university
    name: str - name of university
    location: str - where university was built
    average_salary: int - average salary of university among all teachers

    Function :
    _init__() : constructor of class
    """
    __tablename__ = 'university'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    location = db.Column('location', db.String(50))
    average_salary = db.Column('average_salary', db.Integer, nullable=True, default=0)

    def __init__(self, name, location, average_salary=0) -> None:
        """
        Constructor of class
        :param name: name of university
        :param location: place where university is situated
        :param average_salary: average salary among all teachers in university
        """
        self.name = name
        self.location = location
        self.average_salary = average_salary


class UniversitySchema(ma.Schema):
    """
    UniversitySchema class was made for serializing and deserializing class University
    Parameters :
    id: int - identification of university
    name: str - name of university
    location: str - place where university is located
    average_salary: int - average salary among all teachers in university
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
    location=fields.Str()
    average_salary = fields.Int()
