# Generated by Django 3.1.5 on 2021-02-22 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_notification_date_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='user',
            new_name='claimed_by',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='report_on',
            new_name='claimed_on',
        ),
    ]