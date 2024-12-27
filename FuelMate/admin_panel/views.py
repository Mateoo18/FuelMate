from gc import get_objects

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from stations.models import Users, FavoriteStation, GasStations,PriceHistory,Fuel,Complain,StationFuel,RecommendStations

from django.contrib import messages
from django.contrib.messages import get_messages

@login_required
def admin_dashboard(request):
    # Sprawdzamy, czy użytkownik ma uprawnienia administratora
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz dostępu do tej strony.")

    # Pobieramy wszystkie zgłoszenia z tabeli `Reports`
    complain= Complain.objects.all()

    # Przekazujemy dane do szablonu
    return render(request, 'admin_panel/admin_dashboard.html', {
        'complain': complain,
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
