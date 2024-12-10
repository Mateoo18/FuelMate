from django.core.mail import send_mail

def send_reward_email(email, position, reward):
    subject = f"Gratulacje! Zająłeś {position} miejsce"
    message = f"Gratulacje! Zdobyłeś {position} miejsce w rankingu tygodniowym. Nagroda: {reward} zł."
    from_email = "admin@fuelmate.com"

    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
        print(f"E-mail wysłany do {email}")
    except Exception as e:
        print(f"Błąd wysyłania e-maila do {email}: {e}")
