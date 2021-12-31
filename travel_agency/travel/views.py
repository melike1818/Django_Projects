import sqlite3

from django.contrib.auth.context_processors import auth
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
        check_in = '2021-12-28'
        check_out = '2021-12-28'
        people = "1"
        stmt = "SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity FROM hotel WHERE" + " h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+";"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        print(r)
        cursor.close()
        return render(request, 'travel/Hotel-Booking.html', {'hotels': r})
    if request.method == "POST":
        post = request.POST
        check_in = post["check_in"]
        check_out = post["check_out"]
        location = post["location"]
        rating = post["rating"]
        people = post["number"]
        # Filter by rating
        if(str(rating) != "Select Minimum Rating For Hotel" and location == ""):
            stmt1 ="SELECT * FROM (SELECT * FROM hotel where h_id in (SELECT h_id FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id) WHERE h_rate_unq>=" + rating + ")) INNER NATURAL JOIN (SELECT h_id, h_name, h_address, h_phone, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT * FROM hotel WHERE h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+");"

        # Filter by location and availibility
        if(location != "" and str(rating) == "Select Minimum Rating For Hotel") :
            stmt1 = "SELECT * FROM (SELECT * FROM hotel WHERE h_address LIKE '%" + location + "%') INNER NATURAL JOIN (SELECT h_id, h_name, h_address, h_phone, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT * FROM hotel WHERE h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+");"

        # Filter by location and rating and availibility
        if(str(rating) != "Select Minimum Rating For Hotel" and location != ""):
            stmt1 = "SELECT * FROM (SELECT * FROM (SELECT * FROM hotel where h_id in (SELECT h_id FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id) WHERE h_rate_unq>=" + rating + ")) INNER NATURAL JOIN (SELECT * FROM hotel WHERE h_address LIKE '%" + location + "%')) INNER NATURAL JOIN (SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity FROM hotel WHERE h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+ ");"

        # only by availibility
        if(str(rating) == "Select Minimum Rating For Hotel" and location == ""):
            stmt1 = "SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity FROM hotel WHERE h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+";"
        cursor = connection.cursor()
        cursor.execute(stmt1)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Hotel-Booking.html', {'hotels': r})

def make_booking(request, pk):
    if request.method == "POST":
        print("inside post")
    else:
        #get the h_id
        h_id = pk
        cursor = connection.cursor()
        stmt = "SELECT * FROM room WHERE h_id = '"+str(h_id)+"';";
        cursor.execute(stmt)
        r = cursor.fetchall()
        print("Rooms")
        print(r)
        stmt = "SELECT * FROM hotel WHERE h_id = '"+str(h_id)+"';";
        cursor.execute(stmt)
        h = cursor.fetchone()
        print("Hotel Info")
        print(h)
        return render(request, 'travel/make_booking.html', {'rooms': r, "hotel" : h})

def tour_reservation(request):
    if request.method == "GET":

        if 'Employee' in request.session:
            stmt = "SELECT t_start_location, t_description, t_price, name FROM tour t, assign a, guide g where t.t_id = a.t_id and a.g_id = g.u_id UNION SELECT t_start_location, t_description, t_price, '' FROM tour t, assign a where t.t_id NOT IN (SELECT a.t_id FROM assign a); "
        if 'Customer' in request.session:
            stmt = "SELECT t_start_location, t_description, t_price  FROM tour; "

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
        guide = post["guide"]
        if 'Employee' in request.session:
            stmt2 = "SELECT t_start_location, t_description, t_price, name FROM tour t, assign a, guide g where t.t_id = a.t_id and a.g_id = g.u_id UNION SELECT t_start_location, t_description, t_price, '' FROM tour t, assign a where t.t_id NOT IN (SELECT a.t_id FROM assign a); "
        if 'Customer' in request.session:
            stmt2 = "SELECT t_start_location, t_description, t_price  FROM tour; "

        print("first: " + startdate + enddate + desc + location)

        if(startdate == None):
            startdate = "'2021-12-25'"

        if(enddate == ""):
            enddate = '2026-12-25'

        if(desc == ""):
            desc = ' '
        print("last: " + startdate + " " + enddate + " " + desc + " " + location)
        if(location == ""):
            stmt2 = "SELECT t_start_location, t_description, t_price FROM tour WHERE t_start_date >= '" + startdate + "' and t_end_date <= '" + enddate + "' and t_capacity >= " + people + " and t_description like '%" + desc + "%'"
        else:
            stmt2 = "SELECT t_start_location, t_description, t_price FROM tour WHERE t_start_date >= '" + startdate + "' and t_end_date <= '" + enddate + "' and t_capacity >= " + people + " and t_start_location like '%" + location + "%' and t_description like '%" + desc + "%'"

        #Filter by Guide
        if(str(guide) == "Assigned"):
            stmt2 = "SELECT t_start_location, t_description, t_price, name FROM tour t, assign a, guide g where t.t_id = a.t_id and a.g_id = g.u_id;"

        if(str(guide) == "Unassigned"):
            stmt2 = "SELECT DISTINCT t_start_location, t_description, t_price, '' FROM tour t, assign a where t.t_id NOT IN (SELECT a.t_id FROM assign a); "

        cursor = connection.cursor()
        cursor.execute(stmt2)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Tour-Reservation.html', {'tours': r})

