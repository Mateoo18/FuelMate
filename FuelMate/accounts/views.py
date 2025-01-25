# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from stations.models import Users, FavoriteStation, GasStations
from .models import Profile

from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.contrib import messages
@login_required
def logged_in_view(request):
    return redirect(reverse_lazy('stations:default_page'))


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user without logging them in
            # messages.success(request, "Registration successful. Please log in.")
            return redirect(reverse('accounts:login'))  # Redirect to the login page
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
# accounts/views.py
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('profil_account:profile')  # Redirect to stations app after login

class LoginModalView(LoginView):
    template_name = 'accounts/login_partial.html'

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, self.template_name, self.get_context_data())
        return super().get(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "")
        return super().dispatch(request, *args, **kwargs)
