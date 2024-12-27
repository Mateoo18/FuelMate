from gc import get_objects

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from datetime import timedelta
from django.utils.timezone import now
from stations.models import Users, FavoriteStation, GasStations,PriceHistory,Fuel,Complain,Warning,StationFuel
from collections import defaultdict

from stations.models import Users, FavoriteStation, GasStations,PriceHistory,Fuel,Complain,StationFuel,RecommendStations

from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils.timezone import now

current_time = now()
@login_required
def admin_dashboard(request):
    # Sprawdzamy, czy użytkownik ma uprawnienia administratora
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz dostępu do tej strony.")

    # Pobieramy wszystkie zgłoszenia z tabeli `Reports`
    complain= Complain.objects.all()
    detect_price_anomalies()
    warnings = Warning.objects.filter(points__gte=1)  # Ostrzeżenia do wyświetlenia
    user_points = Warning.objects.values('user').annotate(total_points=Sum('points'))

    # Krytyczni użytkownicy (≥ 3 punkty)
    critical_users = []
    for user_data in user_points:
        if user_data['total_points'] >= 3:
            critical_user = {
                "user": Users.objects.get(pk=user_data['user']),
                "total_points": user_data['total_points']
            }
            critical_users.append(critical_user)

    # Przekazujemy dane do szablonu
    return render(request, 'admin_panel/admin_dashboard.html', {
        'complain': complain,
        'warnings': warnings,
        'critical_users': critical_users
    })


@login_required
def delete_prices(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Nie masz dostępu do tej strony.")

    stations = GasStations.objects.all()
    price_history_records = None

    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        station_id = request.POST.get('station_id')

        if record_id:
            # Usunięcie wybranego rekordu
            try:
                record = get_object_or_404(PriceHistory, pk=record_id)
                record.delete()
                messages.success(request, "Rekord został usunięty.")
            except Exception as e:
                messages.error(request, f"Błąd podczas usuwania rekordu: {e}")
        elif station_id:
            # Wyświetlenie rekordów dla wybranej stacji
            price_history_records = PriceHistory.objects.filter(Station_Id=station_id)

    return render(request, 'delete_prices.html', {
        'stations': stations,
        'price_history_records': price_history_records,
    })

from django.db.models import Sum

def detect_price_anomalies():
    print("Rozpoczęcie analizy anomalii cenowych...")
def refresh_stations(request):
    stations = StationFuel.objects.all()
    cheapest_fuels = {}

    for station in stations:
        if station.Price > 0:
            fuel_id = station.Fuel_Id

            if fuel_id not in cheapest_fuels or station.Price < cheapest_fuels[fuel_id]['price']:
                cheapest_fuels[fuel_id] = {
                    'station': station,
                    'price': station.Price
                }
    print(cheapest_fuels)
    RecommendStations.objects.all().delete()
    for fuel_id, data in cheapest_fuels.items():
        station = data['station']
        RecommendStations.objects.create(
            station_id=station.Station_Id,
            fuel_id=fuel_id,
        )

    return render(request, 'admin_panel/admin_dashboard.html')

    # Pobranie wszystkich cen z ostatnich X dni (np. 1 dzień)
    prices = PriceHistory.objects.filter(Date__gte=now() - timedelta(days=1))
    print(f"Liczba pobranych rekordów: {prices.count()}")

    # Grupowanie cen według stacji i paliwa
    grouped_prices = defaultdict(list)
    for price in prices:
        key = (price.Station_Id_id, price.Fuel_Id_id)
        grouped_prices[key].append(price)

    print(f"Liczba grup do analizy: {len(grouped_prices)}")

    # Analiza każdej grupy
    for (station_id, fuel_id), price_records in grouped_prices.items():
        price_records.sort(key=lambda x: x.Date)

        for i in range(len(price_records)):
            group = [price_records[i]]  # Pierwszy rekord w grupie
            for j in range(i + 1, len(price_records)):
                if price_records[j].Date - price_records[i].Date <= timedelta(minutes=5):
                    group.append(price_records[j])
                else:
                    break

            if len(group) >= 3:
                unique_prices = set(p.Price for p in group)
                if len(unique_prices) > 1:
                    # Najczęstsza cena w grupie
                    most_common_price = max(unique_prices, key=lambda p: len([pr for pr in group if pr.Price == p]))

                    for price in group:
                        if price.Price != most_common_price:
                            # Sprawdź, czy dla tego użytkownika istnieje już ostrzeżenie
                            existing_warning = Warning.objects.filter(
                                user=price.user,
                                station=price.Station_Id,
                                reason="Wprowadzono cenę różniącą się od innych użytkowników w krótkim czasie",
                                timestamp__gte=now() - timedelta(days=1)
                            ).exists()

                            if not existing_warning:
                                print(
                                    f"Wykryto anomalię: Użytkownik {price.user.username if price.user else 'Anonim'}, Cena {price.Price}")
                                Warning.objects.create(
                                    user=price.user,
                                    station=price.Station_Id,
                                    points=1,
                                    reason="Wprowadzono cenę różniącą się od innych użytkowników w krótkim czasie"
                                )

    print("Analiza anomalii zakończona.")