# Generated by Django 3.1.2 on 2020-10-09 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
