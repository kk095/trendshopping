# Generated by Django 3.0.7 on 2020-06-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20200605_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
