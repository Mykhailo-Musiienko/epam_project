"""
This module works for RESTFULL-API in website.

This module includes functions: index(), read_teacher(), add_teacher(), update_teacher(),
delete_teacher(),
search_by_date(), get_university(), get_university_by_id(), post_university(),
update_university(), delete_university()

This module imports: flask.Blueprint, flask.request, flask.jsonify, service,
TeacherSchema, UniversitySchema,
University, Teacher
"""
import datetime
from flask import Blueprint, Response

api = Blueprint('api', __name__)
from flask import request
from flask import jsonify
from app import logger
from service import teachers_crud
from service import universities_crud
from models.teacher import TeacherSchema
from models.university import UniversitySchema
from models.university import University
from models.teacher import Teacher

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
    logger.debug("Api show all teachers in database.")
    return teacher_schema.jsonify(teachers).data


@api.route('/<int:teacher_id>', methods=['GET'])
def read_teacher(teacher_id: int) -> Response:
    """
    Show teacher with given id in json response
    :param teacher_id: Id of teacher
    :return: Response
    """
    teacher = teachers_crud.get_teacher(teacher_id)
    if not teacher:
        return jsonify({'error': {'message': 'No teacher was found with given id',
                                  'status': 400}})
    logger.debug("User get teacher with id {teacher_id} in REST-API")
    return teacher_schema.jsonify(teacher).data


@api.route('/', methods=['POST'])
def add_teacher() -> dict:
    """
    Add new teacher to database. Return new teacher in json format.
    :return: dict
    """
    logger.debug("User make post method  add_teacher in REST-API")
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    birth_date = request.json.get('birth_date')
    salary = request.json.get('salary')
    university = request.json.get('university')
    if not name or not last_name or not birth_date or not salary or not university:
        logger.debug("User did not entered some data")
        return {'error': {'message': 'Some data was not written', 'status': 400}}
    try:
        university_db = University.query.filter_by(name=university).first()
        if not university_db:
            return {'error': {'message': 'Wrong university name.', 'status': 400}}
    except Exception as ex:
        logger.error(str(ex))
        return {'error': {'message': 'Wrong university name.', 'status': 400}}

    try:
        birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
    except (TypeError, ValueError):
        logger.debug('User entered date in incorrect format.')
        return {'error': {'message': 'Incorrect date format.', 'status': 400}}
    if not isinstance(salary, int):
        logger.debug('User entered salary in incorrect format.')
        return {'error': {'message': 'Incorrect salary format.'
                                     ' Salary must be integer.', 'status': 400}}

    new_teacher = Teacher(name, last_name, birth_date, salary, university_db)
    res = teachers_crud.create_teacher(new_teacher)
    if not res:
        logger.error("Can\'t add teacher to database in REST-API")
        return {'error': {'message': 'Can\'t add teacher to database', 'status': 412}}
    logger.debug("User make new teacher in REST-API")
    return teacher_schema.jsonify(new_teacher).data


@api.route('/<int:teacher_id>', methods=['PATCH'])
def update_teacher(teacher_id) -> Response:
    """
    Update teacher with given id for REST-API
    :param teacher_id:
    :return: Response
    """
    logger.debug(f"User make patch method  update_teacher with id {teacher_id} in REST-API")
    teacher = teachers_crud.get_teacher(teacher_id)
    if not teacher:
        logger.debug("User entered wrong teacher id.")
        return {'error': {'message': f'Wrong teacher id.', 'status': 400}}
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    birth_date = request.json.get('birth_date')
    salary = request.json.get('salary')
    university = request.json.get('university')
    res = teachers_crud.update_teacher_api(teacher_id, name, last_name,
                                           birth_date, salary, university)
    if isinstance(res, dict):
        logger.debug("User entered incorrect data.")
        return jsonify(res)
    else:
        logger.debug("Teacher was updated.")
        return teacher_schema.jsonify(res).data


