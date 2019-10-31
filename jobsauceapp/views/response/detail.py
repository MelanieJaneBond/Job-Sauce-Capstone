import sqlite3
from django.shortcuts import render
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

def get_response(response_id):
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
def library_details(request, library_id):
    if request.method == 'GET':

        library = get_library(library_id)
        template = 'libraries/detail.html'
        context = {
            'library': library
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a library
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    UPDATE libraryapp_library
                    SET title = ?,
                        address = ?
                    WHERE id = ?
                    """,
                    (
                        form_data['title'],
                        form_data['address'],
                        library_id,
                    )
                )

            return redirect(reverse('libraryapp:libraries'))

        # Check if this POST is for deleting a library
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM libraryapp_library
                    WHERE id = ?
                """, (library_id,))

            return redirect(reverse('jobsauceapp:responses'))

                elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO jobsauceapp_response
            (is_rejected, date, job_id, user_id, details)
            values (?, ?, ?, ?, ?)
            """,
            (form_data['is_rejected'], form_data['date'],
                form_data['job_id'], request.user.id, form_data["details"]))

        return redirect(reverse('jobsauceapp:responses'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM jobsauceapp_response
                    WHERE id = ?
                """, (id,))

            return redirect(reverse('jobsauceapp:responses'))