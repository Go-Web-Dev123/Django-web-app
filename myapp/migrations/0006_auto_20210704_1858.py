# Generated by Django 3.0.5 on 2021-07-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_employee_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='email',
            field=models.CharField(default='balahari765@gmail.com', max_length=255),
        ),
        migrations.AddField(
            model_name='manager',
            name='email',
            field=models.CharField(default='balahari765@gmail.com', max_length=255),
        ),
    ]