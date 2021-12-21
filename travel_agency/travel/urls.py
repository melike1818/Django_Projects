from django.urls import path
from travel import views

app_name = 'travel'

urlpatterns = [
    path('hotels/', views.hotel_booking, name = 'hotels'),
    path('tours/', views.tour_reservation, name = 'tours'),
    path('flight/', views.flight_booking, name = 'flight'),
    path('previous/', views.previous_trips, name = 'previous'),
    path('friends/', views.friends, name = 'friends'),
    path('profile/', views.my_profile, name = 'profile'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register_c, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('statistics/', views.statistics, name = 'statistics'),
]
