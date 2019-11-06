import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from jobsauceapp.models import Company, Tech_Type, Resource
from ..connection import Connection

def resource_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                r.id,
                r.link_to_resource,
                r.date_due,
                r.is_complete,
                tt.id as tech_type_id,
                tt.name as tech_name
                from jobsauceapp_resource r 
                join jobsauceapp_tech_type tt on tt.id = r.tech_type_id
                order by date_due
            """)

            resources = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                resource = Resource()
                resource.id = row['id']
                resource.link_to_resource = row['link_to_resource']
                resource.date_due = row['date_due']
                resource.is_complete = row['is_complete']
                resource.tech_type_id = row['tech_type_id']
                resource.tech_name = row['tech_name']

                resources.append(resource)

        template = 'resource/list.html'
        context = {
            'all_resources': resources
        }

        return render(request, template, context)
        
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO jobsauceapp_resource
            (link_to_resource, date_due, is_complete, tech_type_id, user_id)
            values (?, ?, ?, ?, ?)
            """,
            (form_data['link_to_resource'], form_data['date_due'],
                form_data['is_complete'], form_data['tech_type_id'], request.user.id))

        return redirect(reverse('jobsauceapp:resources'))
