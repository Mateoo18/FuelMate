from sys import exec_prefix

import googlemaps
from django.shortcuts import render
from django.conf import settings
import os
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils import  timezone
from stations.models import GasStations, Fuel, StationFuel, PriceHistory,Points,Complain
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from django.utils import timezone

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
    max_distance_km = 1.5  # Maksymalna odległość w kilometrach

    if request.user.is_superuser:
        # Superuser - pokaż wszystkie stacje
        stations = GasStations.objects.all()
    elif request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            # Filtracja najbliższych stacji z uwzględnieniem maksymalnej odległości
            stations = GasStations.objects.raw(
                '''
                SELECT *, 
                (6371 * acos(
                    cos(radians(%s)) * cos(radians("latitude")) * 
                    cos(radians("longitude") - radians(%s)) + 
                    sin(radians(%s)) * sin(radians("latitude"))
                )) AS distance
                FROM "Gas_Stations"
                WHERE (6371 * acos(
                    cos(radians(%s)) * cos(radians("latitude")) * 
                    cos(radians("longitude") - radians(%s)) + 
                    sin(radians(%s)) * sin(radians("latitude"))
                )) <= %s
                ORDER BY distance
                LIMIT 5
                ''', [latitude, longitude, latitude, latitude, longitude, latitude, max_distance_km]
            )
        else:
            error = 'Nie można pobrać lokalizacji.'
    else:
        error = 'Musisz podać lokalizację, chyba że jesteś administratorem.'

    serialized_messages = [
        {"message": msg.message, "tags": msg.tags} for msg in get_messages(request)
    ]
    return render(request, 'nearest_stations_to_add_price.html', {
        'stations': stations,
        'serialized_messages': serialized_messages,
        'error': error,
        'is_superuser': request.user.is_superuser  # Informacja dla szablonu
    })
def station_to_list(request, Station_Id):
    station = get_object_or_404(GasStations, Station_Id=Station_Id)
    if request.method == "POST":
        new_price = request.POST.get("price")
        # Tutaj trzeba upewnić się, czy jest gdzie zapisać cenę (może dodać pole `price` w GasStations?)
        station.price = new_price
        station.save()
        return redirect('add_prices:nearest_stations')

    return render(request, 'station_details.html', {'station': station})

