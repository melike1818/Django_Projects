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
# TODO: should change the navbar according to user type
def login(request):
    if request.method == 'POST':
        # get username and password from front-end
        post = request.POST
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        t = request.POST.get("type", "")
        print(username, password)
        # check if user exists if exists and password is correct send to index, if not show a warning
        try:
            stmt = "SELECT username, pw FROM " + t + " WHERE username = '" + username + "' AND pw = '" + password +"'"
            print(stmt)
            cursor = connection.cursor()
            cursor.execute(stmt)
        except:
            print("db not exist")
            return render(request, 'travel/Login.html')

        r = cursor.fetchone()
        cursor.close()
        if (r != None):
            print("successful login")
            request.session['username'] = username
            return HttpResponseRedirect("/")
        else:
            print("user not found")
            return render(request, 'travel/Login.html')
    else:
        return render(request, 'travel/Login.html')

# Customer registration
def register_c(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        post = request.POST
        c_id_o = cursor.execute("SELECT COUNT(*) from customer")
        c_id = c_id_o.fetchone()[0]
        parameters = [(c_id+1), request.POST.get("name", ""), request.POST.get("username", ""), request.POST.get("c_bdate", ""), request.POST.get("address", ""), request.POST.get("c_sex", ""),0, request.POST.get("pw", ""),  request.POST.get("phone", "")]
        print(parameters)
        stmt = "INSERT INTO 'customer'('u_id','name','username','c_bdate','c_address','c_sex','c_wallet','pw','phone') VALUES (" + str(c_id+1) + ",'" + request.POST.get("name", "") + "','" + request.POST.get("username", "") +"','"+ request.POST.get("c_bdate", "")+"','"+ request.POST.get("address", "")+"','"+ request.POST.get("c_sex", "")+"', 0,'"+ request.POST.get("pw", "")+"','" + request.POST.get("phone", "")+"');"
        print(stmt)
        cursor.execute(stmt)
        cursor.close()
        connection.commit()
        connection.close()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'travel/Register_customer.html')

# Employee & Guide registration
def register_e_g(request):
    if request.method == 'POST':
        post = request.POST
        t = request.POST.get("type", "")
        cursor = connection.cursor()
        if(t == "Employee"):
            e_id_o = cursor.execute("SELECT COUNT(*) from employee")
            e_id = e_id_o.fetchone()[0]
            stmt = "INSERT INTO 'employee'('u_id','name','username','phone','pw','e_salary') VALUES (" + str(e_id+1) + ",'" + request.POST.get("name", "") + "','" + request.POST.get("username", "") +"','"+ request.POST.get("phone", "")+"','"+ request.POST.get("pw", "")+"',0);"
        else:
            g_id_o = cursor.execute("SELECT COUNT(*) from guide")
            g_id = g_id_o.fetchone()[0]
            stmt = "INSERT INTO 'guide'('u_id','name','username','phone','pw','g_salary','g_points','g_rating') VALUES (" + str(g_id+1) + ",'" + request.POST.get("name", "") + "','" + request.POST.get("username", "") +"','"+ request.POST.get("phone", "")+"','"+ request.POST.get("pw", "")+"',0,0,0);"
        cursor.execute(stmt)
        cursor.close()
        connection.commit()
        connection.close()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'travel/Register_Employee_Guide.html')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")

def statistics(request):
    return render(request, 'travel/Statistics.html')
