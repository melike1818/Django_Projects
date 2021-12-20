from django.shortcuts import render
from django.db import connection
# Create your views here.
def index(request):
    return render(request, 'travel/index.html')

def hotel_booking(request):
    return render(request, 'travel/Hotel-Booking.html')

def tour_reservation(request):
    return render(request, 'travel/Tour-Reservation.html')

def flight_booking(request):
    return render(request, 'travel/Flight-Booking.html')

def previous_trips(request):
    return render(request, 'travel/Previous-Trips.html')

def friends(request):
    return render(request, 'travel/Friends.html')

def my_profile(request):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customer')
    r = cursor.fetchone()
    return render(request, 'travel/My-Profile.html', {'profile': r})

def login(request):
    return render(request, 'travel/Login.html')
