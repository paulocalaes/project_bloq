from django.urls import path
from .views import LockerBulkCreateView

urlpatterns = [
    path('', LockerBulkCreateView.as_view(), name='locker-list-create'),
]
