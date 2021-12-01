from models import db, ma
from flask_marshmallow.fields import fields
from models.university import UniversitySchema


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column('teacher_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    birth_date = db.Column('birth_date', db.Date, nullable=False)
    salary = db.Column('salary', db.Integer, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey("university.id", ondelete='CASCADE'))

    def __init__(self, name, last_name, birth_date, salary, university):
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.salary = salary
        self.university = university

    def __str__(self):
        return f"Name: {self.name}, Last Name: {self.last_name},birth_date: {self.birth_date},salary: {self.salary}," \
               f"university: {self.university}"


class TeacherSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    last_name = fields.Str()
    birth_date = fields.Date()
    salary = fields.Int()
    university_id = fields.Int()
