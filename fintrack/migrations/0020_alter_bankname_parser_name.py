# Generated by Django 5.1.3 on 2024-12-11 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintrack', '0001_squashed_0019_bankname_parser_name_alter_statement_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankname',
            name='parser_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]