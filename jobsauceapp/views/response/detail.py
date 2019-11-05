import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobsauceapp.models import Job, Response, Company
from ..connection import Connection

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

def get_response_join(response_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_response_join_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.name, j.title_of_position, r.details, r.date
            from jobsauceapp_job j 
            join jobsauceapp_company c on c.job_id = j.id
            join jobsauceapp_response r on j.id = r.job_id
        """, (response_id,))

        return db_cursor.fetchone()

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

def create_response(cursor, row):
    row = sqlite3.Row(cursor, row)

    response = Response()
    response.id = row[0]
    response.details = row[1]
    response.is_rejected = row[2]
    response.date = row[3]
    response.job_id = row[4]
    response.user_id = row[5]

    return response

def get_response(response_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_response
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                r.id,
                r.details,
                r.is_rejected,
                r.date,
                r.job_id,
                r.user_id
            FROM jobsauceapp_response r
            WHERE r.id = ?
            """, (response_id,)
        )

        return db_cursor.fetchone()

def response_details_form(request, response_id):
    if request.method == 'GET':

        # response = get_response_join(response_id)
        jobs = get_jobs()
        one_response = get_response(response_id)
        template = 'response/form.html'
        context = {
            'all_jobs': jobs,
            'one_response': one_response
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM jobsauceapp_response
                    WHERE id = ?
                """, (response_id,))

            return redirect(reverse('jobsauceapp:responses'))
        else:
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE jobsauceapp_response
                SET details = ?,
                    is_rejected = ?,
                    date = ?,
                    job_id = ?,
                    user_id = ?
                WHERE id = ?
                """,
                (form_data['is_rejected'], form_data['date'],
                    form_data['job_id'], request.user.id, form_data["details"]))
                
                return redirect(reverse('jobsauceapp:responses'))