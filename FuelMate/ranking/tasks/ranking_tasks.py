from django.utils.timezone import now
from datetime import timedelta
from .email_tasks import send_reward_email
from django.db.models import Sum


def process_weekly_ranking():
    from ..models import Points
    today = now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Sumowanie punktów i generowanie rankingu
    if today >= start_of_week:
        # Przetwarzamy ranking
        ranking = Points.objects.filter(date__gte=start_of_week).values(
            'user__id', 'user__email'
        ).annotate(total_points=Sum('points')).order_by('-total_points')[:3]

        rewards = [50, 25, 15]
        for i, entry in enumerate(ranking):
            email = entry['user__email']
            if email:
                subject = f"Gratulacje! Zająłeś {i + 1} miejsce"
                message = f"Gratulacje! Zdobyłeś {i + 1} miejsce w rankingu tygodniowym. Nagroda: {rewards[i]} zł."
                from_email = "admin@fuelmate.com"

                # Wysyłanie e-maili
                send_reward_email(subject, message, from_email, [email], fail_silently=False)

        Points.objects.all().delete()
