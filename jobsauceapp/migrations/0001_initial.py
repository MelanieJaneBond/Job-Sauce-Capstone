# Generated by Django 2.2.6 on 2019-10-31 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_of_position', models.CharField(blank=True, max_length=100)),
                ('date_of_submission', models.DateField(auto_now_add=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Co', to='jobsauceapp.Company')),
            ],
            options={
                'verbose_name': 'job',
                'verbose_name_plural': 'jobs',
            },
        ),
        migrations.CreateModel(
            name='Tech_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=25)),
            ],
            options={
                'verbose_name': 'tech_type',
                'verbose_name_plural': 'tech_types',
            },
        ),
        migrations.CreateModel(
            name='Social_Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('title_of_position', models.CharField(blank=True, max_length=100)),
                ('date_of_last_encounter', models.DateField(auto_now_add=True)),
                ('linked_in_profile', models.URLField(blank=True, max_length=250)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsauceapp.Company')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'social_connection',
                'verbose_name_plural': 'social_connections',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(blank=True, max_length=400, null=True)),
                ('is_rejected', models.BooleanField(blank=True, default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsauceapp.Job')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'response',
                'verbose_name_plural': 'responses',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_to_resource', models.URLField(blank=True, max_length=250)),
                ('date_due', models.DateField(auto_now_add=True)),
                ('is_complete', models.BooleanField(blank=True, default=False)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsauceapp.Company')),
                ('tech_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsauceapp.Tech_Type')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'resource',
                'verbose_name_plural': 'resources',
            },
        ),
        migrations.CreateModel(
            name='Job_Tech',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsauceapp.Job')),
                ('tech_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsauceapp.Tech_Type')),
            ],
            options={
                'verbose_name': 'job_tech',
                'verbose_name_plural': 'job_techs',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='tech_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsauceapp.Tech_Type'),
        ),
        migrations.AddField(
            model_name='job',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Co', to='jobsauceapp.Job'),
        ),
    ]
