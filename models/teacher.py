"""
This module represents model Teacher and class TeacherSchema for serialization and deserialization.

This module has class Teacher and class TeacherSchema.
This model imports such libraries like: flask_marshmallow, app, models.teacher, models.university
"""
from app import db, ma
from flask_marshmallow.fields import fields
from models.university import UniversitySchema


class Teacher(db.Model):
    """
    The class represents the model teacher.
    Attributes :
    id: int - identification of teacher
    name: str - name of teacher
    last_name: str - last name of teacher
    birth_date: date - when teacher was born
    salary: int - how much teacher get in cash
    university_id: int - identification for university (made for ForeignKey relation)
    university: University - object of university where teacher works

    Function :
    _init__() : constructor of class
    __str__() : string representation of class
    """

    __tablename__ = 'teacher'
    id = db.Column('teacher_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    birth_date = db.Column('birth_date', db.Date, nullable=False)
    salary = db.Column('salary', db.Integer, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey("university.id", ondelete='CASCADE'))
    university = db.relationship('University', backref='teacher', lazy='subquery')

    def __init__(self, name, last_name, birth_date, salary, university) -> None:
        """
        Constructor for class Teacher
        :param name: name of teacher
        :param last_name: last name of teacher
        :param birth_date: date when teacher was born
        :param salary: teacher's salary
        :param university: university where teacher works
        """
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.salary = salary
        self.university = university

    def __str__(self) -> str:
        """
        String representation of class Teacher
        :return: str
        """
        return f"Name: {self.name}, Last Name: {self.last_name},birth_date: {self.birth_date},salary: {self.salary}," \
               f"university: {self.university}"


class TeacherSchema(ma.Schema):
    """
    TeacherSchema class was made for serializing and deserializing class Teacher
    Parameters :
    id: int - identification of teacher
    name: str - name of teacher
    last_name: str - last name of teacher
    birth_date: date - when teacher was born
    salary: int - how much teacher get in cash
    university: University - object of university where teacher works
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
    last_name = fields.Str()
    birth_date = fields.Date()
    salary = fields.Int()
    university = fields.Nested(UniversitySchema)
