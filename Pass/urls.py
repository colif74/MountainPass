from django.urls import path
from . import api
from .views import IndexView, PerevalAddedViewSet, ClimberViewSet
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static



router = routers.DefaultRouter()
router.register(r'perevall', PerevalAddedViewSet)
router.register(r'climber', ClimberViewSet)


urlpatterns = [
    path('', IndexView.as_view()),
    path('category', api.CategoryListAPIView.as_view(), name='api_categories'),
    path('climber', api.ClimberListAPIView.as_view(), name='api_climbers'),
    path('perevall', api.PerevalAddedListAPIView.as_view(), name='api_perevall'),

]
urlpatterns.extend(router.urls)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
