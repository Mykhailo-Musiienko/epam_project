"""
This module run tests for function in module service.teachers_crude.

This module contains class TestTeacherCrud

This module imports: app,datetime,unittest.TestCase, unittest.mock.patch, Teacher, University, teacher_crude
"""

import datetime
from unittest import TestCase
from unittest.mock import patch
from app import app
from models.teacher import Teacher
from models.university import University
from service import teachers_crud

university1 = University('Test1', 'Test1')
university2 = University('Test2', 'Test2')
university3 = University('Test3', 'Test3')
app.testing = True
teacher1 = Teacher('Test1', 'Test1', datetime.date(2011, 11, 1), 1000, university1)
teacher2 = Teacher('Test2', 'Test2', datetime.date(2010, 8, 21), 800, university2)
teacher3 = Teacher('Test3', 'Test3', datetime.date(2011, 2, 17), 1500, university3)
teacher4 = Teacher('Test4', 'Test4', datetime.date(2011, 5, 5), 200, university1)
teacher_list = [teacher1, teacher2, teacher3, teacher4]


class TestTeacherCrud(TestCase):
    """
    This class runs all tests for the module service.teachers_crud.

    It includes: test test_get_all_teachers, test_get_teacher, test_create_teacher,
    test_update_teacher, test_delete_teacher, test_update_teacher_api,
    test_delete_teacher_api,test_teacher_str

    It inherited from class TestCase
    """

    @patch('service.teachers_crud.Teacher')
    def test_get_all_teachers(self, teacher) -> None:
        """
        Test to get all teachers on website.
        :param teacher: Mock teacher class
        :return: None
        """
        teacher.query.all.return_value = teacher_list
        result = teachers_crud.get_all_teachers()
        self.assertEqual(result, teacher_list)

    @patch('service.teachers_crud.Teacher')
    def test_get_teacher(self, teacher) -> None:
        """
        Test to get teacher by id on website.
        :param teacher: Mock teacher class
        :return: None
        """
        teacher.query.get.return_value = teacher1
        result = teachers_crud.get_teacher(-1)
        self.assertEqual(result, teacher1)

    @patch('service.teachers_crud.db.session')
    def test_create_teacher(self, session) -> None:
        """
        Test to create new teacher on website.
        :param session: Mock session class
        :return: None
        """
        session.add.return_value = 1
        result = teachers_crud.create_teacher(teacher1)
        self.assertEqual(result, True)
        session.add.side_effect = Exception
        result = teachers_crud.create_teacher(teacher1)
        self.assertEqual(result, False)

    @patch('service.teachers_crud.db.session')
    @patch('service.teachers_crud.get_teacher')
    def test_update_teacher(self, get_teacher, session) -> None:
        """
        Test to update teacher on website.
        :param get_teacher: Mock teacher class.
        :param session: Mock session class.
        :return: None
        """
        get_teacher.return_value = teacher1
        session.commit.return_value = 1
        result = teachers_crud.update_teacher(teacher2, 1)
        self.assertEqual(result, True)
        result = teachers_crud.update_teacher(teacher1, 1)
        self.assertEqual(result, False)

    @patch('service.teachers_crud.db.session')
    @patch('service.teachers_crud.Teacher')
    def test_delete_teacher(self, teacher, session) -> None:
        """
        Test to delete teacher from db on website.
        :param teacher: Mock teacher class
        :param session: Mock session class
        :return: None
        """
        teacher.query.filter.return_value.delete.return_value = True
        result = teachers_crud.delete_teacher(1000)
        self.assertEqual(result, True)
        teacher.query.filter.return_value.delete.side_effect = Exception
        session.rollback.return_value = 1
        result = teachers_crud.delete_teacher(1000)
        self.assertEqual(result, False)

    @patch('service.teachers_crud.get_teacher')
    @patch('service.teachers_crud.University')
    def test_update_teacher_api(self, university, get) -> None:
        """
        Test to update teacher on api.
        :param university: Mock university class
        :param get: Mock get_teacher() function
        :return: None
        """
        response1 = {'error': {'message': 'No data was given.', 'status': 400}}
        response2 = {'error': {'message': 'Wrong university name.', 'status': 400}}
        response3 = {'error': {'message': 'Salary is not integer', 'status': 400}}
        response4 = {'error': {'message': 'Incorrect date format.', 'status': 400}}
        result = teachers_crud.update_teacher_api(teacher_id=0, name=None, last_name=None, birth_date=None, salary=None,
                                                  university=None)
        self.assertEqual(result, response1)
        university.query.filter_by.return_value.first.return_value = None
        result = teachers_crud.update_teacher_api(teacher_id=0, name='Test', last_name=None, birth_date=None,
                                                  salary=None,
                                                  university=1)
        self.assertEqual(result, response2)
        result = teachers_crud.update_teacher_api(teacher_id=0, name='Test', last_name=None, birth_date=None,
                                                  salary='80a00',
                                                  university=None)
        self.assertEqual(result, response3)

        result = teachers_crud.update_teacher_api(teacher_id=0, name='Test', last_name=None,
                                                  birth_date=datetime.date(2011, 11, 1),
                                                  salary=None,
                                                  university=None)
        self.assertEqual(result, response4)
        university.query.filter_by.return_value.first.return_value = university2
        get.return_value = teacher1
        result = teachers_crud.update_teacher_api(teacher_id=0, name=teacher2.name, last_name=teacher2.last_name,
                                                  birth_date=str(teacher2.birth_date),
                                                  salary=teacher2.salary,
                                                  university="Test1")
        self.assertEqual(result.name, teacher2.name)
        self.assertEqual(result.last_name, teacher2.last_name)
        self.assertEqual(result.university, teacher2.university)

    @patch('service.teachers_crud.db')
    @patch('service.teachers_crud.Teacher')
    def test_delete_teacher_api(self, teacher, db) -> None:
        """
        Test to delete teacher in api
        :param teacher: Mock teacher class
        :param db: Mock db class
        :return: None
        """
        teacher.query.filter.return_value.first.return_value = teacher1
        teacher.query.filter.return_value.delete.return_value = True
        db.session.commit.return_value = 1
        result = teachers_crud.delete_teacher_api(1)
        self.assertEqual(result, teacher1)

        teacher.query.filter.return_value.delete.return_value = False
        result = teachers_crud.delete_teacher_api(1)
        true_result = {'error': {'message': 'No teacher was found with given id', 'status': 400}}
        self.assertEqual(result, true_result)

        teacher.query.filter.return_value.delete.side_effect = Exception
        db.session.rollback.return_value = 1
        result = teachers_crud.delete_teacher_api(1)
        true_result = {'error': {'message': 'Error deleting from db.', 'status': 400}}
        self.assertEqual(result, true_result)

    def test_teacher_str(self) -> None:
        """
        Test __str__() method
        :return: None
        """
        result = f"Name: {teacher1.name}, Last Name: {teacher1.last_name}" \
                 f",birth_date: {teacher1.birth_date},salary: {teacher1.salary}," \
                 f"university: {teacher1.university}"
        self.assertEqual(result, teacher1.__str__())
