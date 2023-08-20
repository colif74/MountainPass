from django.urls import path
from . import api

urlpatterns = [
    path('category', api.CategoryListAPIView.as_view(), name='api_categories'),
    path('climber', api.ClimberListAPIView.as_view(), name='api_climbers'),
    path('pereval', api.PerevalAddedListAPIView.as_view(), name='api_pereval'),
]

