import json
# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import *
from .serializers import PerevalAddedSerializer


# Create your tests here.
# Тест для проверки функционала нашего Perevall REST-API
class PerevallTest(APITestCase):
    # создаем данные, с которыми будем работать в последующих тестах
    def setUp(self):
        # два объекта перевалов:
        # первый перевал
        self.perevall1 = PerevalAdded.objects.create(
            beautyTitle='перевал',
            title='Перевал1',
            other_titles='',
            connect='',
            author=Climber.objects.create(
                email='email1@gmail.com',
                fam='Фамилия1',
                name='Имя1',
                otc='Отчество1',
                phone='89271001010'
            ),
            coords=Coords.objects.create(
                latitude=11.1,
                longitude=11.1,
                height=1111
            ),
            category=Category.objects.create(
                winter='',
                summer='1a',
                autumn='1a',
                spring=''
            )
        )
        # картинки к первому перевалу
        self.image11 = Images.objects.create(
            photos='http://www.perevall.com/perevall11.jpg',
            title='Перевал-1-1',
            perevall=self.perevall1
        )
        self.image12 = Images.objects.create(
            photos='http://www.perevall.com/perevall12.jpg',
            title='Перевал-1-2',
            perevall=self.perevall1
        )
        self.image13 = Images.objects.create(
            photos='http://www.perevall.com/perevall13.jpg',
            title='Перевал-1-3',
            perevall=self.perevall1
        )

        # второй перевал
        self.perevall2 = PerevalAdded.objects.create(
            beautyTitle='перевал',
            title='Перевал2',
            other_titles='',
            connect='',
            author=Climber.objects.create(
                mail='email2@gmail.com',
                fam='Фамилия2',
                name='Имя2',
                otc='',
                phone='5155515151512'
            ),
            coords=Coords.objects.create(
                latitude=22.2,
                longitude=22.2,
                height=2222
            ),
            category=Category.objects.create(
                winter='',
                summer='1b',
                autumn='1b',
                spring=''
            ),
            status='pending'
        )
        # картинки ко второму перевалу
        self.image21 = Images.objects.create(
            photos='http://www.perevall.com/perevall21.jpg',
            title='Перевал-2-1',
            perevall=self.perevall2
        )
        self.image22 = Images.objects.create(
            photos='http://www.perevall.com/perevall22.jpg',
            title='Перевал-2-2',
            perevall=self.perevall2
        )
        self.image23 = Images.objects.create(
            photos='http://www.perevall.com/perevall23.jpg',
            title='Перевал-2-3',
            perevall=self.perevall2
        )

    # проверяем получение всех записей о перевалах
    def test_perevall_list(self):
        response = self.client.get(reverse('perevall-list'))
        serializer_data = PerevalAddedSerializer([self.perevall1, self.perevall2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)
        self.assertEqual(serializer_data, response.data.get('results'))

    # проверяем получение записи о втором перевале
    def test_perevall_detail(self):
        response = self.client.get(reverse('perevall-detail', kwargs={'pk': self.perevall2.id}))
        serializer_data = PerevalAddedSerializer(self.perevall2).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    # проверяем создание записи о перевале и использование данных пользователя, если он уже есть в БД, вместо создания
    # нового
    def test_valid_create_and_user_reuse(self):
        data = {
            'beauty_title': 'перевал',
            'title': 'Перевал3',
            'other_titles': '',
            'connect': '',
            'author': {
                'mail': 'email1@gmail.com',
                'fam': 'Фамилия1',
                'name': 'Имя1',
                'otc': 'Отчество1',
                'phone': '5155515151512'
            },
            'coords': {
                'latitude': 33.3,
                'longitude': 33.3,
                'height': 3333
            },
            'category': {
                'winter': '',
                'summer': '2a',
                'autumn': '2b',
                'spring': ''
            },
            'images': [
                {
                    'photos': 'http://www.perevall.com/perevall31.jpg',
                    'name': 'Перевал-3-1'
                },
                {
                    'photos': 'https://www.perevall.com/perevall32.jpg',
                    'name': 'Перевал-3-2'
                }
            ]
        }
        json_photos = json.dumps(data)
        response = self.client.post(reverse('perevall-list'), photos=json_photos, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PerevalAdded.objects.all().count(), 3)
        self.assertEqual(Climber.objects.all().count(), 2)

    # проверяем отсутствие создания записи о перевале при незаполненных обязательных полях
    def test_invalid_create(self):
        data = {
            'beautyTitle': 'перевал',
            'title': '',
            'other_titles': 'Перевал4',
            'connect': 'Соединяет4',
            'author': {
                'mail': '',
                'fam': '',
                'name': '',
                'otc': '',
                'phone': ''
            },
            'coords': {
                'latitude': 44.4,
                'longitude': 44.4,
                'height': 4444
            },
            'category': {
                'winter': '1a',
                'summer': '1a',
                'autumn': '1a',
                'spring': '1a'
            },
            'images': [
                {
                    'photos': 'http://www.perevall.com/perevall41.jpg',
                    'name': 'Перевал-4-1'
                },
            ],
            'status': 'new'
        }
        json_data = json.dumps(data)
        response = self.client.post(reverse('perevall-list'), photos=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PerevalAdded.objects.all().count(), 2)

    # проверяем обновление разрешенных данных
    def test_valid_update(self):
        data = {
            'beautyTitle': 'перевал',
            'title': 'Перевал1',
            'other_titles': 'Перевал1',
            'connect': 'Соединяет1',
            'author': {
                'mail': 'email1@gmail.com',
                'fam': 'Фамилия1',
                'name': 'Имя1',
                'otc': 'Отчество1',
                'phone': '5155515151512'
            },
            'coords': {
                'latitude': 55.5,
                'longitude': 55.5,
                'height': 5555
            },
            'category': {
                'winter': '3b',
                'summer': '2b',
                'autumn': '3a',
                'spring': '3b'
            },
            'images': [
                {
                    'photos': 'http://www.perevall.com/perevall11.jpg',
                    'name': 'Перевал-1-1'
                },
                {
                    'photos': 'http://www.passages.com/passage12.jpg',
                    'name': 'Перевал-1-2'
                },
                {
                    'photos': 'http://www.passages.com/passage13.jpg',
                    'name': 'Перевал-1-3'
                },
            ],
            'status': 'accepted'
        }

        json_data = json.dumps(data)
        response = self.client.patch(
            reverse('perevall-detail', kwargs={'pk': self.perevall1.id}),
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.perevall1.refresh_from_db()
        self.assertEqual('Перевал1', self.perevall1.other_titles)
        self.assertEqual('Соединяет1', self.perevall1.connect)
        self.assertEqual(55.5, self.perevall1.coords.latitude)
        self.assertEqual(55.5, self.perevall1.coords.longitude)
        self.assertEqual(5555, self.perevall1.coords.height)
        self.assertEqual('3b', self.perevall1.level.winter)
        self.assertEqual('2b', self.perevall1.level.summer)
        self.assertEqual('3a', self.perevall1.level.autumn)
        self.assertEqual('3b', self.perevall1.level.spring)
        self.assertEqual('accepted', self.perevall1.status)

    # проверяем отсутствие обновления разрешенных данных, если статус не new
    def test_invalid_update_if_status_is_not_new(self):
        data = {
            'beautyTitle': 'перевал',
            'title': 'Перевал2',
            'other_titles': '',
            'connect': 'Соединяет2',
            'author': {
                'mail': 'email2@gmail.com',
                'fam': 'Фамилия2',
                'name': 'Имя2',
                'otc': '',
                'phone': '89272002020'
            },
            'coords': {
                'latitude': 22.2,
                'longitude': 22.2,
                'height': 2222
            },
            'category': {
                'winter': '',
                'summer': '1b',
                'autumn': '1b',
                'spring': ''
            },
            'images': [
                {
                    'photos': 'http://www.perevall.com/perevall21.jpg',
                    'name': 'Перевал-2-1'
                },
                {
                    'photos': 'http://www.perevall.com/perevall22.jpg',
                    'name': 'Перевал-2-2'
                },
                {
                    'photos': 'http://www.perevall.com/perevall23.jpg',
                    'name': 'Перевал-2-3'
                },
            ],
            'status': 'pending'
        }

        json_data = json.dumps(data)
        response = self.client.patch(
            reverse('perevall-detail', kwargs={'pk': self.perevall2.id}),
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.perevall2.refresh_from_db()
        self.assertEqual('', self.perevall2.connect)

    # проверяем отсутствие возможности изменить данные пользователя
    def test_climber_update(self):
        data = {
            '': {
                'mail': 'email3@mail.ru',
                'fam': 'Фамилия3',
                'name': 'Имя3',
                'otc': 'Отчество3',
                'phone': '89088269331'
            },
            'beautyTitle': 'перевал',
            'title': 'Перевал1',
            'other_titles': '',
            'connect': '',
            'coords': {
                'latitude': 11.1,
                'longitude': 11.1,
                'height': 1111
            },
            'category': {
                'winter': '',
                'summer': '1a',
                'autumn': '1a',
                'spring': ''
            },
            'status': 'new',
            'images': [
                {
                    'photos': 'http://www.perevall.com/perevall1-1.jpg',
                    'name': 'Перевал-1-1'
                },
                {
                    'photos': 'http://www.passages.com/passage1-2.jpg',
                    'name': 'Перевал-1-2'
                },
                {
                    'photos': 'http://www.passages.com/passage1-3.jpg',
                    'name': 'Перевал-1-3'
                },
            ]
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            reverse('perevall-detail', kwargs={'pk': self.perevall1.id}),
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.perevall1.refresh_from_db()
        self.assertEqual('email1@gmail.com', self.perevall1.user.email)
        self.assertEqual('Фамилия1', self.perevall1.user.fam)
        self.assertEqual('Имя1', self.perevall1.user.name)
        self.assertEqual('Отчество1', self.perevall1.user.otc)
        self.assertEqual('5155515151512', self.perevall1.user.phone)
