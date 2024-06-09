from django.test import TestCase
from restaurant.models import Menu

class MenuItemTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title='Chocolate', price=50, inventory=100)
        self.assertEqual(item.title, "Chocolate")
        self.assertEqual(item.price, 50)