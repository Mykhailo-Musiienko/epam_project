"""
This module is made for rendering templates for teacher pages.

Pages that are rendering are: teacher.html, add_teacher.html, update_teacher.html

This module contains functions: get_all_teachers(), get_add_teacher(), add_teacher(),
get_update_teacher(), update_teacher(), search_by_date(), delete_teacher().
"""
from flask import Response
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from views import app
from app import logger
from models.teacher import Teacher
from models.university import University
from service import universities_crud
from service import teachers_crud


@app.route('/', methods=['GET'])
def get_all_teachers() -> str:
    """
    Render main page "teachers.html", get every teacher from database.
    :return: str
    """
    teachers = teachers_crud.get_all_teachers()
    logger.debug('Route teacher.html is rendered.')
    return render_template('teachers.html', title="Teachers", teachers=teachers)


@app.route('/add_teacher', methods=['GET'])
def get_add_teacher() -> str:
    """
    Render page "add_teacher.html" Get all universities for this page to show a list of available
    universities.
    :return: str
    """
    universities = universities_crud.get_all_universities()
    logger.debug('Route create new teacher is rendered')
    return render_template('add_teacher.html', title='Add teachers', universities=universities)


@app.route('/add_teacher', methods=['POST'])
def add_teacher() -> Response:
    """
    Route with POST method to redirect to the "teachers.page". It checks validation of data
    before making database request.
    :return: Response
    """
    logger.debug('User click to submit new teacher')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    birth_date = request.form.get('birth_date')
    salary = request.form.get('salary')
    university = request.form.get('university')
    university_db = University.query.filter_by(name=university).first()
    new_teacher = Teacher(name, last_name, birth_date, salary, university_db)
    if not name or not last_name or not birth_date or not salary or not university:
        flash('You didn\'t enter some fields, please enter all fields', category='error')
        logger.debug('Some fields were not entered')
        return redirect(url_for('add_teacher'))
    if teachers_crud.create_teacher(new_teacher):
        flash('Teacher was added', category='success')
        logger.debug('Teacher was successfully added.')
        return redirect(url_for('get_all_teachers'))
    flash('You didn\'t enter some fields, please enter all fields', category='error')
    logger.debug('User did not enter some fields')
    return redirect(url_for('add_teacher'))


@app.route('/update_teacher%<int:teacher_id>', methods=['GET'])
def get_update_teacher(teacher_id) -> str:
    """
    Route with GET method to render "update_teacher.html" page. It takes current teacher
    by given id and all universities to give user a choice to change current university.
    :param teacher_id: Id of teacher.
    :return: str
    """
    teacher = teachers_crud.get_teacher(teacher_id)
    universities = universities_crud.get_all_universities()
    logger.debug(f'User click to update teacher with id {teacher_id}')
    return render_template('update_teacher.html', title='Update teachers',
                           universities=universities, teacher=teacher)


@app.route('/update_teacher', methods=['POST'])
def update_teacher() -> Response:
    """
    Route updates teacher. It als o check validation before sending a database request.
    :return: Response
    """
    logger.debug('User click to update teacher')
    teacher_id = request.form.get('teacher_id')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    birth_date = request.form.get('birth_date')
    salary = request.form.get('salary')
    university = request.form.get('university')
    university_db = University.query.filter_by(name=university).first()
    new_teacher = Teacher(name, last_name, birth_date, salary, university_db)
    if not name and not last_name and not birth_date and not university and not salary:
        flash('Incorrect data, please enter valid data', category='error')
        logger.debug('User entered incorrect data to form fields.')
        return redirect(url_for('get_update_teacher', teacher_id=teacher_id))
    if teachers_crud.update_teacher(new_teacher, teacher_id):
        flash('Teacher was updated', category='success')
        logger.debug('Teacher was successfully updated.')
        return redirect(url_for('get_all_teachers'))
    flash('Incorrect data or any new changes, please enter valid data', category='error')
    logger.debug('User did not entered any new data')
    return redirect(url_for('get_update_teacher', teacher_id=teacher_id))


@app.route('/search_by_date', methods=['POST'])
def search_by_date() -> Response:
    """
    Route with POST method that search in interval of two dates
    and return appropriate teachers to main page.
    :return: Response
    """
    logger.debug('User click to search teachers in date intervals')
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    if not date_to or not date_from:
        flash("Please enter two dates and then click to search",category='error')
        logger.debug('User did not entered all dates in date form.')
        return redirect(url_for('get_all_teachers'))
    teachers = Teacher.query.filter(Teacher.birth_date.between(date_from, date_to))
    logger.debug(f'Teachers in interval {date_from} to {date_to} were found.')
    return render_template('teachers.html', title="Teachers", teachers=teachers)


@app.route('/delete_teacher/<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id) -> Response:
    """
    Route delete teacher by given id. After it reload the page.
    :param teacher_id: Id of teacher.
    :return: str
    """
    logger.debug(f'User click delete teacher with id {teacher_id}.')
    res = teachers_crud.delete_teacher(teacher_id)
    if res:
        flash("Teacher was deleted", category='success')
        logger.debug(f'Teacher with {teacher_id} was deleted.')
    else:
        flash("Error of deleting this Teacher", category='error')
        logger.error('Error of deleting this Teacher.')
    return redirect(url_for('get_all_teachers'))


if __name__ == '__main__':
    app.run(debug=True)
