"""
This module run tests for function in module views.teacher_view.

This module contains class TestTeacherView. It tests all functions that teacher_view.py file has.

This module imports: app,datetime,unittest.TestCase, unittest.mock.patch, Teacher, University, teacher_crude
"""


from app import app
import datetime
from unittest import TestCase
from unittest.mock import patch
from models.university import University


class TestTeacher:
    """
    Class Teacher for tests.

    TestTeacher has __init__ function
    """

    def __init__(self, id, name, last_name, birth_date, salary, university) -> None:
        """
        Constructor of class TestTeacher
        :param id: Teacher's id
        :param name: Teacher's name
        :param last_name: Teacher's last name
        :param birth_date: When teacher was born
        :param salary: Teacher's salary
        :param university: University where teacher works
        """
        self.id = id
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.salary = salary
        self.university = university


university1 = University('Test1', 'Test1')
university2 = University('Test2', 'Test2')
university3 = University('Test3', 'Test3')
university_list = [university1, university2, university3]
app.testing = True
teacher1 = TestTeacher(1, 'Name1', 'Last_name1', datetime.date(2011, 11, 1), 1000, university1)
teacher2 = TestTeacher(2, 'Name2', 'Last_name2', datetime.date(2010, 8, 21), 800, university2)
teacher3 = TestTeacher(3, 'Name3', 'Last_name3', datetime.date(2011, 2, 17), 1500, university3)
teacher4 = TestTeacher(4, 'Name4', 'Last_name4', datetime.date(2011, 5, 5), 200, university1)
teacher_list = [teacher1, teacher2, teacher3, teacher4]


