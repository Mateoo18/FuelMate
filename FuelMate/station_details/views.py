from django.shortcuts import render
from urllib3 import request
from django.shortcuts import render, get_object_or_404
from stations.models import Gas_Stations,Station_Fuel,Price_history,Favorite_Station
from datetime import datetime, time
import json
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
def station_details(request, station_id):
    station = get_object_or_404(Gas_Stations, Station_Id=station_id)

    user = request.user
    user_id = user.id

    def is_favorite_station(user, station_id):
        try:
            favorite_station = Favorite_Station.objects.get(User_Id=user, Station_Id=station_id)
            return True  # Stacja jest ulubiona
        except ObjectDoesNotExist:
            return False
    is_favorite_station(user_id, station_id)

    fuels = Station_Fuel.objects.filter(Station_Id=station_id)

    fuel_prices = {
        "95": [],
        "98": [],
        "Diesel": [],
        "CNG": [],
        "Elektryczny": [],
    }

    for fuel in fuels:
        fuel_name = fuel.Fuel_Id.Name
        if fuel_name in fuel_prices:
            fuel_prices[fuel_name].append({"price": fuel.Price, "date": fuel.Date})


    history_object = Price_history.objects.filter(Station_Id=station_id)

    fuel_prices2 = {
        "95": [],
        "98": [],
        "Diesel": [],
        "CNG": [],
        "Elektryczny": [],
    }

    for ele in history_object:
        fuel_id = ele.Fuel_Id
        fuel_name = ele.Fuel_Id.Name
        print(fuel_name)

        if fuel_name in fuel_prices2:

            if isinstance(ele.Date, datetime):
                date_with_time = ele.Date
            else:
                date_with_time = datetime.combine(ele.Date, time(16, 19))

            fuel_prices2[fuel_name].append({"price": ele.Price, "date": date_with_time})

    print(fuel_prices2)

    fuel_prices_json = {
        fuel_type: [
            {'price': float(price['price']), 'date': price['date'].isoformat()}
            for price in prices
        ]
        for fuel_type, prices in fuel_prices2.items()
    }

    fuel_prices_json_str = json.dumps(fuel_prices_json)

    return render(request, 'deatails.html', {'station': station, 'fuel_prices_now': fuel_prices, 'fuel_prices_old': fuel_prices2,'fuel_prices_json': fuel_prices_json_str, 'is_favorite': is_favorite_station(user_id, station_id)})








