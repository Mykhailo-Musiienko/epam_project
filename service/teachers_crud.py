from app import db
from models.teacher import Teacher


def get_all_teachers():
    return Teacher.query.all()


def get_teacher(id) -> Teacher:
    return Teacher.query.get(id)


def create_teacher(teacher) -> bool:
    try:
        db.session.add(teacher)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print('Error of adding to db', str(ex))
        return False
    return True


def update_teacher(teacher: Teacher, teacher_id: int) -> bool:
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
            if not teacher.salary == db_teacher.salary:
                db_teacher.salary = teacher.salary
                is_changed = True
        if teacher.university:
            if not teacher.university == db_teacher.university:
                db_teacher.university = teacher.unievrsity
                is_changed = True
        if not is_changed:
            return False
        db.session.flush()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print('Error of updating data to db', str(ex))
        return False
    return True


def delete_teacher(teacher_id):
    try:
        Teacher.query.filter(Teacher.id == teacher_id).delete()
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print('Error of deleting from db', str(ex))
        return False
    return True
