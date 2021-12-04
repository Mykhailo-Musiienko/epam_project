"""
Module is made for rendering templates to the webpage.

Module contains: teacher_view and university_view

Module import: app,flask.render_template, flask.request, flask.redirect, flask.url_for, flask.flash, teacher_view and
university_view
"""
from app import db, app
from flask import render_template,request,redirect,url_for,flash
from views import teacher_view
from views import universities_view
