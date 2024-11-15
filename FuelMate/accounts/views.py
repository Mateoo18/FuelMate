# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse

from stations.views import favorite_station_list
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from stations.models import Users, Favorite_Station, Gas_Stations

@login_required
def logged_in_view(request):
    return render(request, 'accounts/zalogowany.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user without logging them in
            messages.success(request, "Registration successful. Please log in.")
            return redirect(reverse('accounts:login'))  # Redirect to the login page
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
# accounts/views.py
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('stations:index')  # Redirect to stations app after login








