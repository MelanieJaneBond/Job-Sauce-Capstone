import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from jobsauceapp.models import Job, Company, Tech_Type, Job_Tech
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

def job_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_job_listing
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                c.name as company_name, 
                j.title_of_position, 
                tt.name, 
                j.date_of_submission
                from jobsauceapp_job j 
                left join jobsauceapp_company c on j.company_id = c.id
                left join jobsauceapp_response r on r.job_id = j.id
                left join jobsauceapp_job_tech jt on j.id = jt.job_id
                inner join jobsauceapp_tech_type tt on jt.tech_type_id = tt.id
            """)

            jobs = db_cursor.fetchall()
            job_technologies = {}

            for (job, tech_type) in jobs:
                if job.title_of_position not in job_technologies:
                    job_technologies[job.title_of_position] = job
                    job_technologies[job.title_of_position].tech_types.append(tech_type)
                else:
                    job_technologies[job.title_of_position].tech_types.append(tech_type)

        template = 'job/list.html'
        context = {
            'all_jobs': job_technologies.values()
        }

        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST
        
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO jobsauceapp_company
            (name)
            VALUES (?)
            """,
            (form_data['company_name']))
        # return redirect(reverse('jobsauceapp:jobs'))

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO jobsauceapp_tech_type
            (name)
            VALUES (?)
            """,
            (form_data['tech_names']))
        # return redirect(reverse('jobsauceapp:jobs'))

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO jobsauceapp_job
            (title_of_position, date_of_submission, company_id, tech_list_id, user_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['title_of_position'], form_data['date_of_submission'],
                form_data['company_id'], form_data['tech_list_id'], request.user.id))

        return redirect(reverse('jobsauceapp:jobs'))

        # I need to recreate the form I had before... it was almost right...
        # So, I learned the "form_data" parts in this file refer to the IDs on html inputs
        # I don't yet understand what the "value" on html inputs refer to but
        # it'll be fine. Don't forget about the fields that won't be filled out by the form
        # in all the tables (especially job table) that may need HIDDEN default fillers or... 
        # they'll need something I haven't thought of yet that utilizes what was created in the form.