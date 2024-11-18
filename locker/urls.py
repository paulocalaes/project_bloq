from django.urls import path
from .views import LockerListCreate

urlpatterns = [
    path('', LockerListCreate.as_view(), name='locker-list-create'),
]
