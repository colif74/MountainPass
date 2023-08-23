from django.urls import path
from . import api
from .views import *



urlpatterns = [
    path('', IndexView.as_view()),
    path('category', api.CategoryListAPIView.as_view(), name='api_categories'),
    path('climber', api.ClimberListAPIView.as_view(), name='api_climbers'),
    path('perevall', api.PerevalAddedListAPIView.as_view(), name='api_pereval'),

]
