import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobsauceapp.models import Job, Job_Tech, Company, Tech_Type
from ..connection import Connection

def create_technology_table(cursor, row):
    row = sqlite3.Row(cursor, row)

    technology = Tech_Type()
    technology.id = row[0]
    technology.name = row[1]

    return (technology)

def get_technologies():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_technology_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            id,
            name 
        from jobsauceapp_tech_type
        """)

        return db_cursor.fetchall()

def job_form(request):

    if request.method == 'GET':
        technologies = get_technologies()

        template = 'job/form.html'
        context = {
            'all_technologies': technologies
        }

        return render(request, template, context)