class TestTeacherView(TestCase):
    """
    This class runs all tests for the module views.teacher_view.

    It includes functions: setUp(), test_get_all_teachers(), test_get_add_teacher(), test_add_teacher(),
    test_get_update_teacher(), test_update_teacher(), test_search_by_date(), test_delete_teacher().

    It inherited from class TestCase
    """
    def setUp(self) -> None:
        """
        Set up for app for testing
        :return:
        """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    @patch('views.teacher_view.teachers_crud')
    def test_get_all_teachers(self, teachers_crud) -> None:
        """
        Test to get status of main page
        :return: None
        """
        # Test for status code
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # Test for data in response 
        teachers_crud.get_all_teachers.return_value = teacher_list
        response = self.app.get('/', content_type='html/text')
        data = response.get_data(as_text=str)
        self.assertIn(teacher1.name, data)
        self.assertIn(teacher2.last_name, data)
        self.assertIn(str(teacher3.salary), data)

    def test_get_add_teacher(self) -> None:
        """
        Test to get page add_teacher.html
        :return: None
        """
        # Test for status code
        response = self.app.get('/add_teacher', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    @patch('views.teacher_view.teachers_crud.create_teacher')
    @patch('views.teacher_view.Teacher')
    def test_add_teacher(self, teacher, create) -> None:
        """
        Test for Post method in view add_teacher.html
        :param teacher: Mock teacher class
        :param create: Mock function create_teacher()
        :return: None
        """
        # Test for status code
        teacher.return_value = teacher1
        create.return_value = True
        # Test if everything is correct
        response = self.app.post('/add_teacher',
                                 data=dict(name='name',
                                           last_name='last_name',
                                           birth_date=teacher1.birth_date,
                                           salary=teacher1.salary,
                                           university=teacher1.university.name),
                                 follow_redirects=True)
        true_response = 'Teacher was added'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if some fields weren't given
        response = self.app.post('/add_teacher',
                                 data=dict(last_name='last_name',
                                           birth_date=teacher1.birth_date,
                                           salary=teacher1.salary,
                                           university=teacher1.university.name),
                                 follow_redirects=True)
        true_response = 'You didn&#39;t enter some fields, please enter all fields'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if exception raised
        create.return_value = False
        response = self.app.post('/add_teacher',
                                 data=dict(name='name',
                                           last_name='last_name',
                                           birth_date=teacher1.birth_date,
                                           salary=teacher1.salary,
                                           university=teacher1.university.name),
                                 follow_redirects=True)
        true_response = 'You didn&#39;t enter some fields, please enter all fields'
        self.assertIn(true_response, response.get_data(as_text=True))

    @patch('views.teacher_view.universities_crud')
    @patch('views.teacher_view.teachers_crud')
    def test_get_update_teacher(self, t_crud, u_crud) -> None:
        """
        Test get method for page update_teacher.html
        :param t_crud: Mock universities_crud
        :param u_crud: Mock teachers_crud
        :return: None
        """
        # Test if placeholders contain teacher's attributes.
        t_crud.get_teacher.return_value = teacher1
        u_crud.get_all_universities.return_value = university_list
        response = self.app.get('update_teacher/0', content_type='html/text')
        self.assertIn(f'placeholder="{teacher1.name}"', response.get_data(as_text=True))
        self.assertIn(f'placeholder="{teacher1.last_name}"', response.get_data(as_text=True))
        self.assertIn(f'placeholder="{teacher1.salary}"', response.get_data(as_text=True))

    @patch('views.teacher_view.teachers_crud')
    @patch('views.teacher_view.University')
    def test_update_teacher(self, university, t_crud) -> None:
        """
        Test Post method in page update_teacher.html
        :param university: Mock university class
        :param t_crud: Mock teachers_crud
        :return: None
        """
        # Test if everything is correct
        university.query.filter_by.return_value.first.return_value = university1
        t_crud.update_teacher.return_value = True
        response = self.app.post('/update_teacher',
                                 data=dict(teacher_id=teacher1.id,
                                           name='name',
                                           last_name='last_name',
                                           birth_date=teacher1.birth_date,
                                           salary=teacher1.salary,
                                           university=teacher1.university.name),
                                 follow_redirects=True)
        true_response = 'Teacher was updated'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if no data was given
        response = self.app.post('/update_teacher',
                                 data=dict(teacher_id=teacher1.id,
                                           name=None,
                                           last_name=None,
                                           birth_date=None,
                                           salary=None,
                                           university=None),
                                 follow_redirects=True)
        true_response = 'Incorrect data, please enter valid data'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Check if redirects back to this page
        self.assertIn('<h1>Update Teacher</h1>', response.get_data(as_text=True))
        # Test if exception was raised
        t_crud.update_teacher.return_value = False
        response = self.app.post('/update_teacher',
                                 data=dict(teacher_id=teacher1.id,
                                           name='name',
                                           last_name='last_name',
                                           birth_date=teacher1.birth_date,
                                           salary=teacher1.salary,
                                           university=teacher1.university.name),
                                 follow_redirects=True)
        true_response = 'Incorrect data or any new changes, please enter valid data'
        self.assertIn(true_response, response.get_data(as_text=True))

    @patch('views.teacher_view.Teacher')
    def test_search_by_date(self, teacher) -> None:
        """
        Test option 'search by date' in teachers.html page
        :param teacher: Mock Teacher class
        :return: None
        """
        # Test of filtering dates
        teacher.query.filter.return_value = teacher_list
        response = self.app.post('search_by_date', data=dict(
            date_from=teacher1.birth_date,
            date_to=teacher1.birth_date),
                                 follow_redirects=True)
        self.assertIn(f'{teacher1.name}', response.get_data(as_text=True))
        self.assertIn(f'{teacher2.name}', response.get_data(as_text=True))
        self.assertIn(f'{teacher3.name}', response.get_data(as_text=True))
        # Test if some dates were not entered
        response = self.app.post('search_by_date', data=dict(
            date_from=None,
            date_to=None), follow_redirects=True)
        true_response = 'Please enter two dates and then click to search'
        self.assertIn(true_response, response.get_data(as_text=True))

    @patch('views.teacher_view.teachers_crud')
    def test_delete_teacher(self, t_crud) -> None:
        """
        Test to delete teacher.
        :param t_crud: Mock teachers_crud
        :return: None
        """
        # Test if everything is correct
        t_crud.delete_teacher.return_value = True
        response = self.app.post('/delete_teacher/1', follow_redirects=True)
        true_response = 'Teacher was deleted'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if exception was raised
        t_crud.delete_teacher.return_value = False
        response = self.app.post('/delete_teacher/1', follow_redirects=True)
        true_response = 'Error of deleting this Teacher'
        self.assertIn(true_response, response.get_data(as_text=True))
