# Generated by Django 3.0.4 on 2020-03-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Generator', '0003_auto_20200324_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
