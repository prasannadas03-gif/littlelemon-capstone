from datetime import datetime, timezone

from django.test import TestCase

from restaurant.models import Booking, Menu


class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")


class BookingTest(TestCase):
    def test_create_booking(self):
        booking = Booking.objects.create(
            name="Jimmy Doe",
            no_of_guests=4,
            booking_date=datetime(2024, 12, 13, 19, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(str(booking), "Jimmy Doe (4) - 2024-12-13 19:00")
