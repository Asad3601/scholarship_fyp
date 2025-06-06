# Generated by Django 5.1.6 on 2025-03-01 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedSchaolarship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('due_date', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('degrees', models.CharField(default='Masters,Bachelors', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.usermodel')),
            ],
        ),
    ]
