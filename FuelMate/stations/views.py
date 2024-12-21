
from .models import Fuel, GasStations, Roles, Users, Notifications, Report, StationRev, Promotion, FavoriteStation, \
    PriceHistory, StationFuel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from .models import GasStations, StationFuel, Fuel
import random
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import GasStations
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
@login_required
def fuel_list(request):
    fuels = Fuel.objects.all()
    return render(request, 'DateBase_Test/fuel_list.html', {'fuels': fuels})
def home(request):
    return render(request, 'DateBase_Test/default_page.html')

@login_required
def gas_station_list(request):
    gas_stations = GasStations.objects.all()
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
    station_revs = StationRev.objects.all()
    return render(request, 'DateBase_Test/station_rev_list.html', {'station_revs': station_revs})
@login_required
def promotion_list(request):
    promotions = Promotion.objects.all()
    return render(request, 'DateBase_Test/promotion_list.html', {'promotions': promotions})
@login_required
def favorite_station_list(request):
    favorite_stations = FavoriteStation.objects.all()
    return render(request, 'DateBase_Test/favorite_station_list.html', {'favorite_stations': favorite_stations})
@login_required
def price_history_list(request):
    price_histories = PriceHistory.objects.all()
    return render(request, 'DateBase_Test/price_history_list.html', {'price_histories': price_histories})
@login_required
def station_fuel_list(request):
    station_fuels = StationFuel.objects.all()
    return render(request, 'DateBase_Test/station_fuel_list.html', {'station_fuels': station_fuels})

@login_required
def DataBase_Test(request):
    return render(request, 'D')



def station_details_ajax(request, station_id):
    print("station")

    station = get_object_or_404(GasStations, Station_Id=station_id)
    print(station)
    html_content = render(request, "DateBase_Test/station_details_partia.html", {'station': station}).content
    return HttpResponse(html_content, content_type='text/html')

