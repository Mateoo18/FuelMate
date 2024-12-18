from django.urls import path
from . import views

app_name = 'ranking'

urlpatterns = [
    path('weekly/', views.weekly_ranking, name='weekly_ranking'),
    path('ranking/', views.weekly_ranking, name='ranking'),

]
