# Generated by Django 4.1.5 on 2023-01-28 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='is_it_for_print',
            field=models.BooleanField(default=False),
        ),
    ]
