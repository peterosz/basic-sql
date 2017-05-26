import os
import psycopg2
from flask import Flask, render_template


def connect_to_database(func_to_be_connected):
    def connection(*args, **kwargs):
        global _cursor
        _db_connection = None
        _cursor = None
        connection_data = {
            'dbname': os.environ.get('MY_PSQL_DBNAME'),
            'user': os.environ.get('MY_PSQL_USER'),
            'host': os.environ.get('MY_PSQL_HOST'),
            'password': os.environ.get('MY_PSQL_PASSWORD')
        }
        connect_string = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        connect_string = connect_string.format(**connection_data)
        _db_connection = psycopg2.connect(connect_string)
        _db_connection.autocommit = True
        _cursor = _db_connection.cursor()
        result = func_to_be_connected(*args, **kwargs)
        _cursor.close()
        _db_connection.close()
        return result
    return connection


@connect_to_database
def mentors():
    query = ('''SELECT mentors.first_name, mentors.last_name, schools.name, schools.country
                FROM mentors
                INNER JOIN schools ON mentors.city = schools.city
                ORDER BY mentors.id asc''')
    _cursor.execute(query)
    table = _cursor.fetchall()
    return render_template('layout.html', table=table)


@connect_to_database
def all_school():
    query = ('''SELECT mentors.first_name, mentors.last_name, schools.name, schools.country
                FROM mentors
                RIGHT JOIN schools ON mentors.city = schools.city
                ORDER BY mentors.id''')
    _cursor.execute(query)
    table = _cursor.fetchall()
    return render_template('layout.html', table=table)


@connect_to_database
def mentors_by_country():
    query = ('''SELECT schools.country, COUNT(mentors.id)
                FROM schools
                INNER JOIN mentors ON schools.city = mentors.city
                GROUP BY schools.country
                ORDER BY schools.country desc;''')
    _cursor.execute(query)
    table = _cursor.fetchall()
    return render_template('layout.html', table=table)


@connect_to_database
def contacts():
    query = ('''SELECT schools.name, CONCAT(mentors.first_name, ' ', mentors.last_name)
                FROM schools
                INNER JOIN mentors ON mentors.id = schools.contact_person
                GROUP BY schools.name, mentors.first_name, mentors.last_name
                ORDER BY schools.name desc;''')
    _cursor.execute(query)
    table = _cursor.fetchall()
    return render_template('layout.html', table=table)


@connect_to_database
def applicants():
    query = ('''SELECT first_name, application_code, creation_date
                FROM applicants
                LEFT JOIN applicants_mentors ON id = applicant_id
                WHERE creation_date > '2016-01-01'
                ORDER BY applicants_mentors.creation_date desc''')
    _cursor.execute(query)
    table = _cursor.fetchall()
    return render_template('layout.html', table=table)


@connect_to_database
def applicants_and_mentors():
    query = ('''SELECT applicants.first_name, applicants.application_code, mentor_first_name, mentor_last_name
                FROM applicants
                INNER JOIN applicants_mentors on id = applicant_id
                ''')
