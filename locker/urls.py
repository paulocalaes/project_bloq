from django.urls import path
from .views import LockerBulkCreateView, LockerDetailView, AvailableLockerListView

urlpatterns = [
    path('', LockerBulkCreateView.as_view(), name='locker-list-create'),
    path('available/', AvailableLockerListView.as_view(), name='locker-available-list'),
    path('<str:id>/', LockerDetailView.as_view(), name='locker-detail'),

    #implement the following endpoints with Admin permissions
    # delete /api/v1/lockers/{locker_id}/
    # PUT /api/v1/lockers/{locker_id}/

    #implement the following endpoints with User permissions
    # POST /api/v1/lockers/{locker_id}/report_issue/
]
