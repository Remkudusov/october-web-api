# Generated by Django 3.2.6 on 2021-08-16 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
