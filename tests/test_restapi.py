"""
This module run tests for function in module views.teacher_view.

This module contains class TestRestApi. It tests all functions that teacher_view.py file has.

This module imports: app,datetime, unittest.TestCase, unittest.mock.patch,
University, University, teacher_crude
"""

from app import app
import datetime
from flask import jsonify
from unittest import TestCase
from unittest.mock import patch
from models.university import University, UniversitySchema
from models.teacher import Teacher, TeacherSchema

university1 = University('Test1', 'Test1')
university2 = University('Test2', 'Test2')
university3 = University('Test3', 'Test3')
university_list = [university1, university2, university3]
app.testing = True
teacher1 = Teacher('Name1', 'Last_name1', datetime.date(2011, 11, 1), 1000, university1)
teacher2 = Teacher('Name2', 'Last_name2', datetime.date(2010, 8, 21), 800, university2)
teacher3 = Teacher('Name3', 'Last_name3', datetime.date(2011, 2, 17), 1500, university3)
teacher4 = Teacher('Name4', 'Last_name4', datetime.date(2011, 5, 5), 200, university1)
teacher_list = [teacher1, teacher2, teacher3, teacher4]


class TestRestApi(TestCase):
    """
    This class runs all tests for the restapi.py file.

    This class includes functions: setUp(), test_index(),
    test_read_teacher(), test_add_teacher(),
    test_update_teacher(), test_delete_teacher(), test_get_university(),
    test_get_university_by_id(), test_post_university(),
    test_update_university(), test_delete_university()
    """

    def setUp(self) -> None:
        """
        Set up for app for testing
        :return: None
        """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.teacher_scheme = TeacherSchema()

    @patch('rest.restapi.teachers_crud')
    def test_index(self, t_crud) -> None:
        """
        Test get all teachers for REST-API
        :param t_crud: Mock teachers_crud
        :return: None
        """
        # Test if everything is correct.
        t_crud.get_all_teachers.return_value = teacher_list
        with app.app_context():
            teacher_scheme = TeacherSchema(many=True)
            true_response = teacher_scheme.jsonify(teacher_list).data
        response = self.app.get('/api/')
        self.assertEqual(true_response, response.data)

    @patch('rest.restapi.teachers_crud')
    def test_read_teacher(self, t_crud) -> None:
        """
        Test to get teacher with given id in API
        :param t_crud: Mock teacher_crud
        :return: None
        """
        # Test if everything is okay
        t_crud.get_teacher.return_value = teacher1
        with app.app_context():
            teacher_scheme = TeacherSchema()
            true_response = teacher_scheme.jsonify(teacher1).data
        response = self.app.get('/api/1')
        self.assertEqual(true_response, response.data)
        # Test if no university was found
        true_response = {'error': {'message': 'No teacher was found with given id',
                                   'status': 400}}
        t_crud.get_teacher.return_value = None
        response = self.app.get('/api/1')
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)

    @patch('rest.restapi.Teacher')
    @patch('rest.restapi.teachers_crud')
    @patch('rest.restapi.University')
    def test_add_teacher(self, university, t_crud, teacher) -> None:
        """
        Test creation of new teacher with REST-API
        :param university: Mock University class
        :param t_crud: Mock teacher_crud
        :param teacher: Mock University class
        :return: None
        """
        # Test if everything is correct
        university.query.filter_by.return_value.first.return_value = university1
        t_crud.create_teacher.return_value = True
        teacher.return_value = teacher1
        response = self.app.post('/api/', json={'name': teacher1.name,
                                                'last_name': teacher1.last_name,
                                                'birth_date': '2011-9-1',
                                                'salary': teacher1.salary,
                                                'university': teacher1.university.name})
        with app.app_context():
            teacher_scheme = TeacherSchema()
            true_response = teacher_scheme.jsonify(teacher1).data
        self.assertEqual(true_response, response.data)
        # Test if university not in database
        university.query.filter_by.return_value.first.return_value = None
        true_response = {'error': {'message': 'Wrong university name.', 'status': 400}}
        response = self.app.post('/api/', json={'name': teacher1.name,
                                                'last_name': teacher1.last_name,
                                                'birth_date': "2001-10-10",
                                                'salary': teacher1.salary,
                                                'university': teacher1.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)
        # Test if not all fields were written
        true_response = {'error': {'message': 'Some data was not written',
                                   'status': 400}}
        response = self.app.post('/api/', json={'name': None,
                                                'last_name': teacher1.last_name,
                                                'birth_date': "2001-10-10",
                                                'salary': teacher1.salary,
                                                'university': teacher1.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)
        # Test if error in adding to database
        university.query.filter_by.return_value.first.return_value = university1
        t_crud.create_teacher.return_value = False
        true_response = {'error': {'message': 'Can\'t add teacher to database', 'status': 412}}
        response = self.app.post('/api/', json={'name': teacher1.name,
                                                'last_name': teacher1.last_name,
                                                'birth_date': "2001-10-10",
                                                'salary': teacher1.salary,
                                                'university': teacher1.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)
        # Test if exception was raised
        university.query.filter_by.return_value.first.side_effect = Exception
        true_response = {'error': {'message': 'Wrong university name.',
                                   'status': 400}}
        response = self.app.post('/api/', json={'name': teacher1.name,
                                                'last_name': teacher1.last_name,
                                                'birth_date': "2001-10-10",
                                                'salary': teacher1.salary,
                                                'university': teacher1.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)
        # Test if date is in incorrect form
        university.query.filter_by.return_value.first.side_effect = None
        university.query.filter_by.return_value.first.return_value = university1
        true_response = {'error': {'message': 'Incorrect date format.',
                                   'status': 400}}
        response = self.app.post('/api/', json={'name': teacher1.name,
                                                'last_name': teacher1.last_name,
                                                'birth_date': "test",
                                                'salary': teacher1.salary,
                                                'university': teacher1.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)
        # Test if salary in incorrect format
        true_response = {'error': {'message': 'Incorrect salary format.'
                                              ' Salary must be integer.', 'status': 400}}
        response = self.app.post('/api/', json={'name': teacher1.name,
                                                'last_name': teacher1.last_name,
                                                'birth_date': "2001-1-1",
                                                'salary': 'test',
                                                'university': teacher1.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)

    @patch('rest.restapi.teachers_crud')
    def test_update_teacher(self, t_crud) -> None:
        """
        Test update teacher for REST-API
        :param t_crud: Mock teachers_crud
        :return: None
        """
        # Test if everything is correct
        t_crud.get_teacher.return_value = teacher1
        t_crud.update_teacher_api.return_value = teacher2
        response = self.app.patch('/api/1',
                                  json={'name': teacher2.name,
                                        'last_name': teacher2.last_name,
                                        'birth_date': teacher2.birth_date,
                                        'salary': teacher2.salary,
                                        'university': teacher2.university.name})
        with app.app_context():
            teacher_scheme = TeacherSchema()
            true_response = teacher_scheme.jsonify(teacher2).data
        self.assertEqual(true_response, response.data)
        # Test if wrong data given
        t_crud.get_teacher.return_value = teacher1
        t_crud.update_teacher_api.return_value = {'error': {'message': f'No data was given.',
                                                            'status': 400}}
        true_response = {'error': {'message': 'No data was given.', 'status': 400}}
        response = self.app.patch('/api/1',
                                  json={'name': teacher2.name,
                                        'last_name': teacher2.last_name,
                                        'birth_date': teacher2.birth_date,
                                        'salary': teacher2.salary,
                                        'university': teacher2.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)
        # Test if wrong teacher id was given
        t_crud.get_teacher.return_value = None
        true_response = {'error': {'message': 'Wrong teacher id.', 'status': 400}}
        response = self.app.patch('/api/1',
                                  json={'name': teacher2.name,
                                        'last_name': teacher2.last_name,
                                        'birth_date': teacher2.birth_date,
                                        'salary': teacher2.salary,
                                        'university': teacher2.university.name})
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)

    @patch('rest.restapi.teachers_crud')
    def test_delete_teacher(self, t_crud) -> None:
        """
        Test to delete data in REST-API
        :param t_crud: Mock teachers_crud
        :return: None
        """
        # Test if everything is correct
        t_crud.delete_teacher_api.return_value = teacher1
        response = self.app.delete('/api/1')
        with app.app_context():
            teacher_scheme = TeacherSchema()
            true_response = teacher_scheme.jsonify(teacher1).data
        self.assertEqual(true_response, response.data)
        # Test if wrong id was given
        t_crud.delete_teacher_api.return_value = {'error': {'message': 'No teacher was found with given id',
                                                            'status': 400}}
        true_response = {'error': {'message': 'No teacher was found with given id', 'status': 400}}
        response = self.app.delete('/api/1')
        with app.app_context():
            true_response = jsonify(true_response).data
        self.assertEqual(true_response, response.data)

    @patch('rest.restapi.Teacher')
    def test_search_by_date(self, teacher) -> None:
        """
        Test search by date for REST-API
        :param teacher: Mock Teacher class
        :return: None
        """
        # Test if everything is okay
        teacher.query.filter.return_value = teacher_list
        response = self.app.post('/api/search_by_date',
                                 json={"date_from": '2011-01-01',
                                       "date_to": '2012-01-01'})
        with app.app_context():
            teacher_schema = TeacherSchema(many=True)
            return_response = teacher_schema.jsonify(teacher_list).data
        self.assertEqual(return_response, response.data)
        # Test if some date was not writen
        response = self.app.post('/api/search_by_date',
                                 json={"date_from": None, "date_to": '2012-01-01'})
        with app.app_context():
            return_response = jsonify({'error': {'message': 'Some date was not given.',
                                                 'status': 400}}).data
        self.assertEqual(return_response, response.data)
        # Test if dates is not in string form
        response = self.app.post('/api/search_by_date',
                                 json={"date_from": 3, "date_to": '2012-01-01'})
        with app.app_context():
            return_response = jsonify({'error': {'message': 'Date must by given in string form.',
                                                 'status': 400}}).data
        self.assertEqual(return_response, response.data)
        # Test if exception was raised
        response = self.app.post('/api/search_by_date',
                                 json={"date_from": '2011-12afs-asd1', "date_to": '2012-01-01'})
        with app.app_context():
            return_response = jsonify({'error': {'message': 'Date is in wrong format'
                                                            ' should be year-month-day',
                                                 'status': 400}}).data
        self.assertEqual(return_response, response.data)

    @patch('rest.restapi.universities_crud')
    def test_get_university(self, u_crud) -> None:
        """
        Test get all universities for REST-API
        :param u_crud: Mock universities_crud
        :return: None
        """
        u_crud.get_all_universities.return_value = university_list
        with app.app_context():
            university_scheme = UniversitySchema(many=True)
            true_response = university_scheme.jsonify(university_list).data
        response = self.app.get('/api/university').data
        self.assertEqual(true_response, response)

    @patch('rest.restapi.universities_crud')
    def test_get_university_by_id(self, u_crud) -> None:
        """
        Test to get university with given id in REST-API
        :param u_crud: Mock universities_crud
        :return: None
        """
        # Test if everything is correct
        u_crud.get_university.return_value = university1
        with app.app_context():
            university_scheme = UniversitySchema()
            true_response = university_scheme.jsonify(university1).data
        response = self.app.get('/api/university/1').data
        self.assertEqual(true_response, response)
        # Test if exception was raised
        u_crud.get_university.return_value = None
        with app.app_context():
            true_response = jsonify({'error': {'message': 'No university was found'
                                                          ' with given id', 'status': 400}}).data
        response = self.app.get('/api/university/1').data
        self.assertEqual(true_response, response)

    @patch('rest.restapi.universities_crud')
    def test_post_university(self, u_crud):
        """
        Test post university method for REST-API
        :param u_crud: Mock universities_crud
        :return: None
        """
        # Test if everything is okay
        u_crud.create_university_api.return_value = university2
        response = self.app.post('/api/university',
                                 json={'name': university2.name, 'location': university2.location})
        with app.app_context():
            university_scheme = UniversitySchema()
            true_response = university_scheme.jsonify(university2).data
        self.assertEqual(true_response, response.data)
        # Test if exception was raised
        u_crud.create_university_api.return_value = {'error': {'message': 'Incorrect data type', 'status': 400}}
        true_response = {'error': {'message': 'Incorrect data type', 'status': 400}}
        with app.app_context():
            true_response = jsonify(true_response).data
        response = self.app.post('/api/university',
                                 json={'name': university2.name, 'location': university2.location})
        self.assertEqual(true_response, response.data)

    @patch('rest.restapi.universities_crud')
    def test_update_university(self, u_crud) -> None:
        """
        Test update university for REST-API
        :param u_crud: Mock university_crud
        :return: None
        """
        u_crud.update_university_api.return_value = university2
        response = self.app.patch('/api/university/1',
                                  json={'name': university2.name, 'location': university2.location})
        with app.app_context():
            university_scheme = UniversitySchema()
            true_response = university_scheme.jsonify(university2).data
        self.assertEqual(true_response, response.data)
        # Test if exception was raised
        u_crud.update_university_api.return_value = \
            {'error': {'message': 'Incorrect data type', 'status': 400}}
        true_response = {'error': {'message': 'Incorrect data type', 'status': 400}}
        with app.app_context():
            true_response = jsonify(true_response).data
        response = self.app.patch('/api/university/1',
                                  json={'name': university2.name, 'location': university2.location})
        self.assertEqual(true_response, response.data)

    @patch('rest.restapi.universities_crud')
    def test_delete_university(self, u_crud) -> None:
        """
        Test delete university for REST-API
        :param u_crud: Mock universities_crud
        :return: None
        """
        u_crud.delete_university_api.return_value = university1
        response = self.app.delete('/api/university/1',
                                   json={'name': university1.name, 'location': university1.location})
        with app.app_context():
            university_scheme = UniversitySchema()
            true_response = university_scheme.jsonify(university1).data
        self.assertEqual(true_response, response.data)
        # Test if exception was raised
        u_crud.delete_university_api.return_value = {'error': {'message': 'Incorrect data type', 'status': 400}}
        true_response = {'error': {'message': 'Incorrect data type', 'status': 400}}
        with app.app_context():
            true_response = jsonify(true_response).data
        response = self.app.delete('/api/university/1', json={'name': university1.name,
                                                              'location': university1.location})
        self.assertEqual(true_response, response.data)
