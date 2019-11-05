import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobsauceapp.models import Job, Response, Company
from ..connection import Connection

def create_response_join_table(cursor, row):
    row = sqlite3.Row(cursor, row)

    company = Company()
    company.name = row[0]

    job = Job()
    job.title_of_position = row[1]

    response = Response()
    response.details = row[2]
    response.date = row[3]

    return (company, job, response)

def get_response(response_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_response_join_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.name, j.title_of_position, r.details, r.date
            from jobsauceapp_job j
            join jobsauceapp_company c on c.id = j.company_id
            join jobsauceapp_response r on j.id = r.job_id
        where response.id = ?
        """, (response_id,))

        return db_cursor.fetchone()

def create_job_table(cursor, row):
    row = sqlite3.Row(cursor, row)

    job = Job()
    job.id = row[0]
    job.title_of_position = row[1]
    job.date_of_submission = row[2]
    job.company_id = row[3]
    job.tech_list_id = row[4]
    job.user_id = row[5]

    return (job)
    
def get_jobs():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_job_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            id,
            title_of_position,
            date_of_submission,
            company_id,
            tech_list_id,
            user_id 
        from jobsauceapp_job
        """)

        return db_cursor.fetchall()

def response_form(request):

    if request.method == 'GET':
        jobs = get_jobs()
        template = 'response/form.html'
        context = {
            'all_jobs': jobs
        }

        return render(request, template, context)

def response_edit_form(request, response_id):

    if request.method == 'GET':
        response = get_response(response_id)
        jobs = get_jobs()

        template = 'response/form.html'
        context = {
            'response': response,
            'all_jobs': jobs
        }

        return render(request, template, context)