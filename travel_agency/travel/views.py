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
        cursor.close()
        return HttpResponseRedirect("/")
    return render(request, 'travel/index.html')

def hotel_booking(request):
    if request.method == "GET":
        stmt = "SELECT * FROM hotel;"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Hotel-Booking.html', {'hotels': r})
    if request.method == "POST":
        post = request.POST
        check_in = post["check_in"]
        check_out = post["check_out"]
        location = post["location"]
        rating = post["rating"]
        people = post["number"]

        if(str(rating) != "Select Minimum Rating For Hotel" and location == ""):
            stmt1 ="SELECT * FROM hotel where h_id in (SELECT h_id FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id) WHERE h_rate_unq>=" + rating + ");"

        if(location != "" and str(rating) == "Select Minimum Rating For Hotel") :
            stmt1 = "SELECT * FROM hotel WHERE h_address LIKE '%" + location + "%';"

        if(str(rating) != "Select Minimum Rating For Hotel" and location != ""):
            stmt1 = "SELECT * FROM (SELECT * FROM hotel where h_id in (SELECT h_id FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id) WHERE h_rate_unq>=" + rating + ")) INNER NATURAL JOIN (SELECT * FROM hotel WHERE h_address LIKE '%" + location + "%');"
<<<<<<< HEAD

=======
        
>>>>>>> b899aeaf19ca0ef9f6f16827217c64c6ff677c6d
        if(str(rating) == "Select Minimum Rating For Hotel" and location == ""):
            stmt1 = "SELECT h_id, h_name, h_address, h_phone, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT * FROM hotel WHERE h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+";"
        cursor = connection.cursor()
        cursor.execute(stmt1)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Hotel-Booking.html', {'hotels': r})

def tour_reservation(request):
    if request.method == "GET":
        stmt = "SELECT t_start_location, t_description, t_price FROM tour;"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Tour-Reservation.html', {'tours': r})
    if request.method == "POST":
        post = request.POST
        startdate = post["startdate"]
        enddate = post["enddate"]
        location = post["location"]
        desc = post["desc"]
        people = post["people"]
        stmt2 = "SELECT t_start_location, t_description, t_price FROM tour;"
        print("first: " + startdate + enddate + desc + location)
        if(startdate == None):
            startdate = "'2021-12-25'"
            
        if(enddate == None):
            enddate = "'2026-12-25'"
        
        if(desc == None):
            desc = ' '
            
        print("last: " + startdate + enddate + desc + location)
        if(location == None):
            stmt2 = 'SELECT t_start_location, t_description, t_price FROM tour WHERE t_start_date >= ' + startdate + ' and t_end_date <= ' + enddate + ' and t_capacity >= ' + people + ' and t_description like “%' + desc + '%”'
        else:
            stmt2 = 'SELECT t_start_location, t_description, t_price FROM tour WHERE t_start_date >= ' + startdate + ' and t_end_date <= ' + enddate + ' and t_capacity >= ' + people + ' and t_start_location == ' + location + ' and t_description like “%' + desc + '%”'
        cursor = connection.cursor()
        cursor.execute(stmt2)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Tour-Reservation.html', {'tours': r})    

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
    cursor.close()
    return render(request, 'travel/My-Profile.html', {'profile': r})
#Only for Employee
def manage_reservations(request):
    if request.method == "GET":
        return render(request, 'travel/manage_reservations.html')
    if request.method == "POST":
        return render(request, 'travel/manage_reservations.html')

def login(request):
    if request.method == 'POST':
        # get username and password from front-end
        post = request.POST
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        t = request.POST.get("type", "")
        # check if user exists if exists and password is correct send to index, if not show a warning
        try:
            stmt = "SELECT username, pw FROM " + t + " WHERE username = '" + username + "' AND pw = '" + password +"'"
            cursor = connection.cursor()
            cursor.execute(stmt)
            r = cursor.fetchone()
            cursor.close()
        except:
            print("db not exist")
            return render(request, 'travel/Login.html')


        if (r != None):
            request.session['username'] = username
            request.session[t] = True
            return HttpResponseRedirect("/")
        else:
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
        parameters = [str(c_id+1), request.POST.get("name", ""),request.POST.get("username", ""),request.POST.get("c_bdate", ""),request.POST.get("address", ""), request.POST.get("c_sex", ""), request.POST.get("pw", ""), request.POST.get("phone", "")]

        cursor.execute("INSERT INTO customer(u_id,name,username,c_bdate,c_address,c_sex,c_wallet,pw,phone) VALUES(%s,%s,%s,%s,%s,%s,0,%s,%s);", parameters)
        cursor.close()
        connection.commit()

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
        return HttpResponseRedirect("/")
    else:
        return render(request, 'travel/Register_Employee_Guide.html')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")

def statistics(request):
    return render(request, 'travel/Statistics.html')
