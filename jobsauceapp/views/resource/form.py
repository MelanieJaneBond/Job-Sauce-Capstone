import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from jobsauceapp.models import Job, Company, Tech_Type, Job_Tech, Resource
from ..connection import Connection

def create_job_listing(cursor, row):
    row = sqlite3.Row(cursor, row)

    job = Job()
    job.company_name = row[0]
    job.title_of_position = row[1]
    job.job_id = row[2]
    job.tech_types = []

    tech_type = Tech_Type()
    tech_type.name = row[3]
    tech_type.tech_type_id = row[4]

    return (job, tech_type)

def job_list():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_job_listing
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.name as company_name,
            j.title_of_position,
            j.id as job_id,
            tt.name,
            tt.id as tech_type_id
        from jobsauceapp_job j 
        left join jobsauceapp_company c on j.company_id = c.id
        left join jobsauceapp_resource r on r.company_id = c.id
        left join jobsauceapp_job_tech jt on j.id = jt.job_id
        inner join jobsauceapp_tech_type tt on jt.tech_type_id = tt.id
        """)

        return db_cursor.fetchall()

def create_resource(cursor, row):
    row = sqlite3.Row(cursor, row)
        resource = Resource()
        resource.id = row[0]
        resource.link_to_resource = row[1]
        resource.date_due = row[2]
        resource.is_complete = row[3]
        resource.company_id = row[4]
        resource.tech_type_id = row[5]
        resource.user_id = row[6]

        return (resource)

def get_resource(resource_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_resource
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            id, link_to_resource, date_due, is_complete, company_id, tech_type_id, user_id
            from jobsauceapp_resource
        """, (resource_id,))

        return db_cursor.fetchone()

def resource_form(request):

    if request.method == 'GET':
        jobs = job_list()
        job_technologies = {}
        for (job, tech_type) in jobs:
            if job.title_of_position not in job_technologies:
                job_technologies[job.title_of_position] = job
                job_technologies[job.title_of_position].tech_types.append(tech_type)
            else:
                job_technologies[job.title_of_position].tech_types.append(tech_type)
        template = 'resource/form.html'
        context = {
            'all_jobs': job_technologies.values()
        }

        return render(request, template, context)

# def resource_edit_form(request, resource_id):

#     if request.method == 'GET':
#         resource = get_resource(resource_id)
#         jobs = get_jobs()

#         template = 'resource/form.html'
#         context = {
#             'resource': resource,
#             'all_jobs': jobs
#         }

#         return render(request, template, context)