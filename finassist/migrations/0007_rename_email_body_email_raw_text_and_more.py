# Generated by Django 5.1.3 on 2024-12-04 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finassist', '0006_email_from_email_name_email_raw_html_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='email_body',
            new_name='raw_text',
        ),
        migrations.RemoveField(
            model_name='email',
            name='plain_text_body',
        ),
    ]