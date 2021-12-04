"""
This module demonstrates CRUD operations for university model.

It has CRUD functions for website application and for REST-API.

This module includes functions: get_all_universities(), get_university(), create_university(), update_university(),
delete_university(), create_university_api(), delete_university_api(), update_university_api().

This module imports: typing.Any, sqlalchemy.func, app, University, Teacher.
"""
from typing import Any
from sqlalchemy import func
from app import db
from models.university import University
from models.teacher import Teacher


def get_all_universities() -> Any:
    """
    Returns a list of all universities from database. READ method for CRUD controller.
    It also updates average_salary of university where it changed.
    :return: Any
    """
    try:
        universities = University.query.all()
        average_list = list(Teacher.query.with_entities(Teacher.university_id, func.avg(Teacher.salary)).group_by(
            Teacher.university_id).all())
    except Exception as ex:
        # print('Error of taking universities from db', str(ex))
        return []
    for i in range(len(average_list)):
        for j in range(len(universities)):
            if universities[j].id == average_list[i][0]:
                if universities[j].average_salary != average_list[i][1]:
                    db.session.flush()
                universities[j].average_salary = average_list[i][1]
                db.session.commit()
    return universities


def get_university(university_id) -> University:
    """
    Get university with given id.
    :param university_id: Id of university.
    :return: University
    """
    return University.query.get(university_id)


def create_university(university) -> bool:
    """
    Add university to database. CREATE method for CRUD controller. Return true if there weren\'t any exceptions.
    :param university: New university to add to database.
    :return: bool
    """
    try:
        db.session.add(university)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        # print('Error of adding to db', str(ex))
        return False
    return True


def update_university(university, university_id) -> bool:
    """
    Update data of a university with id that was given. UPDATE method for CRUD controller.
    :param university: University object with new data.
    :param university_id: Id of university  to update.
    :return: bool
    """
    is_changed = False
    try:
        db_university = get_university(university_id)
        if university.name:
            if not university.name == db_university.name:
                db_university.name = university.name
                is_changed = True
        if university.location:
            if not university.location == db_university.location:
                db_university.location = university.location
                is_changed = True
        if not is_changed:
            return False
        db.session.flush()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        # print('Error of adding to db', str(ex))
        return False
    return True


def delete_university(university_id) -> bool:
    """
    Delete university from database with id that is given. DELETE method for CRUD controller.
    :param university_id: Id of university to delete.
    :return: bool
    """
    try:
        University.query.filter(University.id == university_id).delete()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        # print('Error of deleting from db', str(ex))
        return False
    return True


def create_university_api(name, location) -> dict:
    """
    Function to creat university for REST-API
    :param name: name of university
    :param location: where is university located
    :return: University
    """
    if not name or not location:
        return {'error': {'message': 'Some data was not given',
                          'status': 400}}
    if not isinstance(name, str) or not isinstance(location, str):
        return {'error': {'message': 'Incorrect data type',
                          'status': 400}}
    if not name.isalnum() or location.isspace():
        return {'error': {'message': 'Some fields contain not allowed symbols',
                          'status': 400}}
    university = University(name, location)
    try:
        db.session.add(university)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        # print(str(ex))
        return {'error': {'message': 'Error of adding to db',
                          'status': 412}}
    return university


def delete_university_api(university_id) -> dict:
    """
    Delete university for REST-API
    :param university_id: id of university to delete
    :return: University
    """
    try:
        university = University.query.filter(University.id == university_id).first()
        University.query.filter(University.id == university_id).delete()
        if not university:
            return {'error': {'message': 'No university was found with given id.',
                              'status': 412}}
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        # print('Error of deleting from db', str(ex))
        return {'error': {'message': 'Error of adding to db',
                          'status': 412}}
    return university


def update_university_api(university_id, name, location) -> dict:
    """
    Update university with given id
    :param name: new name of university
    :param location: new location of university
    :param university_id: Id of university to update
    :return: dict
    """
    try:
        university = get_university(university_id)
        if not university:
            return {'error': {'message': 'No university was found with given id', 'status': 400}}
        is_changed = False

        if name:
            if isinstance(name, str):
                if name.isalnum():
                    if not university.name == name:
                        university.name = name
                        is_changed = True
                else:
                    return {'error': {'message': 'Name contains wrong symbols', 'status': 400}}
            else:
                return {'error': {'message': 'Name is an incorrect data type', 'status': 400}}
        if location:
            if isinstance(location, str):
                if not location.isspace():
                    if not university.location == location:
                        university.location = location
                        is_changed = True
                else:
                    return {'error': {'message': 'Location contains wrong symbols', 'status': 400}}
            else:
                return {'error': {'message': 'Location is an incorrect data type', 'status': 400}}
        if not is_changed:
            return {'error': {'message': 'No new data was given', 'status': 400}}
        db.session.flush()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        # print('Error of adding to db', str(ex))
        return {'error': {'message': 'Error to update university to db', 'status': 412}}
    return university
