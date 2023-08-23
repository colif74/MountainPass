from rest_framework.generics import ListAPIView
from . import serializers
from . import models


class CategoryListAPIView(ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return models.Category.objects.all()


class ClimberListAPIView(ListAPIView):
    serializer_class = serializers.ClimberSerializer

    def get_queryset(self):
        return models.Climber.objects.all()


class PerevalAddedListAPIView(ListAPIView):
    serializer_class = serializers.PerevalAddedSerializer

    def get_queryset(self):
        return models.PerevalAdded.objects.all()


class CoordsListAPIView(ListAPIView):
    serializer_class = serializers.CoordsSerializer

    def get_queryset(self):
        return models.Coords.objects.all()


class ImagesListAPIView(ListAPIView):
    serializer_class = serializers.CoordsSerializer

    def get_queryset(self):
        return models.Images.objects.all()