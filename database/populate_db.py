import datetime

from app import db
from models.teacher import Teacher
from models.university import University

university1 = University('NURE', 'Nauchna 14')
university2 = University('KPI', 'Kirpichova 17')
university3 = University('Karazina', 'Independence Avenue 6')
university4 = University('KNMU', 'Nauchna 4')
university5 = University('KHAI', 'Chkalova 17')

teacher1 = Teacher('Andriy', 'Kovalenko', datetime.date(1987, 10, 12), 1500, university1)
teacher2 = Teacher('Irina', 'Perova', datetime.date(1999, 5, 3), 1000, university3)
teacher3 = Teacher('Vitaliy', 'Puchkov', datetime.date(1967, 9, 21), 1800, university2)
teacher4 = Teacher('Oleg', 'Strochak', datetime.date(1990, 4, 4), 1300, university2)
teacher5 = Teacher('Genadiy', 'Gorin', datetime.date(1997, 8, 6), 900, university1)
teacher6 = Teacher('Alexander', 'Hryapkin', datetime.date(1970, 6, 25), 1900, university3)
teacher7 = Teacher('Andriy', 'Kovalenko', datetime.date(1987, 10, 12), 1500, university4)
teacher8 = Teacher('Sergey', 'Chaynikov', datetime.date(1969, 2, 21), 2000, university3)
teacher9 = Teacher('Svitlana', 'Ponomarova', datetime.date(1999, 9, 5), 700, university5)
teacher10 = Teacher('Anton', 'Ostapenko', datetime.date(1985, 12, 12), 2200, university5)

def populate_database():
    db.session.add_all([university1, university2, university3, university4, university5])
    db.session.commit()
    db.session.add_all([teacher1, teacher2, teacher3, teacher4,
                        teacher5, teacher6, teacher7, teacher8, teacher9, teacher10])
    db.session.commit()
