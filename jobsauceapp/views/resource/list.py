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
                c.name as company_name, r.id, r.link_to_resource, r.date_due, r.is_complete, tt.name as tech_name
                from jobsauceapp_resource r 
                join jobsauceapp_tech_type tt on tt.id = r.tech_type_id
                join jobsauceapp_company c on c.id = r.company_id
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
                resource.tech_name = row['tech_name']

                resources.append(resource)

        template = 'resource/list.html'
        context = {
            'all_resources': resources
        }

        return render(request, template, context)