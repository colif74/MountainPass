# Generated by Django 4.2.4 on 2023-08-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pass', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coords',
            name='height',
            field=models.IntegerField(blank=True, max_length=5, verbose_name='высота'),
        ),
    ]
