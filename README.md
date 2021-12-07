[![Coverage Status](https://coveralls.io/repos/github/Mykhailo-Musiienko/epam_project/badge.svg?branch=master)](https://coveralls.io/github/Mykhailo-Musiienko/epam_project?branch=master)

# Managing teachers and universities

---

This project was created to perform management of teachers and universities
using web page application or with a help of REST-API. It reads and writes data
to MySQL database.
With this application you can:

* interact with database
* create, update and delete teachers and universities
* search teachers between two dates
* count average salary among all teachers in every university
* make REST-API requests
* logging every step for checking errors

---

Main libraries used:

1. Flask-SQLAlchem - to add support for SQLAlchemy ORM
2. Flask-Marshmallow - to serialize nad deserialize classes
3. Flask-Migrate - for handling database migrations

## Main use

To see what you can do with web application you can see documentation 
[SRS.md](https://github.com/Mykhailo-Musiienko/epam_project/blob/master/documentation/SRS.md)

---

# Requirements

---

This project requires moduls as: flask, sqlalchemy, marshmallow and others.
All modules are in **requirements.txt** , so to download everything
you can type:

```commandline
pip install -r requirements.txt
```

## Requirements for Database

Default user name, password and database name are in file
[.env](https://github.com/Mykhailo-Musiienko/epam_project/blob/master/.env)

If you have different username or password in your database you can just redo this file
and write your values instead of given. For example ***USER='root'*** change to ***USER='kali'***
and so on.

# Instalation

---

### To install current project you can click on button "Code" and download it with

```commandline
git clone git@github.com:Mykhailo-Musiienko/epam_project.git
```

or you can download zip archive instead.

To run this application you should go to the directory of this project 
with command **cd** and run appication using **gunicorn** that was in
requirements.txt

```commandline
cd epam_project     
gunicorn -c gunicorn.py.ini app:app
```

If it doesn't work for you can run application with:

```commandline
flask run
```
or:
```commandline
python run.py
```

Don't forget to install requirements.txt first.

# How to make REST-API requests

---

### To start making REST-API request your link should contain **/api/** .
Here are all api links with their allowed methods:

* http://0.0.0.0:5000/api/ request method GET
    * Returns all teachers in database.
* http://0.0.0.0:5000/api/ request method POST
  * You can make POST request to create new teacher.
* http://0.0.0.0:5000/api/id request method DELETE
  * You can delete teacher with given **id** 
* http://0.0.0.0:5000/api/id request method GET
  * Returns teacher with writen **id**.
* http://0.0.0.0:5000/api/teacher_update/id request method PATCH
  * You can update teacher with given **id**.
* http://0.0.0.0:5000/api/search_by_date request with method POST
  *You can search teachers how are between two dates
* http://0.0.0.0:5000/api/university request method GET
  * Returns all universities in database
* http://0.0.0.0:5000/api/university request method POST
  * You can create new university
* http://0.0.0.0:5000/api/university/id request method PATCH
  * You can update university with given **id**
* http://0.0.0.0:5000/api/university/id request method DELETE
  * You can delete university with given **id**
* http://0.0.0.0:5000/api/university/id request method GET
  * Returns university with given **id**

### To make POST and PATCH requests for teacher you need to make this json object:

```commandline
{
    "last_name": "name", 
    "name": "last name", 
    "birth_date": "year-month-day", 
    "salary": 1000, 
    "university": "University name"
}
```

You can write PATCH request without some keys, for example you can update only name
if you write

```commandline
{ 
    "name": "last name"
}
```

### To make POST and PATCH requests for university you need to make this json object:

```commandline
{
    "location": "location", 
    "name": "university name"
}
```

You can make PATCH request the same way as where update teacher, so you don't need
to enter every key value.

### To search teacher between two dates you need to make json object as folow:

```commandline
{
    "date_from":"year-month-day",
    "date_to":"year-month-day"
}
```

If you enter the same dates it will search not in interval but in this date.

# Run tests

To run tests to see if everything works correct you can write in terminal:

```commandline
python -m unittest discover
```

It will find all files starting with the word 'test'. It won't change your database
because it uses mock functions to prevent changing database.