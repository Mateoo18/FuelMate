from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Avg, F, ExpressionWrapper, FloatField
from stations.models import Users, FavoriteStation, GasStations,PriceHistory,Fuel,Complain

from django.contrib import messages
from django.contrib.messages import get_messages

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz dostępu do tej strony.")
    complain = Complain.objects.all()
    average_prices = (
        PriceHistory.objects
        .values('Fuel_Id')
        .annotate(avg_price=Avg('Price'))
    )
    avg_price_map = {item['Fuel_Id']: item['avg_price'] for item in average_prices}
    anomalies = (
        PriceHistory.objects
        .annotate(
            avg_price=ExpressionWrapper(
                F('Fuel_Id'),
                output_field=FloatField()
            ),
            deviation=ExpressionWrapper(
                F('Price') - F('avg_price'),
                output_field=FloatField()
            )
        )
        .filter(
            deviation__gt=1.1 * F('avg_price')
        )
        .select_related('Station_Id', 'Fuel_Id')
    )
    return render(request, 'admin_panel/admin_dashboard.html', {
        'complain': complain,
        'anomalies': anomalies,
    })


@login_required
def delete_prices(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Nie masz dostępu do tej strony.")

    stations = GasStations.objects.all()
    price_history_records = None

    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        station_id = request.POST.get('station_id')

        if record_id:
            # Usunięcie wybranego rekordu
            try:
                record = get_object_or_404(PriceHistory, pk=record_id)
                record.delete()
                messages.success(request, "Rekord został usunięty.")
            except Exception as e:
                messages.error(request, f"Błąd podczas usuwania rekordu: {e}")
        elif station_id:
            # Wyświetlenie rekordów dla wybranej stacji
            price_history_records = PriceHistory.objects.filter(Station_Id=station_id)

    return render(request, 'delete_prices.html', {
        'stations': stations,
        'price_history_records': price_history_records,
    })

