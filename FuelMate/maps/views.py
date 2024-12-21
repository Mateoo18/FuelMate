from django.http import JsonResponse
from stations.models import GasStations
from django.shortcuts import render

def gas_stations_list(request):
    # Pobranie wszystkich stacji paliw
    stations = GasStations.objects.all()

    # Serializacja danych do formatu JSON
    data = list(stations.values(
        "Name", "Address", "City", "postal_code", "Phone", "Latitude", "Longitude","Station_Id"
    ))

    return JsonResponse(data, safe=False)
def tomtom_map(request):
    return render(request, 'maps/map.html')