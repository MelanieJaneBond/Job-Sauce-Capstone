import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from jobsauceapp.models import Job, Company, Response
from ..connection import Connection

def response_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                c.name, j.title_of_position, r.details, r.date
                from jobsauceapp_job j 
                join jobsauceapp_company c on c.job_id = j.id
                join jobsauceapp_response r on j.id = r.job_id
                order by r.date
            """)

            responses = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                response = Response()
                response.name = row['name']
                response.title_of_position = row['title_of_position']
                response.details = row['details']
                response.date = row['date']

                responses.append(response)

        template = 'response/list.html'
        context = {
            'all_responses': responses
        }
        return render(request, template, context)

    # elif request.method == 'POST':
    #     form_data = request.POST

    #     with sqlite3.connect(Connection.db_path) as conn:
    #         db_cursor = conn.cursor()

    #         db_cursor.execute("""
    #         INSERT INTO libraryapp_book
    #         (title, author, isbn, year_published, location_id, librarian_id)
    #         values (?, ?, ?, ?, ?, ?)
    #         """,
    #         (form_data['title'], form_data['author'],
    #             form_data['isbn'], form_data['year_published'],
    #             request.user.librarian.id, form_data["location"]))

    #     return redirect(reverse('libraryapp:books'))