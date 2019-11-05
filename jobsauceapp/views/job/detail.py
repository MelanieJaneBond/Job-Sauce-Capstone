import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobsauceapp.models import Job, Response, Company
from ..connection import Connection



def get_job(job_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Library)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                l.id,
                l.title,
                l.address
            FROM libraryapp_library l
            WHERE l.id = ?
            """, (library_id,)
        )

        return db_cursor.fetchone()

def get_libraries():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Library)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            l.id,
            l.title,
            l.address
        from libraryapp_library l
        """)

        return db_cursor.fetchall()


@login_required
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

            return redirect(reverse('libraryapp:libraries'))