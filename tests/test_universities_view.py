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
from models.teacher import Teacher

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


class TestUniversitiesView(TestCase):
    """

    """
    pass