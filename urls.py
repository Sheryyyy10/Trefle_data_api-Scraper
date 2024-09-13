from django.urls import path
from .views import *

urlpatterns = [
    path('scrape-plants/', ScrapePlantDataAPIView.as_view(), name='scrape-plants'),
    path('plants/', PlantListView.as_view(), name='plant-list'),
]
