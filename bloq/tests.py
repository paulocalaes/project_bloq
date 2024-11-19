from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from locker.models import Locker, LockerStatus, LockerSize
from .models import Bloq

class BloqModelTest(TestCase):
    def setUp(self):
        self.bloq = Bloq.objects.create(
            id="1",
            title="Bloq Test",
            address="Test Address",
        )

    def test_bloq_creation(self):
        self.assertEqual(self.bloq.title, "Bloq Test")
        self.assertEqual(self.bloq.address, "Test Address")
        self.assertEqual(str(self.bloq), "Bloq Test")


class BloqAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('bloq-list-create', kwargs={'version': 'v1'})
        self.bloq_data = [
            {
                "id": "1",
                "title": "Bloq A",
                "address": "Address A"
            },
            {
                "id": "2",
                "title": "Bloq B",
                "address": "Address B"
            }
        ]

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_multiple_bloqs(self):
        response = self.client.post(self.url, self.bloq_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bloq.objects.count(), 2)

    def test_get_bloq_list(self):
        Bloq.objects.create(id="1", title="Bloq A", address="Address A")
        Bloq.objects.create(id="2", title="Bloq B", address="Address B")

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_invalid_bloq(self):
        invalid_data = [
            {
                "id": "",  # Empyt ID 
                "title": "Bloq Invalid",
                "address": "Invalid Address"
            }
        ]
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_get_bloq_detail(self):
        Bloq.objects.create(id="1", title="Bloq A", address="Address A")
        response = self.client.get(f"/api/v1/bloq/1/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Bloq A')

    def test_update_bloq(self):
        Bloq.objects.create(id="1", title="Bloq A", address="Address A")
        payload = {  
            "title": "Bloq Updated",  
        }  
        response = self.client.patch(f"/api/v1/bloq/1/",data=payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Bloq Updated')

    def test_delete_bloq(self):
        Bloq.objects.create(id="1", title="Bloq A", address="Address A")
        response = self.client.delete(f"/api/v1/bloq/1/", format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Bloq.objects.count(), 0)

    def create_bloq_locker(self):
        bloq_a = Bloq.objects.create(id="1", title="Bloq A", address="Address A")
        bloq_b = Bloq.objects.create(id="2", title="Bloq B", address="Address B")
        Locker.objects.create(
            id="1", bloqId=bloq_a, status=LockerStatus.OPEN, isOccupied=False, size=LockerSize.M
        )
        Locker.objects.create(
            id="2", bloqId=bloq_b, status=LockerStatus.CLOSED, isOccupied=True, size=LockerSize.M
        )

    def test_get_bloq_lockers(self):
        self.create_bloq_locker()
        response = self.client.get(f"/api/v1/bloq/1/lockers/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], LockerStatus.OPEN)

    def test_get_bloq_locker_available(self):
        self.create_bloq_locker()
        response = self.client.get(f"/api/v1/bloq/1/lockers/available/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['isOccupied'], False)
    
    def test_get_bloq_locker_available_zero(self):
        self.create_bloq_locker()
        response = self.client.get(f"/api/v1/bloq/2/lockers/available/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_bloq_locker_occupied(self):
        self.create_bloq_locker()
        response = self.client.get(f"/api/v1/bloq/2/lockers/occupied/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['isOccupied'], True)

    def test_get_bloq_locker_occupied_zero(self):
        self.create_bloq_locker()
        response = self.client.get(f"/api/v1/bloq/1/lockers/occupied/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    