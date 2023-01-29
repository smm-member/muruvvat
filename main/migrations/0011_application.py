# Generated by Django 4.1.5 on 2023-01-28 17:17

import ckeditor.fields
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_card_number', models.CharField(max_length=10)),
                ('id_card_personal_number', models.IntegerField()),
                ('health_certificate', models.ImageField(upload_to=main.models.application_certificates)),
                ('needed_cash', models.IntegerField()),
                ('deadline', models.DateField()),
                ('card_number', models.IntegerField()),
                ('desc', ckeditor.fields.RichTextField()),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
    ]
