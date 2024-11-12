from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logged_in/', views.logged_in_view, name='logged_in'),

]