from django.urls import path
from . import views

app_name = 'locate_station'

urlpatterns = [
    path('search/', views.logged_in_view, name='search'),
    path('search/news/fuel-prices/', views.NewsFuelPricesView.as_view(), name='news_fuel_prices'),
    path('search/news/cheapest-station/', views.NewsCheapestStationView.as_view(), name='news_cheapest_station'),
    path('search/news/safety-station/', views.NewsSafetyStationView.as_view(), name='news_safety_station'),
    path('search/news/regulations-station/', views.NewsRegulationsStationView.as_view(), name='news_regulations_station'),
    path('search/news/technology-station/', views.NewsTechnologyStationView.as_view(), name='news_technology_station'),


]
