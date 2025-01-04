# accounts/views.py
import random
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import requests
from django.db import connection

from FuelMate.settings import API_KEY_TOM
from stations.models import GasStations, PostalCode,StationRating
import os
from django.contrib.auth.decorators import login_required
from math import radians, cos, sin, sqrt, atan2
from django.shortcuts import render
from django.views import View
API_KEY = os.getenv("API_KEY_TOM_TOM")

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Promień Ziemi w kilometrach
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def calcuate_stations_score(stations, time_in_minutes, distance,max_distance=1000, min_price=4.2, max_price=6.5,max_time=1000,):


    if distance is None:
        distance = 0  # Możesz ustawić domyślną wartość, np. 0 km

    if time_in_minutes is None:
        time_in_minutes = 0

    rank = ranging_get(stations, stations)
    rating = 0
    quantity = 0
    if len(rank) > 0:
        rating = rank[0].rating
        print(rating)
        quantity = rank[0].quantity
        print(quantity)

    if rating is None:
        rating = 0
    if quantity is None:
        quantity = 0

    virtual_reviews = 5
    default_rating = 4.0

    if quantity == 0:
        adjusted_rating = default_rating
    else:
        adjusted_rating = (rating * quantity + default_rating * virtual_reviews) / (quantity + virtual_reviews)

    fuel_price = random.uniform(min_price, max_price)

    distance_score = max(0.0, min(5.0, 5.0 - (distance / max_distance) * 5))


    time_score = max(0.0, min(5.0, 5.0 - (time_in_minutes / max_time) * 5))


    price_score = max(0.0, min(5.0, 5.0 - (
                (fuel_price - min_price) / (max_price - min_price)) * 5))

    # Wagi dla każdego kryterium
    distance_weight = 0.05
    time_weight = 0.5
    price_weight = 0.44
    rank_weight = 0.1


    score = (distance_score * distance_weight) + (time_score * time_weight) + (price_score * price_weight) + (adjusted_rating * rank_weight)
    score = max(0.0, min(5.0, score))
    return score


def time_to_drive_tomtom(start_lat, start_lon, end_lat, end_lon):
    """Funkcja do obliczania czasu podróży i odległości za pomocą API TomTom"""
    url = f'https://api.tomtom.com/routing/1/calculateRoute/{start_lat},{start_lon}%3A{end_lat},{end_lon}/json?language=pl-PL&computeBestOrder=true&key={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Sprawdzamy, czy odpowiedź jest poprawna
        data = response.json()
        sleep(0.3)

        # Sprawdzamy, czy odpowiedź zawiera dane
        if 'routes' in data and len(data['routes']) > 0:
            route = data['routes'][0]['summary']
            length_in_meters = route.get('lengthInMeters', 0)
            travel_time_in_seconds = route.get('travelTimeInSeconds', 0)

            if 'trafficDelayInSeconds' in route:
                travel_time_in_seconds += route['trafficDelayInSeconds']

            if length_in_meters is not None or travel_time_in_seconds is not None:
                 return travel_time_in_seconds, length_in_meters




    except requests.exceptions.RequestException as e:
        print(f'Błąd połączenia z API TomTom: {e}')

    # Jeśli wystąpił błąd, zwracamy None, None
    return None, None

def list_returned_stations(station, latitude, longitude):
    station_obj = station
    travel_time, distance = time_to_drive_tomtom(latitude, longitude, station_obj.Latitude,
                                                                        station_obj.Longitude)
    if travel_time is None or distance is None:
        print(f'Nie udało się obliczyć czasu podróży dla stacji {station_obj.Name}')
    else :
        print(f'{station_obj.Name}: {travel_time} sekund, {distance} metrów')
        return travel_time, distance



def search_stations_by_postal_code(request):
    postal_code = request.GET.get('postal_code', '').strip()
    stations = GasStations.objects.filter(address__icontains=postal_code)
    return render(request, 'search.html', {'stations': stations, 'postal_code': postal_code})

def all_stations_view(request):
    stations = GasStations.objects.all()
    return render(request, 'search.html', {'stations': stations})

def ranging_get(request,station):
    station_id = station.Station_Id
    rank = StationRating.objects.filter(id_stations=station_id)
    return rank




