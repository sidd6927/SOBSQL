from django.urls import path
from .views import *

urlpatterns = [
    path('insert-data/', insert_data, name='insert-data'),
    path('fetch-data/', fetch_data, name='fetch-data'),
    path('', welcome_page, name='welcome'),
]
