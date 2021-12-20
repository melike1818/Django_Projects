from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import registerForm
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
    if request.method == 'POST':
        # get username and password from front-end
        post = request.POST
        username = request.POST.get("username", "")
        password= request.POST.get("password", "")
        print(username, password)
        # check if user exists if exists and password is correct send to index, if not show a warning
        stmt = "SELECT username, pw FROM general_user WHERE username = '" + username + "' AND pw = '" + password +"'"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchone()
        # Question: Should remember the user after login but how?
        if (r != None):
            print("successful login")
            return render(request, 'travel/index.html')
        else:
            print("user not found")
            return render(request, 'travel/Login.html')

def register_c(request):
    if request.method == 'POST':
        post = request.POST
        print('------------------------------')
        print(post)
        print('------------------------------')
        return HttpResponse("congrats, you are signed up <a href='/'>Sign in</a>")
    else:
        return render(request, 'travel/Register_customer.html')

def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = registerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            name = cd.get('name')
            username = cd.get('username')
            print(name, username)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = registerForm()

    return render(request, 'travel/Register_customer.html', {'form': form})
