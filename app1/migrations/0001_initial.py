# Generated by Django 3.1.5 on 2021-01-21 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LostOrFound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number', models.PositiveIntegerField(default=-999)),
                ('category', models.CharField(blank=True, max_length=10, null=True)),
                ('description', models.TextField(help_text='write in short what you lost/found', max_length=500)),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]