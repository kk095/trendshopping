# Generated by Django 3.0.7 on 2020-06-09 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20200609_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Not order', 'Not order'), ('Out for delivery', 'Out for delivery'), ('delivered', 'delivered')], default='not order', max_length=100),
        ),
    ]
