# Generated by Django 5.1.3 on 2024-11-28 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authcore', '0002_alter_customuser_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Note',
        ),
    ]
