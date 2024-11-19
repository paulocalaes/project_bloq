from django.urls import path
from .views import RentBulkCreateView, RentDropoffView, RentPickupView

urlpatterns = [
    path('', RentBulkCreateView.as_view(), name='rent-list-create'),
    path('<str:id>/dropoff/', RentDropoffView.as_view(), name='rent-dropoff'),
    path('<str:id>/pickup/', RentPickupView.as_view(), name='rent-pickup'),
]
