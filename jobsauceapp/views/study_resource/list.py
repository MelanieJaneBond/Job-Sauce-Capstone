import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from jobsauceapp.models import Company, Tech_Type, Study_Resource
from ..connection import Connection

def create_listing(cursor, row):
    row = sqlite3.Row(cursor, row)

    company = Company()
    company.company_name = row[0]

    study_re = Study_Resource()
    study_re.link_to_resource = row[1]
    study_re.date_due = row[2]
    study_re.is_complete = row[3]

    tech_type = Tech_Type()
    tech_type.tech_name = row[4]

    return (company, study_re, tech_type)

def study_resource_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_listing
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                c.name as company_name, sr.link_to_resource, sr.date_due, sr.is_complete, tt.name as tech_name
                from jobsauceapp_study_resource sr 
                join jobsauceapp_tech_type tt on tt.id = sr.tech_type_id
                join jobsauceapp_company c on c.id = sr.company_id
                order by date_due
            """)

            resources = db_cursor.fetchall()

        template = 'study_resource/list.html'
        context = {
            'all_resources': resources
        }

        return render(request, template, context)