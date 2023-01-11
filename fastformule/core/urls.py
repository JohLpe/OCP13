from django.urls import path

from . import views

urlpatterns = [
    path('recherche/', views.search_results, name='search_results'),
    path('saisons/', views.seasons_page, name='seasons'),
    path('saisons/actuelle/', views.current_year_page, name='current'),
    path('saisons/<int:year>/', views.calendar_page, name='calendar'),
    path('saisons/get-info/', views.get_standings, name='getyearlyinfo'),
    path('saisons/<int:year>/<slug:gp_slug>/',
         views.gp_results, name='gp_results'),
    path('pilotes/', views.driver_page, name='driver_page'),
    path('pilotes/get-driver/', views.get_driver, name='getdriver'),
    path('pilotes/get-country/', views.get_by_country, name='getcountry'),
    path('pilotes/<slug:driver_slug>/', views.driver_info, name='driver_info')
]