from django.urls import path
from .views import BloqListCreate

urlpatterns = [
    path('', BloqListCreate.as_view(), name='bloq-list-create'),
]
