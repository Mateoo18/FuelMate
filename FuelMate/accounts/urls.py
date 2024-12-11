from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import LoginModalView,CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginModalView.as_view(), name='login'),
    path('logged_in/', views.logged_in_view, name='logged_in'),
    path('logout/', CustomLogoutView.as_view(next_page='/'), name='logout'),

]