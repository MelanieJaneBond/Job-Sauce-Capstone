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

def get_jobs(user_id):
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
        where j.user_id = ?
        """, (user_id,))

        return db_cursor.all()

def create_company_table(cursor, row):
    row = sqlite3.Row(cursor, row)

    companies = Company()
    


def job_form_start(request):

    if request.method == 'GET':
        companies = get_companies()
        template = 'job/form.html'
        context = {
            'all_companies': companies
        }

        return render(request, template, context)


@login_required
def book_edit_form(request, book_id):

    if request.method == 'GET':
        book = get_book(book_id)
        libraries = get_libraries()

        template = 'books/form.html'
        context = {
            'book': book,
            'all_libraries': libraries
        }

        return render(request, template, context)