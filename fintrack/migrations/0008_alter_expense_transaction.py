# Generated by Django 5.1.3 on 2024-12-05 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintrack', '0007_alter_transaction_account_alter_transaction_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='fintrack.transaction'),
        ),
    ]