def report_incident(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        # Tutaj można zapisać komentarz w modelu incydentu lub wywołać akcję
        print("Zgłoszono incydent:", comment)
        return HttpResponseRedirect(reverse('nearest_gas_stations'))
    return HttpResponseRedirect(reverse('nearest_gas_stations'))

@login_required
def update_prices(request, Station_Id):
    print("hello")
    # Pobranie stacji paliw i listy paliw
    station = get_object_or_404(GasStations, Station_Id=Station_Id)
    fuels = Fuel.objects.all()

    if request.method == "POST":
        last_entry = PriceHistory.objects.filter(user=request.user).order_by('-Date').first()
        if last_entry and (timezone.now() - last_entry.Date).total_seconds() < 600:
            # Jeśli ostatni wpis jest młodszy niż 10 minut
            messages.error(request, "Nie możesz dodać ceny ponownie przed upływem 10 minut.")
            return redirect('add_prices:update_prices', Station_Id=Station_Id)

        print("Dane POST:", request.POST)
        print("Zalogowany użytkownik:", request.user)
        missing_prices = []
        minus_prices = []
        MAX_PRICE = 10.0  # Maksymalna dopuszczalna cena paliwa (w zł)

        for fuel in fuels:
            status = request.POST.get(f"status_{fuel.fuel_id}")
            new_price = request.POST.get(f"price_{fuel.fuel_id}")

            # Sprawdzenie poprawności ceny
            if new_price is not None and new_price.strip() != '':
                try:
                    new_price = float(new_price.replace(',', '.'))
                    if new_price <= 0:
                        minus_prices.append(fuel.Name)
                    elif new_price > MAX_PRICE:
                        messages.warning(request,
                                         f"Cena paliwa {fuel.Name} jest zbyt wysoka ({new_price} zł). Maksymalna dopuszczalna cena to {MAX_PRICE} zł.")
                        return redirect('add_prices:update_prices', Station_Id=Station_Id)
                except ValueError:
                    messages.warning(request, f"Podana cena nie jest liczbą: {new_price}.")
                    return redirect('add_prices:update_prices', Station_Id=Station_Id)
            elif status == "add":  # Cena wymagana w trybie 'add', ale brak wartości
                missing_prices.append(fuel.Name)

        # Obsługa błędów cen ujemnych
        if minus_prices:
            minuses_fuel = ", ".join(minus_prices)
            messages.warning(request, f"Ceny paliw nie mogą być mniejsze od zera dla paliw: {minuses_fuel}.")
            return redirect('add_prices:update_prices', Station_Id=Station_Id)

        # Obsługa brakujących cen
        if missing_prices:
            missing_fuels = ", ".join(missing_prices)
            messages.warning(request, f"Musisz uzupełnić ceny dla następujących paliw: {missing_fuels}.")
            return redirect('add_prices:update_prices', Station_Id=Station_Id)

        # Aktualizacja cen lub statusów paliw
        for fuel in fuels:
            status = request.POST.get(f"status_{fuel.fuel_id}")
            new_price = request.POST.get(f"price_{fuel.fuel_id}")
            if new_price is not None:
                new_price = float(new_price.replace(',', '.'))

            if status == "add" and new_price:
                try:
                    new_price = float(new_price)
                    station_fuel = StationFuel.objects.filter(Station_Id=station, Fuel_Id=fuel).first()
                    if station_fuel:
                        station_fuel.Price = new_price
                        station_fuel.Date = timezone.now()
                        station_fuel.user = request.user
                        print("id uzytkownika: ",station_fuel.user)
                        station_fuel.save()
                        print(f"Zaktualizowano cenę: {new_price} dla paliwa {fuel.Name}")
                    else:
                        StationFuel.objects.create(
                            Station_Id=station,
                            Fuel_Id=fuel,
                            Price=new_price,
                            Date=timezone.now(),
                            user = request.user
                        )
                        print(f"Utworzono nową cenę: {new_price} dla paliwa {fuel.Name}")
                    PriceHistory.objects.create(
                        Station_Id=station,
                        Fuel_Id=fuel,
                        Price=new_price,
                        Date=timezone.now(),
                        user = request.user
                    )
                    print(f"historia dla: {request.user} dla paliwa {fuel.Name}")
                except ValueError:
                    print("????")
                    if(new_price<=0):
                        messages.error(request, f"Ujemna wartość ceny dla paliwa {fuel.Name}.")
                    else:
                        messages.error(request, f"Nieprawidłowa wartość ceny dla paliwa {fuel.Name}.")
                    return redirect('add_prices:update_prices', Station_Id=Station_Id)


            elif status == "none":
                # Ustawienie ceny na 0, jeśli paliwa chwilowo brak
                StationFuel.objects.update_or_create(
                    Station_Id=station,
                    Fuel_Id=fuel,
                    defaults={'Price': 0, 'Date': timezone.now()}
                )

            elif status == "not_available":
                # Ustawienie ceny na -1, jeśli paliwo nie jest dostępne na tej stacji
                StationFuel.objects.update_or_create(
                    Station_Id=station,
                    Fuel_Id=fuel,
                    defaults={'Price': -1, 'Date': timezone.now()}
                )

        # Dodanie punktów za zaktualizowanie cen
        Points.objects.create(
            user=request.user,
            points=1,
            date=timezone.now()
        )
        messages.success(request, "Ceny zostały zaktualizowane, a punkty zostały dodane.")
        return redirect('add_prices:nearest_stations')

    context = {
        'station': station,
        'fuels': fuels,
    }
    return render(request, 'station_details.html', context)



@login_required
def report_complain(request, Station_Id):
    station = get_object_or_404(GasStations, Station_Id=Station_Id)

    if request.method == "POST":
        complain_text = request.POST.get("complain_text")
        if not complain_text:
            messages.warning(request, "Treść zażalenia nie może być pusta.")
            return redirect('add_prices:station_details', Station_Id=Station_Id)

        # Zapisanie zażalenia w bazie danych
        Complain.objects.create(
            user=request.user,
            station=station,
            text=complain_text
        )

        messages.success(request, "Zażalenie zostało zgłoszone.")
        return redirect('add_prices:nearest_stations')