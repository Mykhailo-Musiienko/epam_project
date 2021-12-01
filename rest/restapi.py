from flask import Blueprint, request
from service import teachers_crud
from models.teacher import TeacherSchema
from models.university import University
from models.teacher import Teacher

api = Blueprint('api', __name__)

teacher_schema = TeacherSchema()


@api.route('/', methods=['GET'])
def index() -> dict:
    """
    Show all teachers in json response.
    :return: dict
    """
    teacher_schema = TeacherSchema(many=True)
    teachers = teachers_crud.get_all_teachers()
    return teacher_schema.jsonify(teachers).data


@api.route('/<int:teacher_id>', methods=['GET'])
def read_teacher(teacher_id: int) -> dict:
    """
    Show teacher with given id in json response.
    :param teacher_id: Id of teacher
    :return: dict
    """
    teacher = teachers_crud.get_teacher(teacher_id)
    return teacher_schema.jsonify(teacher).data


# @api.route('/add_teacher', methods=['POST'])
# def add_teacher() -> dict:
#     """
#     Add new teacher to database. Return new teacher in json format.
#     :return: dict
#     """
#     name = request.json['name']
#     last_name = request.json['last_name']
#     birth_date = request.json['birth_date']
#     salary = request.json['salary']
#     university = request.json['university']
#     university_db = University.query.filter_by(name=university).first()
#     new_teacher = Teacher(name, last_name, birth_date, salary, university_db)
#     # teacher = teachers_crud.create_teacher(new_teacher)
#     return teacher_schema.jsonify(new_teacher).data
