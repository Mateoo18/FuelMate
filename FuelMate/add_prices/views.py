
import googlemaps
from django.shortcuts import render
from .models import Gas_Stations,Price_history
from django.conf import settings
import os
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse


API_KEY = os.getenv("API_KEY_GOOGLE")


client = googlemaps.Client(key=API_KEY)


def get_location():
    try:
        result = client.geolocate(consider_ip=True)
        location = result.get("location")
        if location:
            lat = location.get("lat")
            lng = location.get("lng")
            return lat, lng
    except googlemaps.exceptions.ApiError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def nearest_stations(request):
    stations = []
    error = None

    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            # Filtracja najbliższych stacji
            stations = Gas_Stations.objects.raw(
                'SELECT *, (6371 * acos(cos(radians(%s)) * cos(radians("latitude")) * '
                'cos(radians("longitude") - radians(%s)) + sin(radians(%s)) * sin(radians("latitude")))) AS distance '
                'FROM "Gas_Stations" ORDER BY distance LIMIT 5', [latitude, longitude, latitude]
            )
        else:
            error = 'Nie można pobrać lokalizacji.'

    return render(request, 'nearest_stations_to_add_price.html', {'stations': stations, 'error': error})

def station_details(request, station_id):
    station = get_object_or_404(Gas_Stations, pk=station_id)
    if request.method == "POST":
        new_price = request.POST.get("price")
        station.price = new_price
        station.save()
        return redirect('nearest_stations')

    return render(request, 'station_details.html', {'station': station})

def report_incident(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        # Tutaj można zapisać komentarz w modelu incydentu lub wywołać akcję
        print("Zgłoszono incydent:", comment)
        return HttpResponseRedirect(reverse('nearest_gas_stations'))
    return HttpResponseRedirect(reverse('nearest_gas_stations'))

