from django.urls import path
from .views import LockerBulkCreateView
from .views import AvailableLockerListView

urlpatterns = [
    path('', LockerBulkCreateView.as_view(), name='locker-list-create'),
    path('available/', AvailableLockerListView.as_view(), name='locker-available-list'),
    # GET /api/v1/lockers/{locker_id}/
    # delete /api/v1/lockers/{locker_id}/
    # PUT /api/v1/lockers/{locker_id}/
    # POST /api/v1/lockers/{locker_id}/report_issue/
]
