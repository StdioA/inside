# Generated by Django 2.0.7 on 2018-07-22 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblog', '0002_auto_20160817_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Published'),
        ),
    ]