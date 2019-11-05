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
                left join jobsauceapp_tech_type tt on jt.tech_type_id = tt.id
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
        last_id = None
    #form_data.getlist("technologies_list")
    #make a for loop that will "for each technology in technology_list" insert into the tech_types table!
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            nothing = None

            db_cursor.execute("""
            INSERT INTO jobsauceapp_company
            (name)
            VALUES (?)
            """,
            (form_data['company_name'],))

            db_cursor.execute("""
            select last_insert_rowid()
            """)

            last_id = db_cursor.fetchone()
        

    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO jobsauceapp_job
        (title_of_position, date_of_submission, company_id, tech_list_id, user_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (form_data['title_of_position'], form_data['date_of_submission'],
            last_id[0], None, request.user.id))

        db_cursor.execute("""
            select last_insert_rowid()
            """)

        last_job_id = db_cursor.fetchone()

    techlist = form_data.getlist('technologies_list')
    for technology in techlist:
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            nothing = None

            db_cursor.execute("""
            INSERT INTO jobsauceapp_job_tech
            (tech_type_id, job_id)
            VALUES (?, ?)
            """,
            (technology, last_job_id[0]))

    return redirect(reverse('jobsauceapp:jobs'))