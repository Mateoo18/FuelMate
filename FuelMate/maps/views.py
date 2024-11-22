from django.http import JsonResponse
from .models import Gas_Stations
from django.shortcuts import render

def gas_stations_list(request):
    # Pobranie wszystkich stacji paliw
    stations = Gas_Stations.objects.all()

    # Serializacja danych do formatu JSON
    data = list(stations.values(
        "Name", "Address", "City", "Zip", "Phone", "Latitude", "Longitude"
    ))

    return JsonResponse(data, safe=False)
def tomtom_map(request):
    return render(request, 'maps/map.html')