from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status


class ActivityViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')

    def test_unauthenticated_cannot_create_activity(self):
        response = self.client.post('/api/activities/', {'title': 'Test Activity'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_cannot_create_activity(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/activities/', {'title': 'Test Activity'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_activity(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/activities/', {
            'title': 'Test Activity',
            'description': 'Test Description',
            'base_price': 100.00,
            'currency': 'USD',
            'duration_days': 1,
            'group_size_min': 1,
            'group_size_max': 10,
            'age_min': 18,
            'age_max': 65,
            'category': None  # Assuming category can be null or create one
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
