# Generated by Django 3.0.4 on 2020-03-25 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Generator', '0005_skilljson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='code',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
