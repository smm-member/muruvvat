# Generated by Django 4.0.3 on 2022-04-05 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_surai_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ayah',
            name='chapter',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ayah',
            name='verse',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
