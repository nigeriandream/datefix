# Generated by Django 3.0.6 on 2020-08-05 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_auto_20200803_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='secret',
        ),
    ]