'''
Bloq URL Configuration
'''
from django.urls import path
from .views import BloqBulkCreateView

urlpatterns = [
    path('', BloqBulkCreateView.as_view(), name='bloq-list-create'),
]
