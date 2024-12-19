
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

    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            # Filtracja najbliższych stacji
            stations = GasStations.objects.raw(
                'SELECT *, (6371 * acos(cos(radians(%s)) * cos(radians("latitude")) * '
                'cos(radians("longitude") - radians(%s)) + sin(radians(%s)) * sin(radians("latitude")))) AS distance '
                'FROM "Gas_Stations" ORDER BY distance LIMIT 5', [latitude, longitude, latitude]
            )
        else:
            error = 'Nie można pobrać lokalizacji.'
    serialized_messages = [
        {"message": msg.message, "tags": msg.tags} for msg in get_messages(request)
    ]
    print("Stacje: ",stations)
    return render(request, 'nearest_stations_to_add_price.html', {'stations': stations,'serialized_messages': serialized_messages, 'error': error})

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
    # Pobranie stacji paliw i listy paliw
    station = get_object_or_404(GasStations, Station_Id=Station_Id)
    fuels = Fuel.objects.all()

    if request.method == "POST":
        missing_prices = []

        # Sprawdzenie brakujących cen
        for fuel in fuels:
            status = request.POST.get(f"status_{fuel.fuel_id}")
            new_price = request.POST.get(f"price_{fuel.fuel_id}")

            if status == "add" and not new_price:
                missing_prices.append(fuel.Name)

        if missing_prices:
            missing_fuels = ", ".join(missing_prices)
            messages.warning(request, f"Musisz uzupełnić ceny dla następujących paliw: {missing_fuels}.")
            return redirect('add_prices:update_prices', Station_Id=Station_Id)

        # Aktualizacja cen lub statusów paliw
        for fuel in fuels:
            status = request.POST.get(f"status_{fuel.fuel_id}")
            new_price = request.POST.get(f"price_{fuel.fuel_id}")

            if status == "add" and new_price:
                try:
                    new_price = float(new_price)
                    station_fuel = StationFuel.objects.filter(Station_Id=station, Fuel_Id=fuel).first()
                    if station_fuel:
                        station_fuel.Price = new_price
                        station_fuel.Date = timezone.now()
                        station_fuel.save()
                    else:
                        StationFuel.objects.create(
                            Station_Id=station,
                            Fuel_Id=fuel,
                            Price=new_price,
                            Date=timezone.now()
                        )
                    PriceHistory.objects.create(
                        Station_Id=station,
                        Fuel_Id=fuel,
                        Price=new_price,
                        change_date=timezone.now()
                    )
                except ValueError:
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
    subject = f"Gratulacje! Zająłeś 1 miejsce"
    message = f"Gratulacje! Zdobyłeś 1 miejsce w rankingu tygodniowym. Nagroda: 1 zł."
    from_email = "mateusz.nowak.076@gmail.com"
    email=["mateusz.nowak.203@gmail.com"]
    try:
        send_mail(subject, message, from_email, email, fail_silently=False)
        print(f"E-mail wysłany do {email}")
    except Exception as e:
        print(f"Błąd wysyłania e-maila do {email}: {e}")



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