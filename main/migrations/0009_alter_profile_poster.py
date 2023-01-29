# Generated by Django 4.1.5 on 2023-01-28 12:04

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='poster',
            field=models.ImageField(default='posters/default.png', upload_to=main.models.user_directory_path, verbose_name='Poster'),
        ),
    ]
