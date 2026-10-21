from rest_framework import serializers

from .models import Booking, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'price', 'inventory']


class BookingSerializer(serializers.ModelSerializer):
    no_of_guests = serializers.IntegerField(min_value=1, max_value=20)

    class Meta:
        model = Booking
        fields = ['id', 'name', 'no_of_guests', 'booking_date']

