# Generated by Django 5.1.3 on 2024-12-11 19:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintrack', '0020_alter_bankname_parser_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.CharField(max_length=255, unique=True)),
                ('snippet', models.TextField(blank=True, null=True)),
                ('from_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('from_email_name', models.CharField(blank=True, max_length=255, null=True)),
                ('subject', models.CharField(max_length=255)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('raw_html', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('raw_text', models.TextField(blank=True, null=True)),
                ('label', models.CharField(blank=True, max_length=50, null=True)),
                ('processed_text', models.TextField(blank=True, null=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
