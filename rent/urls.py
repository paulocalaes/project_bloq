from django.urls import path
from .views import RentListCreate

urlpatterns = [
    path('', RentListCreate.as_view(), name='rent-list-create'),
]
