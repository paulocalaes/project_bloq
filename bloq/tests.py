from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Bloq
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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