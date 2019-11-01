import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from jobsauceapp.models import Job, Company, Tech_Type, Job_Tech, Resource
from ..connection import Connection

def create_tech_table(cursor, row):
    row = sqlite3.Row(cursor, row)

    tech_type = Tech_Type()
    tech_type.tech_type_id = row[0]
    tech_type.name = row[1]

    return (tech_type)

def get_tech():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_tech_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            id as tech_type_id,
            name
        from jobsauceapp_tech_type
        """)

        return db_cursor.fetchall()

def create_resource(cursor, row):
    row = sqlite3.Row(cursor, row)

    resource = Resource()
    resource.id = row[0]
    resource.link_to_resource = row[1]
    resource.date_due = row[2]
    resource.is_complete = row[3]
    resource.tech_type_id = row[4]
    resource.user_id = row[5]

    return (resource)

def get_resource(resource_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_resource
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
        """, (resource_id,))

        return db_cursor.fetchone()

def resource_form(request):

    if request.method == 'GET':
        tech_types = get_tech()
        template = 'resource/form.html'
        context = {
            'all_tech_types': tech_types
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