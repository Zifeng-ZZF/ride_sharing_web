# Generated by Django 3.1.5 on 2021-02-02 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20210202_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='login.driver'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='sharer',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='special_request',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