@api.route('/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id) -> Response:
    """
    Delete teacher with given id for REST-API
    :param teacher_id: Id of teacher to delete
    :return: Response
    """
    logger.debug("User make delete method  delete_teacher in REST-API")
    res = teachers_crud.delete_teacher_api(teacher_id)
    if isinstance(res, dict):
        logger.debug("User entered wrong teacher id")
        return jsonify(res)
    else:
        logger.debug("Teacher was deleted.")
        return teacher_schema.jsonify(res).data


@api.route('/search_by_date', methods=['POST'])
def search_by_date() -> dict:
    """
    Search teachers between given two dates
    :return: dict
    """
    logger.debug("User make post method  search_by_date in REST-API")
    teacher_schema = TeacherSchema(many=True)
    date_from = request.json.get('date_from')
    date_to = request.json.get('date_to')
    if not date_to or not date_from:
        logger.debug("User did not entered some date")
        return {'error': {'message': 'Some date was not given.', 'status': 400}}
    if not isinstance(date_from, str) or not isinstance(date_to, str):
        logger.debug("User entered date in incorrect form.")
        return {'error': {'message': 'Date must by given in string form.', 'status': 400}}
    try:
        date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
    except (TypeError, ValueError):
        logger.debug("User entered date in wrong format should be year-month-day")
        return {'error': {'message': 'Date is in wrong format should be year-month-day',
                          'status': 400}}
    teachers = Teacher.query.filter(Teacher.birth_date.between(date_from, date_to))
    logger.debug("Teachers between dates were shown")
    return teacher_schema.jsonify(teachers).data


@api.route('/university', methods=['GET'])
def get_university() -> dict:
    """
    Get all universities from database.
    :return: dict
    """
    university_schema = UniversitySchema(many=True)
    universities = universities_crud.get_all_universities()
    logger.debug(f"User get universities in REST-API")
    return university_schema.jsonify(universities).data


@api.route('/university/<int:university_id>', methods=["GET"])
def get_university_by_id(university_id) -> Response:
    """
    Get university with given id
    :param university_id: Id of university to read from database
    :return: dict
    """
    logger.debug(f"User get university with id {university_id} in REST-API")
    res = universities_crud.get_university(university_id)
    if res:
        logger.debug("User entered wrong id")
        return university_schema.jsonify(res).data
    logger.debug("Teacher with id {university_id} was shown.")
    return jsonify({'error': {'message': 'No university was found with given id',
                              'status': 400}})


@api.route('/university', methods=['POST'])
def post_university() -> Response:
    """
    Create new university for REST-API.
    :return: dict
    """
    logger.debug("User make post method to create new university in REST-API")
    name = request.json.get('name')
    location = request.json.get('location')
    res = universities_crud.create_university_api(name, location)
    if isinstance(res, dict):
        logger.debug("User entered wrong data")
        return jsonify(res)
    logger.debug("University was added")
    return university_schema.jsonify(res).data


@api.route('/university/<int:university_id>', methods=['PATCH'])
def update_university(university_id) -> Response:
    """
    Update university with given id
    :param university_id: Id of university to update
    :return: dict
    """
    logger.debug("User make method patch to update university in REST-API")
    name = request.json.get('name')
    location = request.json.get('location')
    res = universities_crud.update_university_api(university_id, name, location)
    if isinstance(res, dict):
        logger.debug("User entered wrong data.")
        return jsonify(res)
    logger.debug("University was updated.")
    return university_schema.jsonify(res).data


@api.route('/university/<int:university_id>', methods=['DELETE'])
def delete_university(university_id) -> Response:
    """
    Delete university with given id from database
    :param university_id: Id of university to delete
    :return: Response
    """
    logger.debug("User make delete method to delete university in REST-API")
    res = universities_crud.delete_university_api(university_id)
    if isinstance(res, dict):
        logger.debug("User entered wrong university id")
        return jsonify(res)
    logger.debug("University was deleted.")
    return university_schema.jsonify(res).data
