# Generated by Django 4.2.7 on 2023-11-27 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_remove_purchaseorder_approval_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 28, 1, 50, 20, 137843)),
        ),
    ]