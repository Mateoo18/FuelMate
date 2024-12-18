
import googlemaps
from django.shortcuts import render
from django.conf import settings
import os
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils import timezone
from .models import Gas_Stations, Fuel, StationFuel, PriceHistory, Points,Complain
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


from django.contrib.auth.models import User

def nearest_stations(request):
    stations = []
    error = None

    if request.user.is_superuser:
        # Superuser - pokaż wszystkie stacje
        stations = Gas_Stations.objects.all()
    elif request.method == 'POST':
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



def station_to_list(request, station_id):
    station = get_object_or_404(Gas_Stations, pk=station_id)
    if request.method == "POST":
        new_price = request.POST.get("price")
        station.price = new_price
        station.save()
        return redirect('update_prices')

    return render(request, 'station_details.html', {'station': station})

def report_incident(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        # Tutaj można zapisać komentarz w modelu incydentu lub wywołać akcję
        print("Zgłoszono incydent:", comment)
        return HttpResponseRedirect(reverse('nearest_gas_stations'))
    return HttpResponseRedirect(reverse('nearest_gas_stations'))

@login_required
def update_prices(request, station_id):
    station = get_object_or_404(Gas_Stations, id_stations=station_id)
    fuels = Fuel.objects.all()

    if request.method == "POST":
        missing_prices = []
        for fuel in fuels:
            new_price = request.POST.get(f"price_{fuel.Fuel_Id}")
            if not new_price:
                missing_prices.append(fuel.Name)

        if missing_prices:
            missing_fuels = ", ".join(missing_prices)
            messages.warning(request, f"Musisz uzupełnić ceny dla następujących paliw: {missing_fuels}.")
            return redirect('add_prices:update_prices', station_id=station_id)

        for fuel in fuels:
            new_price = request.POST.get(f"price_{fuel.Fuel_Id}")
            if new_price:
                try:
                    new_price = float(new_price)
                    station_fuel = StationFuel.objects.filter(station=station, fuel=fuel).first()
                    if station_fuel:
                        station_fuel.Price = new_price
                        station_fuel.Update_Date = timezone.now()
                        station_fuel.user = request.user
                        station_fuel.save()
                    else:
                        StationFuel.objects.create(
                            station=station,
                            fuel=fuel,
                            Price=new_price,
                            Update_Date=timezone.now(),
                            user=request.user
                        )
                    PriceHistory.objects.create(
                        station=station,
                        fuel=fuel,
                        price=new_price,
                        change_date=timezone.now()
                    )
                except ValueError:
                    messages.error(request, f"Nieprawidłowa wartość ceny dla paliwa {fuel.Name}.")
                    return redirect('add_prices:update_prices', station_id=station_id)

        Points.objects.create(
            user=request.user,
            points=1,
            date=timezone.now()
        )
        messages.success(request, "Ceny zostały zaktualizowane, a punkty zostały dodane.")
        return redirect('add_prices:nearest_stations')

    # Serializuj komunikaty Django do JSON
    serialized_messages = [
        {"message": msg.message, "tags": msg.tags} for msg in get_messages(request)
    ]

    context = {
        'station': station,
        'fuels': fuels,
        'serialized_messages': serialized_messages  # Dodaj serializowane komunikaty
    }
    return render(request, 'station_details.html', context)


@login_required
def report_complain(request, station_id):
    subject = f"Gratulacje! Zająłeś 1 miejsce"
    message = f"Gratulacje! Zdobyłeś 1 miejsce w rankingu tygodniowym. Nagroda: 1 zł."
    from_email = "mateusz.nowak.076@gmail.com"
    email="mateusz.nowak.203@gmail.com"
    try:
        send_mail(subject, message, from_email, email, fail_silently=False)
        print(f"E-mail wysłany do {email}")
    except Exception as e:
        print(f"Błąd wysyłania e-maila do {email}: {e}")



    station = get_object_or_404(Gas_Stations, id_stations=station_id)

    if request.method == "POST":
        complain_text = request.POST.get("complain_text")
        if not complain_text:
            messages.warning(request, "Treść zażalenia nie może być pusta.")
            return redirect('add_prices:station_details',  id_stations=station_id)

        # Zapisanie zażalenia w bazie danych
        Complain.objects.create(
            user=request.user,
            station=station,
            text=complain_text
        )

        messages.success(request, "Zażalenie zostało zgłoszone.")
        return redirect('add_prices:nearest_stations')