# FuelMate/urls.py (or your project-level urls.py)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('add_prices/', include('add_prices.urls')),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),  # Strona główna
    #path('accounts/login/', TemplateView.as_view(template_name="login.html"), name='login'),

]

