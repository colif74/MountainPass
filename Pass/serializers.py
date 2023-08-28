from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import *


# сериализатор вложенной модели уровней сложности перевала
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring',
        ]


# сериализатор вложенной модели географичеких координат перевала
class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height',
        ]


# сериализатор вложенной модели пользователя, создающего запись о перевале
class ClimberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Climber
        fields = [
            'mail',
            'fam',
            'name',
            'otc',
            'phone',
        ]

    def save(self, **kwargs):
        self.is_valid()
        user = Climber.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = Climber.objects.create(
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
                phone=self.validated_data.get('phone'),
                mail=self.validated_data.get('mail'),
            )
            return new_user


class ImagesSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Images
        fields = [
            'pk',
            'name'
        ]


# сериализатор модели самого перевала
class PerevalAddedSerializer(WritableNestedModelSerializer):
    coords = CoordsSerializer()
    category = CategorySerializer()
    author = ClimberSerializer()
    images = ImagesSerializer()

    class Meta:
        model = PerevalAdded
        depth = 1
        fields = [
            'id',
            'beautyTitle',
            'title',
            'other_titles',
            'connect',
            'author',
            'coords',
            'category',
            'images',
            'status',
        ]

    # переопределяем метод post
    def create(self, validated_data, **kwargs):
        author = validated_data.pop('author')
        coords = validated_data.pop('coords')
        category = validated_data.pop('category')
        images = validated_data.pop('images')

        author_ = Climber.objects.filter(email=author['email'])
        if author_.exists():
            author_serializer = ClimberSerializer(data=author)
            author_serializer.is_valid(raise_exception=True)
            author = author_serializer.save()
        else:
            author = Climber.objects.create(**author)

        coords = Coords.objects.create(**coords)
        category = Category.objects.create(**category)
        perevall = PerevalAdded.objects.create(**validated_data, images=images,
                                              author=author, coords=coords, category=category)
        if images:
            for imag in images:
                name = imag.pop(name)
                photo = photo.pop(photo)
                Images.objects.create(perevall=perevall, name=name, photo=photo)

        return perevall

    def validate(self, data):
        if self.instance is not None:
            instance_author = self.instance.author
            data_author = data.get('author')
            author_fields_for_validation = [
                instance_author.fam != data_author['fam'],
                instance_author.name != data_author['name'],
                instance_author.otc != data_author['otc'],
                instance_author.phone != data_author['phone'],
                instance_author.email != data_author['mail'],
            ]
            if data_author is not None and any(author_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Отказано': 'Данные пользователя не могут быть изменены',
                    }
                )
        return data
