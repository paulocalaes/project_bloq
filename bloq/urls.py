'''
Bloq URL Configuration
'''
from django.urls import path
from .views import BloqBulkCreateView, BloqDetailView, BloqLockerAvailableView, BloqLockerOccupiedView, BloqLockersListView

urlpatterns = [
    path('', BloqBulkCreateView.as_view(), name='bloq-list-create'),
    path('<str:id>/', BloqDetailView.as_view(), name='bloq-detail'),
    path('<str:id>/lockers/', BloqLockersListView.as_view(), name='bloq-lockers'),
    path('<str:id>/lockers/available/', BloqLockerAvailableView.as_view(), name='bloq-locker-available'),
    path('<str:id>/lockers/occupied/', BloqLockerOccupiedView.as_view(), name='bloq-locker-occupied'),
]
