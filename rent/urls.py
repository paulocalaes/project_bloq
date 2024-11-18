from django.urls import path
from .views import RentBulkCreateView

urlpatterns = [
    path('', RentBulkCreateView.as_view(), name='rent-list-create'),
]
