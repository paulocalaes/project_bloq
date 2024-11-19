from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from locker.models import Locker, LockerStatus
from bloq.models import Bloq
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Rent, RentStatus, LockerSize as RentSize

class RentModelTest(TestCase):
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
        self.rent = Rent.objects.create(
            id="1",
            lockerId=self.locker,
            weight=10.5,
            size=RentSize.M,
            status=RentStatus.CREATED
        )

    def test_rent_creation(self):
        self.assertEqual(self.rent.lockerId, self.locker)
        self.assertEqual(self.rent.weight, 10.5)
        self.assertEqual(self.rent.size, RentSize.M)
        self.assertEqual(self.rent.status, RentStatus.CREATED)
        self.assertEqual(str(self.rent), "Rent 1 - CREATED")


class RentAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('rent-list-create', kwargs={'version': 'v1'})
        self.bloq = Bloq.objects.create(id="1", title="Bloq A", address="Endereço A")
        self.locker = Locker.objects.create(id="1", bloqId=self.bloq, status=LockerStatus.OPEN, isOccupied=False)
        self.rent_data = [
            {
                "id": "1",
                "lockerId": self.locker.id,
                "weight": 10.5,
                "size": "M",
                "status": "CREATED"
            },
            {
                "id": "2",
                "lockerId": self.locker.id,
                "weight": 5.0,
                "size": "S",
                "status": "WAITING_PICKUP"
            }
        ]
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_multiple_rents(self):
        response = self.client.post(self.url, self.rent_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Rent.objects.count(), 2)

    def test_get_rent_list(self):
        # Primeiro, cria alguns Rents
        Rent.objects.create(
            id="1",
            lockerId=self.locker,
            weight=10.5,
            size=RentSize.M,
            status=RentStatus.CREATED
        )
        Rent.objects.create(
            id="2",
            lockerId=self.locker,
            weight=5.0,
            size=RentSize.S,
            status=RentStatus.WAITING_PICKUP
        )

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_dropoff_rent(self):
        rent = Rent.objects.create(
            id="1",
            lockerId=self.locker,
            weight=10.5,
            size=RentSize.M,
            status=RentStatus.WAITING_DROPOFF
        )
        url = reverse('rent-dropoff', kwargs={'version': 'v1', 'id': rent.id})
        response = self.client.patch(url, {}, format='json')
        rent = Rent.objects.get(id=rent.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rent.status, RentStatus.WAITING_PICKUP)
        locker = Locker.objects.get(id=self.locker.id)
        self.assertTrue(locker.isOccupied)

    def test_pickup_rent(self):
        rent = Rent.objects.create(
            id="1",
            lockerId=self.locker,
            weight=10.5,
            size=RentSize.M,
            status=RentStatus.WAITING_PICKUP
        )
        url = reverse('rent-pickup', kwargs={'version': 'v1', 'id': rent.id})
        response = self.client.patch(url, {}, format='json')
        rent = Rent.objects.get(id=rent.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rent.status, RentStatus.DELIVERED)
        locker = Locker.objects.get(id=self.locker.id)
        self.assertFalse(locker.isOccupied)
        self.assertEqual(locker.status, LockerStatus.OPEN)