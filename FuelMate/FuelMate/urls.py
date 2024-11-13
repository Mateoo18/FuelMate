# FuelMate/urls.py (or your project-level urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stations.urls')),
    path('accounts/', include('accounts.urls')),

    path('profil_account/', include('profil_account.urls')),

]

