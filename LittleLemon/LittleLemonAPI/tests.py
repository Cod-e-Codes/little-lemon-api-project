from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework import status
from .models import MenuItem, Category, Order

class LittleLemonAPITests(TestCase):
    def setUp(self):
        # Create test groups
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        delivery_group, _ = Group.objects.get_or_create(name='Delivery Crew')

        # Create test users
        self.manager_user = User.objects.create_user(
            username='manager', 
            password='managerpass'
        )
        self.manager_user.groups.add(manager_group)

        self.delivery_user = User.objects.create_user(
            username='delivery', 
            password='deliverypass'
        )
        self.delivery_user.groups.add(delivery_group)

        self.customer_user = User.objects.create_user(
            username='customer', 
            password='customerpass'
        )

        # Create test category and menu item
        self.category = Category.objects.create(
            slug='test-category', 
            title='Test Category'
        )
        self.menu_item = MenuItem.objects.create(
            title='Test Menu Item',
            price=10.00,
            category=self.category
        )

        # Setup API clients
        self.manager_client = APIClient()
        self.manager_client.force_authenticate(user=self.manager_user)

        self.customer_client = APIClient()
        self.customer_client.force_authenticate(user=self.customer_user)

    def test_menu_item_list(self):
        response = self.customer_client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    def test_manager_can_create_menu_item(self):
        data = {
            'title': 'New Menu Item',
            'price': 15.00,
            'category_id': self.category.id
        }
        response = self.manager_client.post('/api/menu-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_cannot_create_menu_item(self):
        data = {
            'title': 'New Menu Item',
            'price': 15.00,
            'category_id': self.category.id
        }
        response = self.customer_client.post('/api/menu-items/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)