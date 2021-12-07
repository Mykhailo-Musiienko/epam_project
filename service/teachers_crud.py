"""
This module demonstrates CRUD operations for teacher model.

It has CRUD functions for website application and for REST-API.

This module includes functions: get_all_teachers(), get_teacher(), create_teacher(),
update_teacher(), delete_teacher(), update_teacher_api(), delete_teacher_api().

This module imports: typing.Any, sqlalchemy.func, app, University, Teacher.
"""
import datetime
from app import db
from app import logger
from models.teacher import Teacher
from models.university import University


def get_all_teachers() -> list:
    """
    Return all teachers from database.
    :return: list
    """
    return Teacher.query.all()


def get_teacher(teacher_id) -> Teacher:
    """
    Return teacher with given id from database
    :param teacher_id: Id of teacher.
    :return: Teacher
    """
    return Teacher.query.get(teacher_id)


def create_teacher(teacher) -> bool:
    """
    Add teacher to database. Return True if teacher was added and False if raised exception
    :param teacher: Teacher to add.
    :return: bool
    """
    try:
        db.session.add(teacher)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        logger.error(str(ex))
        return False
    return True


def update_teacher(teacher: Teacher, teacher_id: int) -> bool:
    """
    Update teacher from database to given teacher. Return true if teacher was successfully updated
    and False if it was raised an exception
    :param teacher: new teacher
    :param teacher_id: Id of teacher to update
    :return: bool
    """
    is_changed = False
    try:
        db_teacher = get_teacher(teacher_id)
        if teacher.name:
            if not teacher.name == db_teacher.name:
                db_teacher.name = teacher.name
                is_changed = True
        if teacher.last_name:
            if not teacher.last_name == db_teacher.last_name:
                db_teacher.last_name = teacher.last_name
                is_changed = True
        if teacher.birth_date:
            if not teacher.birth_date == db_teacher.birth_date:
                db_teacher.birth_date = teacher.birth_date
                is_changed = True
        if teacher.salary:
            if not int(teacher.salary) == db_teacher.salary:
                db_teacher.salary = teacher.salary
                is_changed = True
        if teacher.university:
            if not teacher.university == db_teacher.university:
                db_teacher.university = teacher.university
                is_changed = True
        if not is_changed:
            return False
        db.session.flush()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        logger.error(str(ex))
        return False
    return True


def delete_teacher(teacher_id) -> bool:
    """
    Delete teacher from database with given id
    :param teacher_id: Teacher's id to delete
    :return: bool
    """
    try:
        Teacher.query.filter(Teacher.id == teacher_id).delete()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        logger.error(str(ex))
        return False
    return True


def update_teacher_api(teacher_id, name, last_name, birth_date, salary, university) -> dict:
    """
    Method PATCH for teacher api. Update teacher with given id
    :param teacher_id: Id of teacher
    :param name: Teacher's name
    :param last_name: Teacher's last name
    :param birth_date: When teacher was born
    :param salary: How much teacher get in cash
    :param university: Name of university where teacher make lectures
    :return: Teacher
    """
    if not name and not last_name and not birth_date and not salary and not university:
        logger.debug('No data was given')
        return {'error': {'message': f'No data was given.', 'status': 400}}
    db_teacher = get_teacher(teacher_id)
    if university:
        university_db = University.query.filter_by(name=university).first()
        if not university_db:
            logger.debug('Wrong university name')
            return {'error': {'message': 'Wrong university name.', 'status': 400}}
        db_teacher.university = university_db
    if name:
        if name.isalnum():
            db_teacher.name = name
        else:
            logger.debug('User entered symbols in name that are not allowed')
            return {'error': {'message': 'Symbols in name are not allowed.', 'status': 400}}
    if last_name:
        if last_name.isalnum():
            db_teacher.last_name = last_name
        else:
            logger.debug('User entered symbols in last name that are not allowed')
            return {'error': {'message': 'Symbols in last name are not allowed.', 'status': 400}}

    if salary:
        if not isinstance(salary, int) and not isinstance(salary, bool):
            logger.debug('User entered salary with wrong type')
            return {'error': {'message': 'Salary is not integer', 'status': 400}}
        db_teacher.salary = salary
    if birth_date:
        try:
            datetime.datetime.strptime(birth_date, "%Y-%m-%d")
            db_teacher.birth_date = birth_date

        except (TypeError, ValueError):
            db.session.rollback()
            logger.debug('User entered date in incorrect format.')
            return {'error': {'message': 'Incorrect date format.', 'status': 400}}
    db.session.flush()
    db.session.commit()
    return db_teacher


def delete_teacher_api(teacher_id) -> dict:
    """
    Delete teacher with current id for reset api
    :param teacher_id: Id of teacher
    :return: Teacher
    """
    try:
        teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
        res = Teacher.query.filter(Teacher.id == teacher_id).delete()
        if not res:
            return {'error': {'message': 'No teacher was found with given id', 'status': 400}}
        db.session.commit()
    except Exception as ex:
        logger.error(str(ex))
        db.session.rollback()
        return {'error': {'message': 'Error deleting from db.', 'status': 400}}
    return teacher
