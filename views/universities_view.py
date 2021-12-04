"""
This module is made for rendering templates for university pages.

Pages that are rendering are: university.html, add_university.html, update_university.html

This module contains functions: get_all_universities(), add_university(), create_university(), get_update_university(),
update_university(), delete_university().
"""
from views import app, render_template, request, redirect, url_for, flash
from models.university import University
from service import universities_crud


@app.route('/universities', methods=['GET'])
def get_all_universities() -> str:
    """
    Route to render template "universities.html"
    Get all universities from db, count average salary by average salary of every teacher in the university.
    :return: str
    """
    universities = universities_crud.get_all_universities()
    if universities:
        return render_template('universities.html', list=universities, title='University')
    else:
        flash("Error of reading Universities from db,please check if you have table 'University' ", category="error")
        return redirect(url_for('get_all_teachers'))


@app.route('/add_university', methods=['GET'])
def add_university() -> str:
    """
    Route to render a template "add_university.html"
    :return: str
    """
    return render_template('add_university.html', title='Add university')


@app.route('/add_university', methods=["POST"])
def create_university() -> str:
    """
    Route for POST method to create a new university. It also validate data before sending it to database.
    :return: str
    """
    name = request.form['name']
    location = request.form['location']
    university = University(name, location)
    if not name or not location:
        flash("You didn't write all fields please fill in every field", category="error")
        return redirect(url_for('add_university'))
    if not name.isalnum() or not location.isalnum():
        print('Here')
        flash("Fields doesn't contain alphabetic symbols", category="error")
        return redirect(url_for('add_university'))
    if not universities_crud.create_university(university):
        flash("Error of adding university to db", category="error")
        return redirect(url_for('add_university'))
    else:
        flash("University was added", category="success")
        return redirect(url_for('get_all_universities'))


@app.route('/update_university%<int:university_id>', methods=['GET'])
def get_update_university(university_id) -> str:
    """
    Route for GET method to get a certain university and update it
    :param university_id: Id of university
    :return: str
    """
    university = universities_crud.get_university(university_id)
    return render_template('/update_university.html', title='Update university', university=university)


@app.route('/update_university', methods=['POST'])
def update_university() -> str:
    """
    Route method POST to update a certain university. If it is changes or whitespaces, it will not add data to database.
    :return: str
    """
    id = request.form['university_id']
    name = request.form['name']
    location = request.form['location']
    university = University(name, location)
    if not name and not location:
        flash("You didn\'t write anything, please make at least one change", category='error')
        return redirect(url_for('get_update_university', university_id=id))
    if universities_crud.update_university(university, id):
        return redirect(url_for('get_all_universities'))
    else:
        flash('Incorrect data or any new changes, please enter valid data', category='error')
        return redirect(url_for('get_update_university', university_id=id))


@app.route('/delete_university/<int:university_id>', methods=['POST'])
def delete_university(university_id) -> str:
    """
    Route for deleting university. After modal message it delete university and render university page.
    :param university_id: Id of university.
    :return: str
    """
    if universities_crud.delete_university(university_id):
        flash('University was deleted', category='success')
        return redirect(url_for('get_all_universities'))
    else:
        flash('Can\'t delete this university from db', category='error')
        return redirect(url_for('get_all_universities'))
