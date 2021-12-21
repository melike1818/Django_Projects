from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import registerForm
# Create your views here.
def index(request):
    if request.method == "POST":
        post = request.POST
        username = post["username"]
        password = post["password"]
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        if auth:
            request.session['username'] = username
        return HttpResponseRedirect("/")
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
    if request.method == 'POST':
        # get username and password from front-end
        post = request.POST
        username = request.POST.get("username", "")
        password= request.POST.get("password", "")
        print(username, password)
        # check if user exists if exists and password is correct send to index, if not show a warning
        try:
            stmt = "SELECT username, pw FROM customer WHERE username = '" + username + "' AND pw = '" + password +"'"
            cursor = connection.cursor()
            cursor.execute(stmt)
        except:
            print("db not exist")
            return render(request, 'travel/Login.html')

        r = cursor.fetchone()
        # Question: Should remember the user after login but how?
        if (r != None):
            print("successful login")
            request.session['username'] = username
            return HttpResponseRedirect("/")
        else:
            print("user not found")
            return render(request, 'travel/Login.html')
    else:
        return render(request, 'travel/Login.html')


def register_c(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        post = request.POST
        c_id = cursor.execute("SELECT COUNT(*) from customer")
        parameters = [(c_id+1), request.POST.get("name", ""), request.POST.get("username", ""), request.POST.get("pw", ""), request.POST.get("c_bdate", ""), request.POST.get("address", ""), request.POST.get("c_sex", ""), 0, request.POST.get("phone", "")]
        print(parameters)

        cursor.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", parameters)
        connection.commit()
        connection.close()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'travel/Register_customer.html')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")