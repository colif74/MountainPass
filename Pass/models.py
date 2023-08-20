from django.db import models
from django.utils import timezone


BEAUTYTITLE = [
    ('poss', 'перевал'),
    ('gorge', 'ущелье'),
    ('plateau', 'плато'),
]


STATUS = [
    ('new', 'новый'),
    ('pending', 'на модерации'),
    ('accepted', 'принят'),
    ('rejected', 'не принят'),
]

LEVELS = [
    ('', 'не указано'),
    ('1A', '1a'),
    ('1B', '1б'),
    ('2А', '2а'),
    ('2В', '2б'),
    ('3А', '3а'),
    ('3В', '3б'),
    ]


class Climber(models.Model):

    mail = models.EmailField('почта', unique=True)
    phone = models.IntegerField('телефон', max_length=12)
    fam = models.CharField('фамилия', max_length=30)
    name = models.CharField('имя', max_length=30)
    otc = models.CharField('отчество', max_length=30)

    def __str__(self):
        return f'{self.fam}'


class Category(models.Model):
    winter = models.CharField('зима', max_length=2, choices=LEVELS)
    summer = models.CharField('лето', max_length=2, choices=LEVELS)
    autumn = models.CharField('осень', max_length=2, choices=LEVELS)
    spring = models.CharField('весна', max_length=2, choices=LEVELS)

    def __str__(self):
        return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, весна: {self.spring}'


class Coords(models.Model):

    latitude = models.FloatField('широта', max_length=9, blank=True)
    longitude = models.FloatField('долгота', max_length=9, blank=True)
    height = models.IntegerField('высота', max_length=5, blank=True)


class Images(models.Model):
    name = models.CharField(max_length=50)
    photos = models.FileField(upload_to='images', default=0)


class PerevalAdded(models.Model):
    beautyTitle = models.CharField('тип', choices=BEAUTYTITLE, max_length=150)
    title = models.CharField('название', max_length=150, blank=True)
    other_titles = models.CharField('иные названия', max_length=150)
    connect = models.CharField('соединяет', max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ForeignKey(Images, on_delete=models.CASCADE, default=0)
    add_time = models.DateTimeField(default=timezone.now, editable=False)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    author = models.ForeignKey(Climber, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=25, default='new')


class PassUser(models.Model):
    climber = models.ForeignKey(Climber, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
