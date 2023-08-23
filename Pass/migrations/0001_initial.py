# Generated by Django 4.2.4 on 2023-08-19 06:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], max_length=2, verbose_name='зима')),
                ('summer', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], max_length=2, verbose_name='лето')),
                ('autumn', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], max_length=2, verbose_name='осень')),
                ('spring', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], max_length=2, verbose_name='весна')),
            ],
        ),
        migrations.CreateModel(
            name='Climber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('phone', models.IntegerField(max_length=12, verbose_name='телефон')),
                ('fam', models.CharField(max_length=30, verbose_name='фамилия')),
                ('name', models.CharField(max_length=30, verbose_name='имя')),
                ('otc', models.CharField(max_length=30, verbose_name='отчество')),
            ],
        ),
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(blank=True, max_length=9, verbose_name='широта')),
                ('longitude', models.FloatField(blank=True, max_length=9, verbose_name='долгота')),
                ('height', models.FloatField(blank=True, max_length=5, verbose_name='высота')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('photos', models.FileField(default=0, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beautyTitle', models.CharField(choices=[('poss', 'перевал'), ('gorge', 'ущелье'), ('plateau', 'плато')], max_length=150, verbose_name='тип')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='название')),
                ('other_titles', models.CharField(max_length=150, verbose_name='иные названия')),
                ('connect', models.CharField(max_length=250, verbose_name='соединяет')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('new', 'новый'), ('pending', 'на модерации'), ('accepted', 'принят'), ('rejected', 'не принят')], default='new', max_length=25)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pass.climber')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pass.category')),
                ('coords', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Pass.coords')),
                ('images', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Pass.images')),
            ],
        ),
    ]
