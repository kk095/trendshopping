# Generated by Django 3.0.7 on 2020-06-06 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200606_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='unique_id',
            field=models.CharField(default='', max_length=20),
        ),
    ]
