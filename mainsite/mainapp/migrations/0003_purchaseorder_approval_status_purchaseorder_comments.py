# Generated by Django 4.2.7 on 2023-11-21 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_userorganization'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='approval_status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='comments',
            field=models.CharField(default='', max_length=255),
        ),
    ]