@login_required
def logged_in_view(request):
    stations = []
    postal_code = request.GET.get('postal_code', '').strip()
    latitude = request.GET.get('latitude')# Szerokość geograficzna użytkownika
    longitude = request.GET.get('longitude')  # Długość geograficzna użytkownika
    nearby_stations = []
    recommended_stations = []
    recommended_stations_re = []

    # Obsługa wyszukiwania po kodzie pocztowym
    if postal_code:
        stations = list(GasStations.objects.filter(postal_code=postal_code))

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
                all_stations = GasStations.objects.exclude(postal_code=postal_code)

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
        all_stations = GasStations.objects.all()

        for station in all_stations:
            if station.Latitude and station.Longitude:
                distance = calculate_distance(latitude, longitude, station.Latitude, station.Longitude)
                  # Symulacja opóźnienia
                nearby_stations.append((station, distance))

        # Posortuj według odległości
        recommended_stations = sorted(nearby_stations, key=lambda x: x[1])[:5]
        nearby_stations = sorted(nearby_stations, key=lambda x: x[1])[:5]  # Max 5 najbliższych
        #print(recommended_stations)

        for station in recommended_stations:
            travel_time,distance = list_returned_stations(station[0], latitude, longitude)
            score = calcuate_stations_score(station[0], travel_time/60, distance)
            recommended_stations_re.append((station[0], round(travel_time/60), round(distance/1000,2),round(score,2)))
        #print(recommended_stations_re)





    return render(request, 'search.html', {
        'stations': stations,
        'postal_code': postal_code,
        'recommended_stations': sorted(recommended_stations_re, key=lambda x: x[3], reverse=True),  # Rekomendowane stacje
        'nearby_stations': [station[0] for station in nearby_stations],  # Najbliższe stacje
        'api_key': API_KEY_TOM
    })


def get_stations_from_tomtom(query, user_latitude=None, user_longitude=None):
    api_key = os.getenv("GEFJGFwsJTFCL8APYN0w48ks3eweIIAk")  # Użyj zmiennej środowiskowej lub klucza w ustawieniach
    url = f"https://api.tomtom.com/search/2/search/{query}.json"
    params = {
        'key': api_key,
        'typeahead': 'true',
        'countrySet': 'PL',
        'limit': '5',
        'language': 'pl-PL'
    }

    # Dodaj współrzędne użytkownika, jeśli są dostępne
    if user_latitude and user_longitude:
        params['lat'] = user_latitude
        params['lon'] = user_longitude

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Jeśli status to 4xx lub 5xx, zgłoś wyjątek
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from TomTom API: {e}")
        return []


def search_stations(request):
    search_query = request.GET.get('search', '')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    user_latitude = float(latitude) if latitude else None
    user_longitude = float(longitude) if longitude else None

    stations = []
    nearby_stations = []

    if search_query:
        # Pobieramy stacje paliw na podstawie zapytania użytkownika
        stations = get_stations_from_tomtom(search_query, user_latitude, user_longitude)

    if user_latitude and user_longitude:
        # Można dodać logikę dla stacji w pobliżu użytkownika, jeśli nie jest podane wyszukiwanie
        nearby_stations = get_stations_from_tomtom('', user_latitude, user_longitude)

    # W przypadku zwrócenia wyniku do frontend
    return render(request, 'search.html', {
        'stations': stations,
        'nearby_stations': nearby_stations,
    })

def some_view(request):
    # Przekazanie API_KEY do szablonu HTML
    return render(request, 'search.html', {'api_key': API_KEY_TOM})

# Widok dla strony "Zmiany w cenach paliw"
class NewsFuelPricesView(View):
    def get(self, request):
        return render(request, 'fuel_prices.html')

# Widok dla strony "Jak wybrać najtańszą stację paliw"
class NewsCheapestStationView(View):
    def get(self, request):
        return render(request, 'cheapest_station.html')

# Widok dla strony "Bezpieczeństwo na stacjach paliw"
class NewsSafetyStationView(View):
    def get(self, request):
        return render(request, 'safety_station.html')

# Widok dla strony "Zmiany w regulacjach dotyczących stacji paliw"
class NewsRegulationsStationView(View):
    def get(self, request):
        return render(request, 'regulations_station.html')

# Widok dla strony "Nowoczesne technologie w stacjach paliw"
class NewsTechnologyStationView(View):
    def get(self, request):
        return render(request, 'technology_station.html')