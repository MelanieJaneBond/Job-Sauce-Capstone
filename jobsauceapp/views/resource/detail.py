import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobsauceapp.models import Job, Resource, Company, Tech_Type
from ..connection import Connection

def create_resource_table(cursor, row):
    row = sqlite3.Row(cursor, row)

    resource = Resource()
    resource.id = row[0]
    resource.link_to_resource = row[1]
    resource.date_due = row[2]
    resource.is_complete = row[3]
    resource.tech_type_id = row[4]
    resource.user_id = row[5]

    return (resource)

def create_resource_join_table(cursor, row):
    row = sqlite3.Row(cursor, row)

    resource = Resource()
    resource.link_to_resource = row[0]
    resource.date_due = row[1]
    resource.is_complete = row[2]

    tech_type = Tech_Type()
    tech_type.tech_type_id = row[3]
    tech_type.name = row[4]

    return (resource, tech_type)

def get_resource(resource_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_resource_join_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
        r.link_to_resource,
        r.date_due,
        r.is_complete,
        tt.id as tech_type_id,
        tt.name
        from jobsauceapp_resource r 
        join jobsauceapp_tech_type tt on tt.id = r.tech_type_id
        order by date_due;
        """, (resource_id,))

        return db_cursor.fetchone()

def get_resources():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_resource_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            id,
            link_to_resource,
            date_due,
            is_complete,
            tech_type_id,
            user_id
        from jobsauceapp_resource
        """)

        return db_cursor.fetchall()

def resource_details(request, resource_id):
    if request.method == 'GET':

        resource = get_resource(resource_id)
        template = 'resource/list.html'
        context = {
            'all_resources': resource
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM jobsauceapp_resource
                    WHERE id = ?
                """, (resource_id,))

            return redirect(reverse('jobsauceapp:resources'))
        else:
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                INSERT INTO jobsauceapp_resource
                (link_to_resource, date_due, is_complete, tech_type_id, user_id)
                values (?, ?, ?, ?, ?)
                """,
                (form_data['link_to_resource'], form_data['date_due'], form_data['is_complete'],
                    form_data['tech_type_id'], request.user.id))
                
                return redirect(reverse('jobsauceapp:resources'))
