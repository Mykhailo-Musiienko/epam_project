"""
Module is made for handling models for website

Module contains modules: teacher, university.

This module import app, Teacher and University to get rid of circular imports
"""
from app import db, ma
from models.teacher import Teacher
from models.university import University
