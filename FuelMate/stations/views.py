from django.shortcuts import render
from .models import Fuel,Gas_Stations,Roles,Users,Notifications,Report,Station_Rev,Promotion,Favorite_Station,Price_history,Station_Fuel

def fuel_list(request):
    fuels = Fuel.objects.all()
    return render(request, 'fuel_list.html', {'fuels': fuels})

def home(request):
    return render(request, 'default_page.html')

def gas_station_list(request):
    gas_stations = Gas_Stations.objects.all()
    return render(request, 'gas_station_list.html', {'gas_stations': gas_stations})

def role_list(request):
    roles = Roles.objects.all()
    return render(request, 'role_list.html', {'roles': roles})

def user_list(request):
    users = Users.objects.all()
    return render(request, 'user_list.html', {'users': users})

def notification_list(request):
    notifications = Notifications.objects.all()
    return render(request, 'notification_list.html', {'notifications': notifications})

def report_list(request):
    reports = Report.objects.all()
    return render(request, 'report_list.html', {'reports': reports})

def station_rev_list(request):
    station_revs = Station_Rev.objects.all()
    return render(request, 'station_rev_list.html', {'station_revs': station_revs})

def promotion_list(request):
    promotions = Promotion.objects.all()
    return render(request, 'promotion_list.html', {'promotions': promotions})

def favorite_station_list(request):
    favorite_stations = Favorite_Station.objects.all()
    return render(request, 'favorite_station_list.html', {'favorite_stations': favorite_stations})

def price_history_list(request):
    price_histories = Price_history.objects.all()
    return render(request, 'price_history_list.html', {'price_histories': price_histories})

def station_fuel_list(request):
    station_fuels = Station_Fuel.objects.all()
    return render(request, 'station_fuel_list.html', {'station_fuels': station_fuels})
