from django.test import TestCase
from restaurant.models import Menu
import json

class MenuViewTest(TestCase):

    def setUp(self) -> None:
        Menu.objects.create(title="IceCream", price=80, inventory=100)
        Menu.objects.create(title="Pizza", price=180, inventory=100)
        Menu.objects.create(title="Burger", price=100, inventory=100)
        Menu.objects.create(title="Pasta", price=140, inventory=100)

        return super().setUp()

    def test_get_all_menu(self):
        response = self.client.get('/restaurant/menu')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 4)

        self.assertEqual(data[0]['title'], 'IceCream')
        self.assertEqual(data[0]['price'], '80.00')
        self.assertEqual(data[0]['inventory'], 100)

        self.assertEqual(data[1]['title'], 'Pizza')
        self.assertEqual(data[1]['price'], '180.00')
        self.assertEqual(data[1]['inventory'], 100)

        self.assertEqual(data[2]['title'], 'Burger')
        self.assertEqual(data[2]['price'], '100.00')
        self.assertEqual(data[2]['inventory'], 100)

        self.assertEqual(data[3]['title'], 'Pasta')
        self.assertEqual(data[3]['price'], '140.00')
        self.assertEqual(data[3]['inventory'], 100)