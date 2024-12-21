
from django.shortcuts import render
from stations.models import Points
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

def weekly_ranking(request):
    # Pobierz początek bieżącego tygodnia
    today = now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    ranking = Points.objects.filter(date__gte=start_of_week) \
                  .values('user__username', 'user__id') \
                  .annotate(total_points=Sum('points')) \
                  .order_by('-total_points')[:10]

    # Sprawdzamy, czy ranking zwrócił jakieś dane
    if ranking:
        print(ranking)  # Możesz dodać to do logów, żeby sprawdzić wynik zapytania

    return render(request, 'ranking.html', {'ranking': ranking})
