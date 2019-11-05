import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobsauceapp.models import Job, Company, Job_Tech, Tech_Type
from ..connection import Connection

# def get_job_joined(job_id):
#     with sqlite3.connect(Connection.db_path) as conn:
#         conn.row_factory = create_job_joined
#         db_cursor = conn.cursor()

#         db_cursor.execute("""
#         select
#             j.id,
#             j.title_of_position,
#             j.date_of_submission,
#             j.company_id,
#             j.tech_list_id,
#             j.user_id
#         from jobsauceapp_job j
#         left join jobsauceapp_company c
#         on j.company_id = c.id
#         where j.id = ?
#         """, (job_id,)
#         )

#         return db_cursor.fetchone()

# def create_job_joined(cursor, row):
#     row = sqlite3.Row(cursor, row)

#     job = Job()
#     job.id = row[0]
#     job.title_of_position = row[1]
#     job.date_of_submission = row[2]
#     job.company_id = row[3]
#     job.tech_list_id = row[4]
#     job.user_id = row[5]

#     company = Company()
#     company.id = row[6]
#     company.name = row[7]

#     return (company, job,)
#get one of job, company, and job_techs
#you will be PUTTING for EACH ID so, you need a details.py
# to organize the functionality of your code
def create_company(cursor, row):
    row = sqlite3.Row(cursor, row)

    company = Company()
    company.id = row[0]
    company.name = row[1]

    return (company,)

def create_job(cursor, row):
    row = sqlite3.Row(cursor, row)

    job = Job()
    job.id = row[0]
    job.title_of_position = row[1]
    job.date_of_submission = row[2]
    job.company_id = row[3]
    job.tech_list_id = row[4]
    job.user_id = row[5]

    return job

def create_job_tech(cursor, row):

    job_tech = Job_Tech()
    job_tech.id = row[0]
    job_tech.tech_type_id = row[1]
    job_tech.job_id = row[2]

    return (job_tech,)

def get_company(company_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_company
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                c.id,
                c.name
            FROM jobsauceapp_company c
            WHERE c.id = ?
            """, (company_id,)
        )

        return db_cursor.fetchone()

def get_job(job_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_job
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                j.id,
                j.title_of_position,
                j.date_of_submission,
                j.company_id,
                j.tech_list_id,
                j.user_id
            FROM jobsauceapp_job j
            WHERE j.id = ?
            """, (job_id,)
        )

        return db_cursor.fetchone()

def get_job_tech(job_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_job_tech
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                jt.id,
                jt.tech_type_id,
                jt.job_id
            FROM jobsauceapp_job_tech jt
            WHERE jt.job_id = ?
            """, (job_id,)
        )

        return db_cursor.fetchone()

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

# @login_required
def job_details_form(request, job_id):
    if request.method == 'GET':

        # company = get_company(company_id)
        job = get_job(job_id)
        job_tech = get_job_tech(job_id)
        technologies = get_technologies()
        template = 'job/form.html'
        context = {
            # 'company': company,
            'all_technologies': technologies,
            'job': job,
            'job_tech': job_tech
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing instead of creating
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE jobsauceapp_company
                SET name = ?,
                WHERE id = ?
                """,
                (form_data['company_name'], form_data['company_id'],))

            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE jobsauceapp_job
                SET title_of_position = ?,
                    date_of_submission = ?,
                    company_id = ?,
                    tech_list_id = ?,
                    user_id = ?,
                WHERE id = ?
                """,
                (form_data['title_of_position'], form_data['date_of_submission'],
                    company_id, None, request.user.id))
    
    #delete all the techs they created before, when they choose to edit the techs, all will go away and
    # a new list of techs will be created when they hit submit on the edit form.
    #I will need to fetch the ID of the job they are editing... or the ID of the job they just edited ?
    # using that id, I will write a SQL delete and then an INSERT INTO for the job_tech table

            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                nothing = None

                db_cursor.execute("""
                UPDATE jobsauceapp_job_tech
                SET tech_type_id = ?
                WHERE job_id = ?
                """,
                (form_data['technologies_list'], job_id,))
            
            
            return redirect(reverse('jobsauceapp:jobs'))

        # Check if this POST is for deleting instead of creating
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

            return redirect(reverse('libraryapp:libraries'))