# Generated by Django 3.1.5 on 2021-01-31 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210131_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ride',
            options={'permissions': (('isDriver', 'search as driver'),)},
        ),
    ]
