import sqlite3
from django.shortcuts import render
from jobsauceapp.models import Job
from jobsauceapp.models import Company
from jobsauceapp.models import Tech_Type
from jobsauceapp.models import Job_Tech
from ..connection import Connection


def job_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                c.name as company_name, j.title_of_position, tt.name, j.date_of_submission, r.is_rejected
                from jobsauceapp_job j 
                left join jobsauceapp_company c on j.company_id = c.id
                left join jobsauceapp_response r on r.job_id = j.id
                left join jobsauceapp_job_tech jt on j.id = jt.job_id
                inner join jobsauceapp_tech_type tt on jt.tech_type_id = tt.id
            """)

            all_jobs = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                job = Job()
                job.company_name = row['company_name']
                job.title_of_position = row['title_of_position']
                job.name = row['name']
                job.date_of_submission = row['date_of_submission']
                job.is_rejected = row['is_rejected']

                all_jobs.append(job)

        template = 'job/list.html'
        context = {
            'all_jobs': all_jobs
        }

        return render(request, template, context)