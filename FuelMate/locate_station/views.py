# accounts/views.py
import random
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from .models import GasStation, PostalCode

from django.contrib.auth.decorators import login_required
from math import radians, cos, sin, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Promień Ziemi w kilometrach
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# accounts/views.py
from django.contrib.auth.views import LoginView


from django.shortcuts import render

def search_stations_by_postal_code(request):
    postal_code = request.GET.get('postal_code', '').strip()
    stations = GasStation.objects.filter(address__icontains=postal_code)
    return render(request, 'search.html', {'stations': stations, 'postal_code': postal_code})
def all_stations_view(request):
    stations = GasStation.objects.all()
    return render(request, 'search.html', {'stations': stations})
@login_required
def logged_in_view(request):
    stations = []
    postal_code = request.GET.get('postal_code', '').strip()
    latitude = request.GET.get('latitude')  # Szerokość geograficzna użytkownika
    longitude = request.GET.get('longitude')  # Długość geograficzna użytkownika
    nearby_stations = []

    # Obsługa wyszukiwania po kodzie pocztowym
    if postal_code:
        stations = list(GasStation.objects.filter(postal_code=postal_code))

        if len(stations) < 10:
            # Pobierz współrzędne dla kodu pocztowego
            try:
                postal_entry = PostalCode.objects.get(zip_code=postal_code)
                lat, lon = postal_entry.latitude, postal_entry.longitude
            except PostalCode.DoesNotExist:
                lat, lon = None, None

            # Jeśli mamy współrzędne, szukaj dodatkowych stacji
            if lat is not None and lon is not None:
                additional_stations = []
                all_stations = GasStation.objects.exclude(postal_code=postal_code)

                for station in all_stations:
                    if station.latitude and station.longitude:
                        distance = calculate_distance(lat, lon, station.latitude, station.longitude)
                        additional_stations.append((station, distance))

                # Posortuj według odległości i dodaj brakujące stacje
                additional_stations = sorted(additional_stations, key=lambda x: x[1])
                stations.extend([s[0] for s in additional_stations[:10 - len(stations)]])

    # Obsługa wyszukiwania po lokalizacji użytkownika
    if latitude and longitude:
        latitude, longitude = float(latitude), float(longitude)
        all_stations = GasStation.objects.all()

        for station in all_stations:
            if station.latitude and station.longitude:
                distance = calculate_distance(latitude, longitude, station.latitude, station.longitude)
                nearby_stations.append((station, distance))

        # Posortuj według odległości
        nearby_stations = sorted(nearby_stations, key=lambda x: x[1])[:5]  # Max 5 najbliższych

    # Pobierz polecane stacje (losowe 5)
    all_stations = list(GasStation.objects.all())
    recommended_stations = random.sample(all_stations, min(len(all_stations), 5))

    return render(request, 'search.html', {
        'stations': stations,
        'postal_code': postal_code,
        'recommended_stations': recommended_stations,  # Polecane stacje
        'nearby_stations': [station[0] for station in nearby_stations],  # Najbliższe stacje
    })