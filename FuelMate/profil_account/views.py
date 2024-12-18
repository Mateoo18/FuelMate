from django.shortcuts import render
from stations.models import Users, FavoriteStation, GasStations
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from stations.views import favorite_station_list


@login_required
def profile(request):

    user = request.user
    print(user.id)

    try:
        user_info = Users.objects.get(UserId=user.id)
    except Users.DoesNotExist:
        print("chuja")
        user_info = None

    favorite_station_list = []
    favorite_stations = FavoriteStation.objects.filter(User_Id=user_info.UserId)

    for station in favorite_stations:

        station = GasStations.objects.get(Station_Id=station.Station_Id.Station_Id)

        favorite_station_list.append(station)

    return render(request, 'profil_page.html', {'user_info': user_info, 'user': user , 'favorite_station_list': favorite_station_list})

@login_required  # Ensures the user must be logged in
def add_favorite_station(request):

    stations = GasStations.objects.all()
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        if station_id is None:
            messages.error(request, "Nie wybrano stacji.")
            return render(request, 'add_favorite_station.html', {'stations': stations})

        station = GasStations.objects.get(Station_Id=station_id)
        user=request.user
        user_id=Users.objects.get(Username=user.username)


        if not FavoriteStation.objects.filter(User_Id=user_id.UserId, Station_Id=station.Station_Id).exists():
            messages.success(request, "Stacja została dodana do ulubionych.")
            FavoriteStation.objects.create(User_Id=user_id, Station_Id=station)
        else:
            messages.error(request, "Stacja jest juz dodana do ulubionych.")

    return render(request, 'add_favorite_station.html', {'stations': stations})
@login_required
def remove_favorite_station(request):
    user = request.user

    favorite_station_list = []
    favorite_station = FavoriteStation.objects.filter(User_Id=user.id)
    for station in favorite_station:
        station = GasStations.objects.get(Station_Id=station.Station_Id.Station_Id)
        favorite_station_list.append(station)


    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        if station_id is None:
            messages.error(request, "Nie wybrano stacji.")
            return render(request, 'remove_favorite_station.html', {'favorite_station_list': favorite_station_list})


        station = GasStations.objects.get(Station_Id=station_id)
        user_id = Users.objects.get(Username=user.username)


        try:
            favorite_station = FavoriteStation.objects.get(User_Id=user_id.UserId, Station_Id=station.Station_Id)
            favorite_station.delete()
            messages.success(request, "Stacja została usunięta z ulubionych.")
        except FavoriteStation.DoesNotExist:
            messages.error(request, "Stacja nie jest dodana do ulubionych.")

    return render(request, 'remove_favorite_station.html', {'favorite_station_list': favorite_station_list})



