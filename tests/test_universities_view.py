"""
This module run tests for function in module views.teacher_view.

This module contains class TestTeacherView. It tests all functions that teacher_view.py file has.

This module imports: app,datetime,unittest.TestCase, unittest.mock.patch, Teacher, University, teacher_crude
"""

from app import app
from unittest import TestCase
from unittest.mock import patch


class TestUniversity:
    """
    University class for tests.

    Class include __init__ function.
    """

    def __init__(self, id, name, location):
        """
        Constructor for class TestUniversity
        :param id: Id of university
        :param name: University name
        :param location: University location
        """
        self.id = id
        self.name = name
        self.location = location


university1 = TestUniversity(1, 'Name1', 'Location1')
university2 = TestUniversity(2, 'Name2', 'Location2')
university3 = TestUniversity(3, 'Name3', 'Location3')
university_list = [university1, university2, university3]
app.testing = True


class TestUniversitiesView(TestCase):
    """
    This class is made for testing universities_view.py file.

    It includes functions: setUp(), test_get_all_universities(), test_add_university(), test_create_university(),
    test_add_university(), test_get_update_university(), test_delete_university()
    """

    def setUp(self) -> None:
        """
        Set up for app for testing
        :return: None
        """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    @patch('views.universities_view.universities_crud')
    def test_get_all_universities(self, u_crud) -> None:
        """
        Test univesity main page.
        :param u_crud: Mock universities_crud
        :return: None
        """
        # Test for 200 response
        u_crud.get_all_universities.return_value = university_list
        response = self.app.get('/universities', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # Test if exception was raised
        true_response = "Error of reading Universities from db,please check if you have table &#39;University&#39; "
        u_crud.get_all_universities.return_value = None
        response = self.app.get('/universities', content_type='html/text', follow_redirects=True)
        self.assertIn(true_response, response.get_data(as_text=True))

    def test_add_university(self) -> None:
        """
        Test get method on page add_university.html.
        :return: None
        """
        response = self.app.get('/add_university')
        self.assertIn('Add university', response.get_data(as_text=True))

    @patch('views.universities_view.universities_crud')
    def test_create_university(self, u_crud):
        # Test if everything is correct
        u_crud.create_university.return_value = True
        response = self.app.post('/add_university', data=dict(
            name=university1.name,
            location=university1.location),
                                 follow_redirects=True)
        true_response = 'University was added'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if some fields were not written
        response = self.app.post('/add_university', data=dict(
            name=None,
            location=university1.location),
                                 follow_redirects=True)
        true_response = "You didn&#39;t write all fields please fill in every field"
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if some fields contain incorrect symbols
        response = self.app.post('/add_university', data=dict(
            name='@#$%^&*(',
            location=university1.location), follow_redirects=True)
        true_response = "Fields doesn&#39;t contain alphabetic symbols"
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if exception was raised
        u_crud.create_university.return_value = False
        response = self.app.post('/add_university', data=dict(
            name=university1.name,
            location=university1.location), follow_redirects=True)
        true_response = 'Error of adding university to db'
        self.assertIn(true_response, response.get_data(as_text=True))

    @patch('views.universities_view.universities_crud')
    def test_get_update_university(self, u_crud) -> None:
        """
        Test get method on page update_university
        :param u_crud: Mock universities_crud
        :return: None
        """
        # Test if everything is correct
        u_crud.get_university.return_value = university1
        response = self.app.get('/update_university%251', follow_redirects=True)
        self.assertIn(f'{university1.name}', response.get_data(as_text=True))
        self.assertIn(f'{university1.location}', response.get_data(as_text=True))

    @patch('views.universities_view.universities_crud')
    def test_update_university(self, u_crud) -> None:
        """
        Test post method on update_university.html page
        :param u_crud: Mock universities_crud
        :return: None
        """
        # Test if everything is correct
        u_crud.update_university.return_value = True
        response = self.app.post('/update_university', data=dict(university_id=university1.id,
                                                                 name=university1.name,
                                                                 location=university1.location),
                                 follow_redirects=True)
        true_response = 'University was updated'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if name and location were not written
        response = self.app.post('/update_university', data=dict(university_id=university1.id,
                                                                 name=None,
                                                                 location=None),
                                 follow_redirects=True)
        true_response = 'You didn&#39;t write anything, please make at least one change'
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if exception was raised
        u_crud.update_university.return_value = False
        response = self.app.post('/update_university', data=dict(university_id=university1.id,
                                                                 name=university1.name,
                                                                 location=university1.location),
                                 follow_redirects=True)
        true_response = 'Incorrect data or any new changes, please enter valid data'
        self.assertIn(true_response, response.get_data(as_text=True))

    @patch('views.universities_view.universities_crud')
    def test_delete_university(self, u_crud) -> None:
        """
        Test delete method on main university page.
        :param u_crud: Mock universities_crud
        :return: None
        """
        # Test if everything is correct
        u_crud.delete_university.return_value = True
        true_response = 'University was deleted'
        response = self.app.post('/delete_university/0', follow_redirects=True)
        self.assertIn(true_response, response.get_data(as_text=True))
        # Test if exception was raised
        u_crud.delete_university.return_value = False
        response = self.app.post('/delete_university/0', follow_redirects=True)
        true_response = 'Can&#39;t delete this university from db'
        self.assertIn(true_response, response.get_data(as_text=True))
