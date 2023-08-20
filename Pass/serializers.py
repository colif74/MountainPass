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
    user = ClimberSerializer()
    images = ImagesSerializer()

    class Meta:
        model = PerevalAdded
        depth = 1
        fields = [
            'pk',
            'beautyTitle',
            'title',
            'other_titles',
            'connect',
            'user',
            'coords',
            'category',
            'images',
            'status',
        ]

    # переопределяем метод post
    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        category = validated_data.pop('category')
        images = validated_data.pop('images')

        user_ = Climber.objects.filter(email=user['email'])
        if user_.exists():
            user_serializer = ClimberSerializer(data=user)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        else:
            user = Climber.objects.create(**user)

        coords = Coords.objects.create(**coords)
        category = Category.objects.create(**category)
        passage = PerevalAdded.objects.create(**validated_data, images=images,
                                              user=user, coords=coords, category=category)

        return passage

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            user_fields_for_validation = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['mail'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Отказано': 'Данные пользователя не могут быть изменены',
                    }
                )
        return data
