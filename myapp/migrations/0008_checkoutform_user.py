# Generated by Django 3.0.5 on 2020-05-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20200529_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutform',
            name='user',
            field=models.CharField(default='', max_length=20),
        ),
    ]
