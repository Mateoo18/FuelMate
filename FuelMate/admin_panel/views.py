from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from stations.models import Users, Favorite_Station, Gas_Stations,Price_history,Fuel,Report

from django.contrib import messages
from django.contrib.messages import get_messages

@login_required
def admin_dashboard(request):
    # Sprawdzamy, czy użytkownik ma uprawnienia administratora
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz dostępu do tej strony.")

    # Pobieramy wszystkie zgłoszenia z tabeli `Reports`
    reports = Report.objects.all()

    # Przekazujemy dane do szablonu
    return render(request, 'admin_panel/admin_dashboard.html', {
        'reports': reports,
    })


@login_required
def delete_prices(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Nie masz dostępu do tej strony.")

    stations = Gas_Stations.objects.all()
    price_history_records = None

    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        station_id = request.POST.get('station_id')

        if record_id:
            # Usunięcie wybranego rekordu
            try:
                record = get_object_or_404(Price_history, pk=record_id)
                record.delete()
                messages.success(request, "Rekord został usunięty.")
            except Exception as e:
                messages.error(request, f"Błąd podczas usuwania rekordu: {e}")
        elif station_id:
            # Wyświetlenie rekordów dla wybranej stacji
            price_history_records = Price_history.objects.filter(Station_Id=station_id)

    return render(request, 'delete_prices.html', {
        'stations': stations,
        'price_history_records': price_history_records,
    })

