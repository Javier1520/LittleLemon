# LittleLemonAPI/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart, Order, OrderItem

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        if User.objects.filter(username='testuser').exists():
            User.objects.filter(username='testuser').delete()

        # Create a user and set up authentication
        self.user = User.objects.create_user(username='testuser', password='password')

        # Ensure the Manager group does not already exist
        self.manager_group, created = Group.objects.get_or_create(name='Manager')
        self.user.groups.add(self.manager_group)

        # Obtain auth token if using token-based authentication
        response = self.client.post('/api/auth/token/login/', {'username': 'testuser', 'password': 'password'})

        self.token = response.data.get('auth_token')
        if self.token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Creating test data
        self.category = Category.objects.create(slug="test-category", title="Test Category")
        self.menu_item = MenuItem.objects.create(title="Test Item", price=10.00, featured=False, category=self.category)
        self.order = Order.objects.create(user=self.user, total=10.00)

    def test_login(self):
        response = self.client.post('/api/auth/token/login/', {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_access(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_creation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('categories'), {'slug': 'new-category', 'title': 'New Category'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_menu_item_creation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('menu-items'), {
            'title': 'New Item', 'price': 15.00, 'featured': False, 'category_id': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cart_operations(self):
        self.client.force_authenticate(user=self.user)

        # Create a cart item
        response = self.client.post(reverse('cart'), {'menuitem_id': self.menu_item.id, 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve the cart item
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_creation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('orders'), {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_single_order_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('single-order', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_user_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('manager-users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delivery_crew_user_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('delivery-crew-users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
