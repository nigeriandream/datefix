# Generated by Django 3.0.6 on 2020-08-05 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='text',
            field=models.TextField(),
        ),
    ]