"""
This module run tests for  function in module service.universities_crud.

This module contains class Test

This module imports: app,datetime,unittest.TestCase, unittest.mock.patch, Teacher, University, teacher_crude
"""

from app import app
from unittest import TestCase
from unittest.mock import patch
from models.university import University
from service import universities_crud

university1 = University('Test1', 'Test1')
university2 = University('Test2', 'Test2')
university3 = University('Test3', 'Test3')
list_university = [university1, university2, university3]
app.testing = True


class TestUniversityCrud(TestCase):
    """
    This class runs all tests for the module service.universities_crud.

    It includes: test test_get_all_universities, test_get_university, test_create_university, test_update_university,
    test_delete_university, test_create_university_api, test_delete_university_api, test_update_university_api

    It inherited from class TestCase
    """

    @patch('service.universities_crud.University')
    def test_get_all_universities(self, university) -> None:
        """
        Test to get all unievrsities
        :param university: Mock class University
        :return: None
        """
        university.query.all.return_value = list_university
        result = universities_crud.get_all_universities()
        self.assertEqual(result, list_university)

        university.query.all.side_effect = Exception
        result = universities_crud.get_all_universities()
        self.assertEqual(result, [])

    @patch('service.universities_crud.University')
    def test_get_university(self, university) -> None:
        """
        Test to get university by given id
        :param university: Mock class university
        :return: None
        """
        university.query.get.return_value = university3
        result = universities_crud.get_university(1)
        self.assertEqual(result, university3)

    @patch('service.universities_crud.db')
    def test_create_university(self, db) -> None:
        """
        Test to create new university to database.
        :param db: Mock class SQLAlchemy
        :return: None
        """
        db.session.add.return_value = 1
        db.session.commit.return_value = 1
        result = universities_crud.create_university(university1)
        self.assertEqual(result, True)
        db.session.add.side_effect = Exception
        db.session.rollback.return_value = 1
        result = universities_crud.create_university(university1)
        self.assertEqual(result, False)

    @patch('service.universities_crud.db')
    @patch('service.universities_crud.get_university')
    def test_update_university(self, get_university, db) -> None:
        """
        Test for updating university with given id.
        :param get_university: Mock function get_university
        :param db: Mock class SQLAlchemy
        :return: None
        """
        # Test if everything is correct
        get_university.return_value = university1
        db.session.flush.return_value = 1
        db.session.commit.return_value = 1
        result = universities_crud.update_university(university2, 1)
        self.assertEqual(result, True)
        # Test if exception raised
        get_university.side_effect = Exception
        db.session.rollback.return_value = 1
        result = universities_crud.update_university(university2, 1)
        self.assertEqual(result, False)
        # Test if no new data was added
        result = universities_crud.update_university(university1, 1)
        self.assertEqual(result, False)

    @patch('service.universities_crud.db')
    @patch('service.universities_crud.University')
    def test_delete_university(self, university, db) -> None:
        """
        Test delete university with given id
        :param university: Mock class University
        :param db: Mock class SQLAlchemy
        :return: None
        """
        # Test if everything is okay
        university.query.filter.return_value.delete.return_value = 1
        db.session.commit.return_value = 1
        result = universities_crud.delete_university(1)
        self.assertEqual(result, True)
        # Test if exception raised
        db.session.rollback.return_value = 1
        university.query.filter.return_value.delete.side_effect = Exception
        result = universities_crud.delete_university(1)
        self.assertEqual(result, False)

    @patch('service.universities_crud.db')
    def test_create_university_api(self, db) -> None:
        """
        Test creat new university for REST-API.
        :param db: Mock class SQLAlchemy
        :return: None
        """
        # Test for correct data
        db.session.add.return_value = 1
        db.session.commit.return_value = 1
        result = universities_crud.create_university_api(university1.name, university1.location)
        self.assertEqual(university1.name, result.name)
        self.assertEqual(university1.location, result.location)
        # Test if exception raised
        db.session.add.side_effect = Exception
        db.session.rollback.return_value = 1
        result = universities_crud.create_university_api(university1.name, university1.location)
        true_value = {'error': {'message': 'Error of adding to db', 'status': 412}}
        self.assertEqual(true_value, result)
        # Test if name or location is None
        result = universities_crud.create_university_api(university1.name, None)
        true_value = {'error': {'message': 'Some data was not given', 'status': 400}}
        self.assertEqual(true_value, result)
        # Test if name or location incorrect type
        result = universities_crud.create_university_api(university1.name, 1)
        true_value = {'error': {'message': 'Incorrect data type', 'status': 400}}
        self.assertEqual(true_value, result)
        # Test if name or location contains wrong symbols
        result = universities_crud.create_university_api('1?#$%^&', '    ')
        true_value = {'error': {'message': 'Some fields contain not allowed symbols', 'status': 400}}
        self.assertEqual(true_value, result)

    @patch('service.universities_crud.db')
    @patch('service.universities_crud.University')
    def test_delete_university_api(self, university, db) -> None:
        """
        Test delete university with given id in REST-API.
        :param university: Mock class University
        :param db: Mock class SQLAlchemy
        :return: None
        """
        # Test if everything is correct
        university.query.filter.return_value.first.return_value = university1
        db.session.delete.return_value = 1
        db.session.commit.return_value = 1
        result = universities_crud.delete_university_api(1)
        self.assertEqual(university1, result)
        # Test if exception was raised
        university.query.filter.return_value.first.side_effect = Exception
        db.session.rollback.return_value = 1
        result = universities_crud.delete_university_api(1)
        true_result = {'error': {'message': 'Error of adding to db', 'status': 412}}
        self.assertEqual(true_result, result)
        # Test if university was not in database
        university.query.filter.return_value.first.side_effect = None
        university.query.filter.return_value.first.return_value = None
        db.session.delete.return_value = 1
        result = universities_crud.delete_university_api(-1)
        true_result = {'error': {'message': 'No university was found with given id.', 'status': 412}}
        self.assertEqual(true_result, result)

    @patch('service.universities_crud.db')
    @patch('service.universities_crud.get_university')
    def test_update_university_api(self, get_university, db) -> None:
        """
        Test update university for API.
        :param get_university: Mock function get_university
        :param db: Mock class SQLAlchemy
        :return: None
        """
        # Test if everything is okay
        university1 = University('Test1', 'Test1')
        get_university.return_value = university1
        db.session.flush.return_value = 1
        db.session.commit.return_value = 1
        result = universities_crud.update_university_api(1, university2.name, university2.location)
        self.assertEqual(university2.name, result.name)
        self.assertEqual(university2.location, result.location)
        # Test if exception raised
        get_university.side_effect = Exception
        db.session.rollback.return_value = 1
        result = universities_crud.update_university_api(1, university2.name, university2.location)
        true_result = {'error': {'message': 'Error to update university to db', 'status': 412}}
        self.assertEqual(true_result, result)
        # Test if name contains incorrect symbols
        get_university.side_effect = None
        get_university.return_value = university1
        result = universities_crud.update_university_api(-1, '@#$%^&', university2.location)
        true_result = {'error': {'message': 'Name contains wrong symbols', 'status': 400}}
        self.assertEqual(true_result, result)
        # Test if name not string
        get_university.return_value = university1
        result = universities_crud.update_university_api(-1, 1, university2.location)
        true_result = {'error': {'message': 'Name is an incorrect data type', 'status': 400}}
        self.assertEqual(true_result, result)
        # Test if location contains incorrect symbols
        get_university.side_effect = None
        get_university.return_value = university1
        result = universities_crud.update_university_api(-1, university1.name, ' ')
        true_result = {'error': {'message': 'Location contains wrong symbols', 'status': 400}}
        self.assertEqual(true_result, result)
        # Test if location not string
        get_university.return_value = university1
        result = universities_crud.update_university_api(-1, university1.name, 1)
        true_result = {'error': {'message': 'Location is an incorrect data type', 'status': 400}}
        self.assertEqual(true_result, result)
        # Test if no data was changes
        result = universities_crud.update_university_api(-1, university1.name, university1.location)
        true_result = {'error': {'message': 'No new data was given', 'status': 400}}
        self.assertEqual(true_result, result)
