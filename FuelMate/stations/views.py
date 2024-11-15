from django.contrib.auth import login
from django.shortcuts import render
from .models import Fuel, Gas_Stations, Roles, Users, Notifications, Report, Station_Rev, Promotion, Favorite_Station, \
    Price_history, Station_Fuel
from django.contrib.auth.decorators import login_required

@login_required
def fuel_list(request):
    fuels = Fuel.objects.all()
    return render(request, 'DateBase_Test/fuel_list.html', {'fuels': fuels})
def home(request):
    return render(request, 'DateBase_Test/default_page.html')

@login_required
def gas_station_list(request):
    gas_stations = Gas_Stations.objects.all()
    return render(request, 'DateBase_Test/gas_station_list.html', {'gas_stations': gas_stations})

@login_required
def role_list(request):
    roles = Roles.objects.all()
    return render(request, 'DateBase_Test/role_list.html', {'roles': roles})
@login_required
def user_list(request):
    auth_users = Users.objects.all()
    return render(request, 'DateBase_Test/user_list.html', {'auth_users': auth_users})
@login_required
def notification_list(request):
    notifications = Notifications.objects.select_related('User_Id', 'Station_Id', 'Fuel_Id').all()
    return render(request, 'DateBase_Test/notification_list.html', {'notifications': notifications})
@login_required
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'DateBase_Test/report_list.html', {'reports': reports})
@login_required
def station_rev_list(request):
    station_revs = Station_Rev.objects.all()
    return render(request, 'DateBase_Test/station_rev_list.html', {'station_revs': station_revs})
@login_required
def promotion_list(request):
    promotions = Promotion.objects.all()
    return render(request, 'DateBase_Test/promotion_list.html', {'promotions': promotions})
@login_required
def favorite_station_list(request):
    favorite_stations = Favorite_Station.objects.all()
    return render(request, 'DateBase_Test/favorite_station_list.html', {'favorite_stations': favorite_stations})
@login_required
def price_history_list(request):
    price_histories = Price_history.objects.all()
    return render(request, 'DateBase_Test/price_history_list.html', {'price_histories': price_histories})
@login_required
def station_fuel_list(request):
    station_fuels = Station_Fuel.objects.all()
    return render(request, 'DateBase_Test/station_fuel_list.html', {'station_fuels': station_fuels})
