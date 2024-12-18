from django.shortcuts import render
from django.shortcuts import render
from stations.models import Users, FavoriteStation, GasStations,Pricehistory,Fuel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from datetime import datetime, time
# Create your views here.


@login_required  # Ensures the user must be logged in
def price_history(request):

    stations = GasStations.objects.all()
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        if station_id is None:
            messages.error(request, "Nie wybrano stacji.")
            return render(request, 'list_price.html', {'stations': stations})

        station = GasStations.objects.get(Station_Id=station_id)
        print(station)
        history_object = Pricehistory.objects.filter(Station_Id=station.Station_Id)
        print(history_object)
        fuel_prices = {
            1: [],  # PB95
            2: [],  # PB98
            3: [],  # Diesel
            4: [],  # LPG
            5: [],  # Elektryczne
        }

        for ele in history_object:
            fuel_id = ele.Fuel_Id
            fuel_name = fuel_id.fuel_id

            print(fuel_name)


            if fuel_name in fuel_prices:

                if isinstance(ele.Date, datetime):
                    date_with_time = ele.Date
                else:
                    date_with_time = datetime.combine(ele.Date, time(16, 19))


                fuel_prices[fuel_name].append({"price": ele.Price, "date": date_with_time})


        print(fuel_prices)


        return render(request, 'station_details_history.html', {'station': station, 'history_object': history_object,'fuel_prices': fuel_prices,})





    return render(request, 'list_price.html', {'stations': stations})


@login_required
def station_details(request, station_name):
    return render(request, 'station_details.html',)