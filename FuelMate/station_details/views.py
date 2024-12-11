from django.shortcuts import render
from urllib3 import request
from django.shortcuts import render, get_object_or_404
from stations.models import Gas_Stations,Station_Fuel,Price_history
from datetime import datetime, time
import json

def station_details(request, station_id):
    station = get_object_or_404(Gas_Stations, Station_Id=station_id)

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

    return render(request, 'deatails.html', {'station': station, 'fuel_prices_now': fuel_prices, 'fuel_prices_old': fuel_prices2,'fuel_prices_json': fuel_prices_json_str})

