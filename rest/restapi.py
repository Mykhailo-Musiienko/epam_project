"""
This module works for RESTFULL-API in website.

This module includes functions: index(), read_teacher(), add_teacher(), update_teacher(), delete_teacher(),
get_university(), get_university_by_id(), post_university(), update_university(), delete_university()

This module imports: flask.Blueprint, flask.request, flask.jsonify, service, TeacherSchema, UniversitySchema,
University, Teacher
"""
from flask import Blueprint
from flask import request
from flask import jsonify
from service import teachers_crud
from service import universities_crud
from models.teacher import TeacherSchema
from models.university import UniversitySchema
from models.university import University
from models.teacher import Teacher

api = Blueprint('api', __name__)

teacher_schema = TeacherSchema()
university_schema = UniversitySchema()


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


@api.route('/', methods=['POST'])
def add_teacher() -> dict:
    """
    Add new teacher to database. Return new teacher in json format.
    :return: dict
    """
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    birth_date = request.json.get('birth_date')
    salary = request.json.get('salary')
    university = request.json.get('university')
    if not name or not last_name or not birth_date or not salary or not university:
        return {'error': {'message': 'Some data was not written', 'status': 400}}
    try:
        university_db = University.query.filter_by(name=university).first()
        if not university_db:
            return {'error': {'message': f'Wrong university name.', 'status': 400}}
    except Exception as ex:
        return {'error': {'message': f'Wrong university name. {str(ex)}', 'status': 400}}
    new_teacher = Teacher(name, last_name, birth_date, salary, university_db)
    res = teachers_crud.create_teacher(new_teacher)
    if not res:
        return {'error': {'message': 'Can\'t add teacher to database', 'status': 412}}
    return teacher_schema.jsonify(new_teacher).data


@api.route('/teacher_update/<int:teacher_id>', methods=['PATCH'])
def update_teacher(teacher_id) -> dict:
    """
    Update teacher with given id for REST-API.
    :param teacher_id:
    :return: dict
    """
    teacher = teachers_crud.get_teacher(teacher_id)
    if not teacher:
        return {'error': {'message': f'Wrong teacher id.', 'status': 400}}
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    birth_date = request.json.get('birth_date')
    salary = request.json.get('salary')
    university = request.json.get('university')
    res = teachers_crud.update_teacher_api(teacher_id, name, last_name, birth_date, salary, university)
    if isinstance(res, dict):
        return jsonify(res)
    else:
        return teacher_schema.jsonify(res).data


@api.route('/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id) -> dict:
    """
    Delete teacher with given id for REST-API.
    :param teacher_id: Id of teacher to delete
    :return: dict
    """
    res = teachers_crud.delete_teacher_api(teacher_id)
    print(res)
    if isinstance(res, dict):
        return jsonify(res)
    else:
        return teacher_schema.jsonify(res).data


@api.route('/university', methods=['GET'])
def get_university() -> dict:
    """
    Get all universities from database.
    :return: dict
    """
    university_schema = UniversitySchema(many=True)
    universities = universities_crud.get_all_universities()
    return university_schema.jsonify(universities).data


@api.route('/university/<int:university_id>', methods=["GET"])
def get_university_by_id(university_id) -> dict:
    """
    Get university with given id.
    :param university_id: Id of university to read from database
    :return: dict
    """
    res = universities_crud.get_university(university_id)
    if res:
        return university_schema.jsonify(res).data
    return jsonify({'error': {'message': 'No university was found with given id',
                              'status': 400}})


@api.route('/university', methods=['POST'])
def post_university() -> dict:
    """
    Create new university for REST-API.
    :return: dict
    """
    name = request.json.get('name')
    location = request.json.get('location')
    res = universities_crud.create_university_api(name, location)
    if isinstance(res, dict):
        return jsonify(res)
    return university_schema.jsonify(res).data


@api.route('/university/<int:university_id>', methods=['PATCH'])
def update_university(university_id) -> dict:
    """
    Update university with given id.
    :param university_id: Id of university to update
    :return: dict
    """
    name = request.json.get('name')
    location = request.json.get('location')
    res = universities_crud.update_university_api(university_id, name, location)
    if isinstance(res,dict):
        return jsonify(res)
    return university_schema.jsonify(res).data
    pass


@api.route('/university/<int:university_id>', methods=['DELETE'])
def delete_university(university_id) -> dict:
    """
    Delete university with given id from database.
    :param university_id: Id of university to delete
    :return: dict
    """
    res = universities_crud.delete_university_api(university_id)
    if isinstance(res, dict):
        return jsonify(res)
    return university_schema.jsonify(res).data
