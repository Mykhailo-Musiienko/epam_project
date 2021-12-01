from typing import Any
from sqlalchemy import func
from app import db
from models.university import University
from models.teacher import Teacher


def get_all_universities() -> Any:
    """
    Returns a list of all universities from database.READ method for CRUD controller.
    It also update average_salary of university where it changed.
    :return: Any
    """
    try:
        universities = University.query.all()
        average_list = list(Teacher.query.with_entities(Teacher.university_id, func.avg(Teacher.salary)).group_by(
            Teacher.university_id).all())
    except Exception as ex:
        print('Error of taking universities from db', str(ex))
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
        print('Error of adding to db', str(ex))
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
        print('Error of adding to db', str(ex))
        return False
    return True


def delete_university(university_id) -> bool:
    """
    Delete universiy from database with id that is given. DELETE method for CRUD controller.
    :param university_id: Id of university to delete.
    :return: bool
    """
    try:
        University.query.filter(University.id == university_id).delete()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print('Error of deleting from db', str(ex))
        return False
    return True
