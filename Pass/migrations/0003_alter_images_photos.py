# Generated by Django 4.2.4 on 2023-08-23 14:17

import Pass.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pass', '0002_alter_coords_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='photos',
            field=models.ImageField(blank=True, null=True, upload_to=Pass.models.get_image_path, verbose_name='Фото'),
        ),
    ]
