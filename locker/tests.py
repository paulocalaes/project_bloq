from django.test import TestCase
from .models import Locker, LockerStatus
from rest_framework.test import APITestCase
from django.urls import reverse
from bloq.models import Bloq
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Locker, LockerStatus, LockerSize

class LockerModelTest(TestCase):
    def setUp(self):
        self.bloq = Bloq.objects.create(
            id="1",
            title="Bloq Test",
            address="Test Address",
        )
        self.locker = Locker.objects.create(
            id="1",
            bloqId=self.bloq,
            status=LockerStatus.OPEN,
            isOccupied=False
        )

    def test_locker_creation(self):
        self.assertEqual(self.locker.bloqId, self.bloq)
        self.assertEqual(self.locker.status, LockerStatus.OPEN)
        self.assertFalse(self.locker.isOccupied)
        self.assertEqual(str(self.locker), "Locker 1 - OPEN")

class LockerAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('locker-list-create', kwargs={'version': 'v1'})
        self.bloq = Bloq.objects.create(id="1", title="Bloq A", address="Address A")
        self.locker_data = [
            {
                "id": "1",
                "bloqId": self.bloq.id,
                "status": "OPEN",
                "isOccupied": False
            },
            {
                "id": "2",
                "bloqId": self.bloq.id,
                "status": "CLOSED",
                "isOccupied": True
            }
        ]

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_multiple_lockers(self):
        response = self.client.post(self.url, self.locker_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Locker.objects.count(), 2)

    def test_get_locker_list(self):
        Locker.objects.create(id="1", bloqId=self.bloq, status=LockerStatus.OPEN, isOccupied=False)
        Locker.objects.create(id="2", bloqId=self.bloq, status=LockerStatus.CLOSED, isOccupied=True)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

class AvailableLockerAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('locker-available-list', kwargs={'version': 'v1'})
        self.bloq = Bloq.objects.create(id="1", title="Bloq A", address="Address A")
        self.locker1 = Locker.objects.create(
            id="1", bloqId=self.bloq, status=LockerStatus.OPEN, isOccupied=False, size=LockerSize.M
        )
        self.locker2 = Locker.objects.create(
            id="2", bloqId=self.bloq, status=LockerStatus.CLOSED, isOccupied=True, size=LockerSize.M
        )
        self.locker3 = Locker.objects.create(
            id="3", bloqId=self.bloq, status=LockerStatus.OPEN, isOccupied=False, size=LockerSize.L
        )
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_available_lockers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 2)
        locker_ids = [locker['id'] for locker in response.data]
        self.assertIn('1', locker_ids)
        self.assertIn('3', locker_ids)

    def test_filter_by_bloq_id(self):
        response = self.client.get(self.url, {'bloq': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

    def test_filter_by_size(self):
        response = self.client.get(self.url, {'size': 'M'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], '1')
