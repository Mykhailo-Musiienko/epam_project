"""
This module is made for rendering templates for university pages.

Pages that are rendering are: university.html, add_university.html, update_university.html

This module contains functions: get_all_universities(), add_university(), create_university(),
get_update_university(),
update_university(), delete_university().
"""
from typing import Union
from werkzeug import Response
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from app import app
from app import logger

from models.university import University
from service import universities_crud


@app.route('/universities', methods=['GET'])
def get_all_universities() -> Union[str, Response]:
    """
    Route to render template "universities.html"
    Get all universities from db, count average salary
    by average salary of every teacher in the university.
    :return: Response
    """
    logger.debug('university.page was shown')
    universities = universities_crud.get_all_universities()
    if universities:
        logger.debug('Got universities from database')
        return render_template('universities.html', list=universities, title='University')
    flash("Error of reading Universities from db,please check if you have table 'University' ",
          category="error")
    logger.error('Error of reading Universities from db.')
    return redirect(url_for('get_all_teachers'))


@app.route('/add_university', methods=['GET'])
def add_university() -> str:
    """
    Route to render a template "add_university.html"
    :return: str
    """
    logger.debug('Page add_university.html was shown.')
    return render_template('add_university.html', title='Add university')


@app.route('/add_university', methods=["POST"])
def create_university() -> Response:
    """
    Route for POST method to create a new university.
    It also validates data before sending it to database.
    :return: Response
    """
    logger.error('User click submit button to create new university.')
    name = request.form.get('name')
    location = request.form.get('location')
    university = University(name, location)
    if not name or not location:
        flash("You didn't write all fields please fill in every field", category="error")
        logger.debug('User did not write all fields in field form.')
        return redirect(url_for('add_university'))
    if not name.isalnum() or location.isspace():
        flash("Fields doesn't contain alphabetic symbols", category="error")
        logger.debug('User entered invalid symbols')
        return redirect(url_for('add_university'))
    if not universities_crud.create_university(university):
        flash("Error of adding university to db", category="error")
        logger.error('Error of adding university to db.')
        return redirect(url_for('add_university'))
    flash("University was added", category="success")
    logger.debug('University was added')
    return redirect(url_for('get_all_universities'))


@app.route('/update_university%<int:university_id>', methods=['GET'])
def get_update_university(university_id) -> str:
    """
    Route for GET method to get a certain university and update it
    :param university_id: Id of university
    :return: str
    """
    logger.debug(f'Page update_university was show with university id {university_id}')
    university = universities_crud.get_university(university_id)
    return render_template('/update_university.html', title='Update university',
                           university=university)


@app.route('/update_university', methods=['POST'])
def update_university() -> Response:
    """
    Route method POST to update a certain university. If it is changes or whitespaces,
    it will not add data to database.
    :return: Response
    """
    logger.debug('User click to update university')
    university_id = request.form.get('university_id')
    name = request.form.get('name')
    location = request.form.get('location')
    university = University(name, location)
    if not name and not location:
        flash("You didn\'t write anything, please make at least one change", category='error')
        logger.debug('User did not write anything to the field form')
        return redirect(url_for('get_update_university', university_id=university_id))
    if universities_crud.update_university(university, university_id):
        flash('University was updated', category='success')
        logger.debug('University was updated')
        return redirect(url_for('get_all_universities'))
    flash('Incorrect data or any new changes, please enter valid data', category='error')
    logger.debug('User write incorrect data or any new changes')
    return redirect(url_for('get_update_university', university_id=university_id))


@app.route('/delete_university/<int:university_id>', methods=['POST'])
def delete_university(university_id) -> Response:
    """
    Route for deleting university. After modal message it delete university and
    render university page.
    :param university_id: Id of university.
    :return: Response
    """
    logger.debug(f'User click to delete university with id {university_id}')
    if universities_crud.delete_university(university_id):
        flash('University was deleted', category='success')
        logger.debug('University was successfully deleted.')
        return redirect(url_for('get_all_universities'))
    flash('Can\'t delete this university from db', category='error')
    logger.error('Can\'t delete this university from db.')
    return redirect(url_for('get_all_universities'))
