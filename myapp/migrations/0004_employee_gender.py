# Generated by Django 3.0.5 on 2021-06-26 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210625_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(default='Human', max_length=255),
        ),
    ]