from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


def index(request):
    """Static HTML home page served by Django."""
    return render(request, 'index.html', {})


class MenuItemsView(generics.ListCreateAPIView):
    """GET: list menu items (public). POST: add an item (token required)."""
    queryset = Menu.objects.all().order_by('id')
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """GET one item (public). PUT/PATCH/DELETE (token required)."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """Full CRUD on table bookings. Every request needs a token."""
    queryset = Booking.objects.all().order_by('booking_date')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