def assign_guide(request):
    if request.method == "GET":
        id = 1
        stmt = "SELECT * FROM tour WHERE t_id = " + str(id);
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        print(r)
        return render(request, 'travel/tour/assign_guide.html', {'tours': r})

def tour_details(request):
    if request.method == "GET":
        id = 1
        stmt = "SELECT * FROM tour WHERE t_id = " + str(id);
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        print(r)
        return render(request, 'travel/Tour-details.html', {'tours': r})

def flight_booking(request):
    return render(request, 'travel/Flight-Booking.html')

def previous_trips(request):
    cursor = connection.cursor()
    stmt = "SELECT * FROM book_room NATURAL JOIN customer WHERE c_id = '"+ request.session['username']+"';"
    cursor.execute(stmt)
    r = cursor.fetchone()
    cursor.close()
    return render(request, 'travel/Previous-Trips.html', {'previous_trips': r})

def friends(request):
    return render(request, 'travel/Friends.html')

def my_profile(request):
    cursor = connection.cursor()
    stmt = "SELECT * FROM "+request.session['type']+" WHERE username = '"+ request.session['username']+"';"
    cursor.execute(stmt)
    r = cursor.fetchone()
    cursor.close()
    return render(request, 'travel/My-Profile.html', {'profile': r})

#Only for Employee
def manage_reservations(request):
    if request.method == "GET":
        stmt = "SELECT * FROM book_room"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/manage_reservations.html', {'reservations': r})
    if request.method == "POST":
        post = request.POST
        check_in = post["check_in"]
        check_out = post["check_out"]
        res_code = post["res_code"]
        rating = post["rating"]
        p_name = post["p_name"]
        ok = False
        stmt = ""
        stmt1 = "SELECT b_id FROM book_room WHERE b_id = "+ res_code
        stmt2 = "SELECT b_id FROM book_room WHERE b_start_date = '"+ check_in +"' AND b_end_date = '" + check_out+"'"
        stmt3 = "SELECT b_id FROM book_room NATURAL JOIN evaluate_hotel WHERE h_rate = "+rating
        stmt4 = "SELECT b_id FROM book_room NATURAL JOIN customer WHERE name = "+p_name
        if(res_code != ""):
            stmt = stmt1
            ok = True
        if(check_in != "" and check_out != ""):
            if(ok):
                stmt ="SELECT * FROM ("+stmt+") NATURAL JOIN ("+stmt2+")"
            else:
                stmt = stmt2
                ok = True
        if(rating != "Rating"):
            if(ok):
                stmt ="SELECT * FROM ("+stmt+") NATURAL JOIN ("+stmt3+")"
            else:
                stmt = stmt3
                ok = True
        if(p_name != ""):
            if(ok):
                stmt ="SELECT * FROM ("+stmt+") NATURAL JOIN ("+stmt4+")"
            else:
                stmt = stmt4
                ok = True
        if(ok):
            stmt = "SELECT * FROM book_room where b_id IN("+stmt+");"

        else:
            stmt = "SELECT * FROM book_room"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()

        return render(request, 'travel/manage_reservations.html', {'reservations': r})

def update_booking(request, b_id, h_id, r_id):
    if request.method == "POST":
        stmt = "SELECT * FROM book_room WHERE b_id = "+str(b_id)+" AND h_id = "+str(h_id)+" AND r_number = "+str(r_id)+";"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchone()
        cursor.close()
        print("post")
        context = {
            'res_code':r[0],
            'hotel_id':r[1],
            'start':r[2],
            'end':r[3],
            'c_id':r[4],
            'r_id':r[6],
            'status':r[7],
            'comment':r[8],
        }
    return render(request, 'travel/update_booking.html', {'context': context})
    if request.method == "GET":
        print("get")
        return render(request, 'travel/update_booking.html')

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
            request.session['type'] = t
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
