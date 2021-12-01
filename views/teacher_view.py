from views import app
from views import render_template
from views import request
from views import redirect
from views import url_for
from views import flash
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
    return render_template('teachers.html', title="Teachers", teachers=teachers)


@app.route('/add_teacher', methods=['GET'])
def get_add_teacher() -> str:
    """
    Render page "add_teacher.html" Get all universities for this page to show a list of available universities.
    :return: str
    """
    universities = universities_crud.get_all_universities()
    return render_template('add_teacher.html', title='Add teachers', universities=universities)


@app.route('/add_teacher', methods=['POST'])
def add_teacher() -> str:
    """
    Route with POST method to redirect to the "teachers.page". It checks validation of data before making
    database request.
    :return: str
    """
    name = request.form['name']
    last_name = request.form['last_name']
    birth_date = request.form['birth_date']
    salary = request.form['salary']
    university = request.form['university']
    university_db = University.query.filter_by(name=university).first()
    new_teacher = Teacher(name, last_name, birth_date, salary, university_db)
    if not name or not last_name or not birth_date or not salary or not university:
        flash('You didn\'t enter some fields, please enter all fields', category='error')
        return redirect(url_for('add_teacher'))
    if teachers_crud.create_teacher(new_teacher):
        flash('Teacher was added', category='success')
        return redirect(url_for('get_all_teachers'))
    else:
        flash('You didn\'t enter some fields, please enter all fields', category='error')
        return redirect(url_for('add_teacher'))


@app.route('/update_teacher%<int:teacher_id>', methods=['GET'])
def get_update_teacher(teacher_id) -> str:
    """
    Route with GET method to render "update_teacher.html" page. It takes current teacher by given id and all
    universities to give user a choice to change current university.
    :param teacher_id: Id of teacher.
    :return:
    """
    teacher = teachers_crud.get_teacher(teacher_id)
    universities = universities_crud.get_all_universities()
    return render_template('update_teacher.html', title='Update teachers', universities=universities, teacher=teacher)


@app.route('/update_teacher', methods=['POST'])
def update_teacher() -> str:
    """
    Route updates teacher. It als o check validation before sending a database request.
    :return: str
    """
    id = request.form['teacher_id']
    name = request.form['name']
    last_name = request.form['last_name']
    birth_date = request.form['birth_date']
    salary = request.form['salary']
    university = request.form['university']
    university_db = University.query.filter_by(name=university).first()
    new_teacher = Teacher(name, last_name, birth_date, salary, university_db)
    if not name and not last_name and not birth_date and not university and not salary:
        flash('Incorrect data, please enter valid data', category='error')
        return redirect(url_for('get_update_teacher', teacher_id=id))
    if teachers_crud.update_teacher(new_teacher, id):
        return redirect(url_for('get_all_teachers'))
    else:
        flash('Incorrect data or any new changes, please enter valid data', category='error')
        return redirect(url_for('get_update_teacher', teacher_id=id))


@app.route('/search_by_date', methods=['POST'])
def search_by_date() -> str:
    """
    Route with POST method that search in interval of two dates and return appropriate teachers to main page.
    :return: str
    """
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    teachers = Teacher.query.filter(Teacher.birth_date.between(date_from, date_to))
    return render_template('teachers.html', title="Teachers", teachers=teachers)


@app.route('/delete_teacher%<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id) -> str:
    """
    Route delete teacher by given id. After it reload the page.
    :param teacher_id: Id of teacher.
    :return: str
    """
    print(teacher_id)
    res = teachers_crud.delete_teacher(teacher_id)
    if res:
        flash("Teacher was deleted", category='success')
    else:
        flash("Error of deleting this Teacher", category='error')
    return redirect(url_for('get_all_teachers'))


if __name__ == '__main__':
    app.run(debug=True)
