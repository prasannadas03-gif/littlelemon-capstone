from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from restaurant.models import Booking, Menu
from restaurant.serializers import MenuSerializer


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="Str0ngPass!")
        self.token = Token.objects.create(user=self.user)
        self.pizza = Menu.objects.create(title="Pizza", price=12.50, inventory=10)
        self.pasta = Menu.objects.create(title="Pasta", price=9.99, inventory=20)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_getall(self):
        response = self.client.get("/restaurant/menu/")
        expected = MenuSerializer(Menu.objects.all().order_by("id"), many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    def test_get_single_item(self):
        response = self.client.get(f"/restaurant/menu/{self.pizza.id}")
        self.assertEqual(response.data["title"], "Pizza")

    def test_create_requires_token(self):
        response = self.client.post("/restaurant/menu/", {"title": "Salad", "price": "7.00", "inventory": 5})
        self.assertEqual(response.status_code, 401)

    def test_create_update_delete_with_token(self):
        self.authenticate()
        response = self.client.post("/restaurant/menu/", {"title": "Salad", "price": "7.00", "inventory": 5})
        self.assertEqual(response.status_code, 201)
        item_id = response.data["id"]

        response = self.client.put(
            f"/restaurant/menu/{item_id}", {"title": "Greek Salad", "price": "8.00", "inventory": 5}
        )
        self.assertEqual(response.data["title"], "Greek Salad")

        response = self.client.delete(f"/restaurant/menu/{item_id}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Menu.objects.filter(id=item_id).exists())


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username="tester", password="Str0ngPass!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=user).key}")
        self.payload = {"name": "Jimmy Doe", "no_of_guests": 4, "booking_date": "2024-12-13T19:00:00Z"}

    def test_booking_requires_token(self):
        self.client.credentials()
        self.assertEqual(self.client.get("/restaurant/booking/tables/").status_code, 401)

    def test_booking_crud(self):
        response = self.client.post("/restaurant/booking/tables/", self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        booking_id = response.data["id"]

        self.assertEqual(len(self.client.get("/restaurant/booking/tables/").data), 1)

        response = self.client.patch(
            f"/restaurant/booking/tables/{booking_id}/", {"no_of_guests": 6}, format="json"
        )
        self.assertEqual(response.data["no_of_guests"], 6)

        response = self.client.delete(f"/restaurant/booking/tables/{booking_id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)

    def test_invalid_guest_count_rejected(self):
        self.payload["no_of_guests"] = 0
        response = self.client.post("/restaurant/booking/tables/", self.payload, format="json")
        self.assertEqual(response.status_code, 400)


class AuthTest(TestCase):
    def test_register_and_get_token(self):
        client = APIClient()
        response = client.post(
            "/auth/users/", {"username": "newuser", "password": "Str0ngPass!", "email": "a@b.com"}
        )
        self.assertEqual(response.status_code, 201)
        response = client.post("/api-token-auth/", {"username": "newuser", "password": "Str0ngPass!"})
        self.assertIn("token", response.data)
