from django.utils.timezone import now
from datetime import timedelta
from .email_tasks import send_reward_email
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
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
            subject = f"Nagroda w konkursie od FuelMate za {i+1} miejsce "
            message = f"Gratulacje! Zdobyłeś {i+1} miejsce w rankingu tygodniowym. Nagroda to: {rewards[i]} zł."
            from_email = settings.DEFAULT_FROM_EMAIL
            try:
                send_mail(subject, message, from_email, [email], fail_silently=False)
                print(f"E-mail wysłany do {email}")
            except Exception as e:
                print(f"Błąd wysyłania e-maila do {email}: {e}")

        Points.objects.all().delete()
