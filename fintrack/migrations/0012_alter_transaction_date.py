# Generated by Django 5.1.3 on 2024-12-08 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintrack', '0011_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
