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

def get_tech(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_tech_table
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            tt.id as tech_type_id,
            tt.name
        from jobsauceapp_tech_type tt
            join jobsauceapp_job_tech jt on jt.tech_type_id = tt.id
            join jobsauceapp_job j on j.id = jt.job_id
        where j.user_id = ?
        """, (request.user.id,))



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

    return resource

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
        where id = ?
        """, (resource_id,))

        return db_cursor.fetchone()

def resource_form(request):

    if request.method == 'GET':
        tech_types = get_tech(request)
        template = 'resource/form.html'
        context = {
            'all_tech_types': tech_types
        }

        return render(request, template, context)

def resource_edit_form(request, resource_id):

    if request.method == 'GET':
        resource = get_resource(resource_id)

        template = 'resource/edit.html'
        context = {
            'resource': resource
        }
    
        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                # resource_id = get_resource(resource_id)

                db_cursor.execute("""
                UPDATE jobsauceapp_resource
                SET link_to_resource = ?,
                    date_due = ?,
                    is_complete = ?,
                    tech_type_id = ?,
                    user_id = ?
                WHERE id = ?
                """,
                (form_data["link_to_resource"], form_data['date_due'],
                    form_data['is_complete'], form_data['tech_type_id'], request.user.id, resource_id))
                
            return redirect(reverse('jobsauceapp:resources'))