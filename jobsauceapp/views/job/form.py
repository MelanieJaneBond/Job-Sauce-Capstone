import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobsauceapp.models import Job, Job_Tech, Company, Tech_Type
from ..connection import Connection

def create_job_listing(cursor, row):
    row = sqlite3.Row(cursor, row)

    job = Job()
    job.company_name = row[0]
    job.title_of_position = row[1]
    job.date_of_submission = row[3]
    job.tech_types = []

    tech_type = Tech_Type()
    tech_type.name = row[2]

    return (job, tech_type,)

def get_jobs():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_job_listing
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.name as company_name,
            j.title_of_position,
            tt.name as name_of_tech,
            j.date_of_submission,
            r.is_rejected
        from jobsauceapp_job j 
        left join jobsauceapp_company c on j.company_id = c.id
        left join jobsauceapp_response r on r.job_id = j.id
        left join jobsauceapp_job_tech jt on j.id = jt.job_id
        inner join jobsauceapp_tech_type tt on jt.tech_type_id = tt.id
        """)

        return db_cursor.fetchall()

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
        # jobs = get_jobs()
        # job_technologies = {}
        # for (job, tech_type) in jobs:
        #     if job.title_of_position not in job_technologies:
        #         job_technologies[job.title_of_position] = job
        #         job_technologies[job.title_of_position].tech_types.append(tech_type)
        #     else:
        #         job_technologies[job.title_of_position].tech_types.append(tech_type)

        template = 'job/form.html'
        context = {
            # 'all_jobs': job_technologies.values()
            'all_technologies': technologies
        }

        return render(request, template, context)

# @login_required
# def book_edit_form(request, book_id):

#     if request.method == 'GET':
#         book = get_book(book_id)
#         libraries = get_libraries()

#         template = 'books/form.html'
#         context = {
#             'book': book,
#             'all_libraries': libraries
#         }

#         return render(request, template, context)