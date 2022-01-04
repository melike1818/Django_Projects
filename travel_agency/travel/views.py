import sqlite3

from django.contrib.auth.context_processors import auth
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import registerForm
from django.urls import reverse


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
        cursor.close()
        return render(request, 'travel/Hotel-Booking.html', {'hotels': r})
    if request.method == "POST":
        post = request.POST
        check_in = post["check_in"]
        check_out = post["check_out"]
        location = post["location"]
        rating = post["rating"]
        people = post["number"]
        request.session['check_in'] = check_in
        request.session['check_out'] = check_out
        request.session['no_people'] = people
        stmt1 = "SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity FROM hotel WHERE" + " h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+";"

        # Filter by rating
        if(str(rating) != "Select Minimum Rating For Hotel" and location == ""):
            stmt1 ="SELECT * FROM(SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity FROM hotel WHERE" + " h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+") WHERE h_id IN (SELECT h_id FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id) WHERE h_rate_unq>=" + rating +");"
        # Filter by location and availibility
        if(location != "" and str(rating) == "Select Minimum Rating For Hotel") :
            stmt1 = "SELECT * FROM (SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity FROM hotel WHERE" + " h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+") WHERE h_id IN (SELECT h_id FROM hotel WHERE h_address LIKE '%" + location + "%');"

        # Filter by location and rating and availibility
        if(str(rating) != "Select Minimum Rating For Hotel" and location != ""):
            stmt1 = "SELECT * FROM (SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity - res_room FROM hotel AS H NATURAL JOIN( SELECT h_id, COUNT(b_id) AS res_room FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"' GROUP BY h_id) WHERE h_capacity - res_room >= "+ people +" UNION SELECT h_id, h_name, h_address, h_phone, h_capacity, h_capacity FROM hotel WHERE" + " h_id NOT IN ( SELECT h_id FROM book_room  where b_start_date <= '"+ check_out +"' AND b_end_date >= '" + check_in +"') AND h_capacity >= "+ people+") WHERE h_id IN(SELECT * FROM (SELECT h_id FROM hotel WHERE h_address LIKE '%" + location + "%') WHERE h_id IN (SELECT h_id FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id) WHERE h_rate_unq>=" + rating +"));"
        cursor = connection.cursor()
        cursor.execute(stmt1)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Hotel-Booking.html', {'hotels': r})

def make_booking(request, pk):
    if request.method == "POST":
        print("inside post")
        return HttpResponse("Booking Successful!")
    else:
        #get the h_id
        h_id = pk
        cursor = connection.cursor()
        stmt = "SELECT * FROM room WHERE h_id = '"+str(h_id)+"';"
        cursor.execute(stmt)
        r = cursor.fetchall()
        print("Rooms")
        print(r)
        stmt = "SELECT * FROM hotel WHERE h_id = '"+str(h_id)+"';"
        cursor.execute(stmt)
        h = cursor.fetchone()
        print("Hotel Info")
        print(h)
        if 'Customer' in request.session:
            u = 0
        if 'Employee' in request.session:
            u = 1
        return render(request, 'travel/make_booking.html', {'rooms': r, "hotel" : h, "user" : u})

def done_booking(request, pk, r_id):
    if request.method == 'POST':
        if 'Employee' in request.session:
            #make booking accordingly
            cursor = connection.cursor()
            c_id = (cursor.execute("SELECT u_id FROM customer WHERE username = '" + request.POST.get("name", "") + "';")).fetchone()[0]

            print(c_id)
            b_id = (cursor.execute("SELECT COUNT(*) from booking")).fetchone()[0]
            b_id = b_id + 1
            parameters = [b_id,request.POST.get("check_in", ""), request.POST.get("check_out", ""), request.POST.get("number", "")]
            print(parameters)

            cursor.execute("INSERT INTO booking(b_id,b_start_date, b_end_date, no_of_people) VALUES(%s,%s,%s,%s);", parameters)
            parameters = [b_id, pk, request.POST.get("check_in", ""), request.POST.get("check_out", ""), c_id, request.session['u_id'], r_id, 'true', 'created by employee']
            cursor.execute("INSERT INTO book_room VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);", parameters)
            cursor.close()
            connection.commit()

        if 'Customer' in request.session:
            cursor = connection.cursor()
            b_id = (cursor.execute("SELECT COUNT(*) from booking")).fetchone()[0]
            b_id = b_id + 1
            #Insert into booking Table
            parameters = [b_id, request.POST.get("check_in", ""), request.POST.get("check_out", ""), request.POST.get("number", "")]
            cursor.execute("INSERT INTO booking(b_id,b_start_date, b_end_date, no_of_people) VALUES(%s,%s,%s,%s);", parameters)
            #Insert into book_room table
            parameters = [b_id, pk, request.POST.get("check_in", ""), request.POST.get("check_out", ""), request.session['u_id'], r_id]
            cursor.execute("INSERT INTO book_room (b_id, h_id, b_start_date, b_end_date,c_id, r_number) VALUES(%s,%s,%s,%s,%s,%s);", parameters)
            cursor.close()
            connection.commit()
    cursor = connection.cursor()
    cursor.execute("SELECT h_name from hotel where h_id =" + str(pk)+";")
    h = cursor.fetchone()
    cursor.execute("SELECT bed_capacity from room where h_id =" + str(pk) + " AND r_number = " + str(r_id)+";")
    m = cursor.fetchone()
    cursor.close()
    return render(request, 'travel/done_booking.html', {'hname' : h, 'room' : r_id, 'max': m})

def done_booking_e(request, pk, r_id):
    if request.method == 'POST':
        #make booking accordingly
        cursor = connection.cursor()
        c_id = (cursor.execute("SELECT u_id FROM customer WHERE username = '" + request.POST.get("name", "") + "';")).fetchone()[0]

        print(c_id)
        b_id = (cursor.execute("SELECT COUNT(*) from booking")).fetchone()[0]
        b_id = b_id + 1
        parameters = [b_id,request.POST.get("check_in", ""), request.POST.get("check_out", ""), request.POST.get("number", "")]
        print(parameters)

        cursor.execute("INSERT INTO booking(b_id,b_start_date, b_end_date, no_of_people) VALUES(%s,%s,%s,%s);", parameters)
        parameters = [b_id, pk, request.POST.get("check_in", ""), request.POST.get("check_out", ""), c_id, request.session['u_id'], r_id, 'true', 'created by employee']
        cursor.execute("INSERT INTO book_room VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);", parameters)
        cursor.close()
        connection.commit()

    cursor = connection.cursor()
    cursor.execute("SELECT h_name from hotel where h_id =" + str(pk)+";")
    h = cursor.fetchone()
    cursor.execute("SELECT bed_capacity from room where h_id =" + str(pk) + " AND r_number = " + str(r_id)+";")
    m = cursor.fetchone()
    cursor.close()
    return render(request, 'travel/done_booking_e.html', {'hname' : h, 'room' : r_id, 'max': m})

def update_booking(request):
    if request.method == "POST":
        post = request.POST
        cursor = connection.cursor()
        comment = request.POST.get("comment", "")
        stmt = "SELECT u_id FROM Employee where username = '"+request.session['username']+"';"
        cursor.execute(stmt)
        e_id = cursor.fetchone()[0]
        stmt  = "UPDATE book_room SET b_start_date = '"+str(post['check_in'])+"', b_end_date = '"+str(post['check_out'])+"', explanation = '"+comment+"', is_accepted = "+post['is_accepted']+", e_id = '"+str(e_id)+"' WHERE h_id = "+post['hotel_id']+" AND b_id = "+post['b_id']+" AND r_number = "+post['r_id']+";"
        cursor.execute(stmt)
        connection.commit()
        stmt = "UPDATE booking SET b_start_date = '"+str(post['check_in'])+"', b_end_date = '"+str(post['check_out'])+"', no_of_people = "+str(post['number'])+" WHERE b_id = "+str(post['b_id'])+";"
        cursor.execute(stmt)
        connection.commit()
        cursor.close()
        context = {

        }
        return HttpResponseRedirect(reverse('travel:manage_booking'))

def tour_reservation(request):
    if request.method == "GET":

        if 'Employee' in request.session:
            stmt = "SELECT t.t_id, t_start_location, t_description, t_price, name FROM tour t, assign a, guide g where t.t_id = a.t_id and a.g_id = g.u_id UNION SELECT t.t_id, t_start_location, t_description, t_price, '' FROM tour t, assign a where t.t_id NOT IN (SELECT a.t_id FROM assign a); "
        if 'Customer' in request.session:
            stmt = "SELECT t_id, t_start_location, t_description, t_start_date, t_price  FROM tour; "

        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        print(r)
        cursor.close()
        return render(request, 'travel/Tour-Reservation.html', {'tours': r})
    if request.method == "POST":
        post = request.POST
        startdate = post["startdate"]
        enddate = post["enddate"]
        location = post["location"]
        desc = post["desc"]
        people = post["people"]
        if 'Employee' in request.session:
            stmt2 = "SELECT t.t_id, t_start_location, t_description, t_price, name FROM tour t, assign a, guide g where t.t_id = a.t_id and a.g_id = g.u_id UNION SELECT t.t_id, t_start_location, t_description, t_price, '' FROM tour t, assign a where t.t_id NOT IN (SELECT a.t_id FROM assign a); "
        if 'Customer' in request.session:
            stmt2 = "SELECT t_id, t_start_location, t_description, t_start_date, t_price  FROM tour; "

        if(startdate == ""):
            startdate = '2022-01-01'

        if(enddate == ""):
            enddate = '2026-12-25'

        if(desc == ""):
            desc = ' '

        if(location == ""):
            stmt2 = "SELECT t_id, t_start_location, t_description, t_start_date, t_price FROM tour WHERE t_start_date >= '" + startdate + "' and t_end_date <= '" + enddate + "' and t_capacity >= " + people + " and t_description like '%" + desc + "%'; "
        else:
            stmt2 = "SELECT t_id, t_start_location, t_description, t_start_date, t_price FROM tour WHERE t_start_date >= '" + startdate + "' and t_end_date <= '" + enddate + "' and t_capacity >= " + people + " and t_start_location like '%" + location + "%' and t_description like '%" + desc + "%'; "

        if 'Employee' in request.session:
            guide = post["guide"]
            #Filter by Guide
            if(str(guide) == "Assigned"):
                stmt2 = "SELECT t.t_id, t_start_location, t_description, t_price, name FROM tour t, assign a, guide g where t.t_id = a.t_id and a.g_id = g.u_id; "

            if(str(guide) == "Unassigned"):
                stmt2 = "SELECT DISTINCT t.t_id, t_start_location, t_description, t_price, '' FROM tour t, assign a where t.t_id NOT IN (SELECT a.t_id FROM assign a); "

        cursor = connection.cursor()
        cursor.execute(stmt2)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/Tour-Reservation.html', {'tours': r})

def assign_guide(request,pk):
    print("inside guide")
    if request.method == "GET":
        stmt = "SELECT u_id, name FROM guide;"
        cursor = connection.cursor()
        cursor.execute(stmt)
        g = cursor.fetchall()
        print(g)
        cursor.close()
        return render(request, 'travel/assign_guide.html', {'guides': g, 't_id': pk})
    if request.method == "POST":
        post = request.POST
        stmt2 = "SELECT u_id, name FROM guide;"
        guide = post["guide"]
        #Filter by Guide
        if(str(guide) == "All"):
            stmt2 = "SELECT u_id, name FROM guide;"
        if(str(guide) == "Available"):
            stmt2 = "SELECT DISTINCT u_id, name FROM guide g, assign a WHERE g.u_id NOT IN (SELECT a.g_id FROM assign a);"
        if(str(guide) == "Unavailable"):
            #stmt2 = "SELECT g.u_id, name FROM guide g, assign a, tour t where t.t_id = '"+ str(pk) +"' AND t.t_start_date >= a.t_start_date and t.t_start_date <= a.t_end_date or t.t_end_date >= a.t_start_date and t.t_end_date <= a.t_end_date ;"
            #stmt2 = "SELECT g.u_id, name FROM guide g, assign a, tour t where t.t_id = '"+ str(pk) +"' AND t.t_start_date > a.t_start_date or t.t_end_date < a.t_end_date;"
            #stmt2 = "SELECT g.u_id, name FROM guide g, assign a, tour t where t.t_id = '"+ str(pk) +"' AND a.t_start_date BETWEEN (t.t_start_date >= a.t_start_date and t.t_start_date <= a.t_end_date) ;"
            #stmt2 = "SELECT t.t_id, t.t_start_date FROM tour t where t.t_id = '"+ str(pk) +"' ;"
            stmt2 = "SELECT DISTINCT g.u_id, name FROM guide g, assign a where g.u_id = a.g_id;"
        cursor = connection.cursor()
        cursor.execute(stmt2)
        g = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/assign_guide.html', {'guides': g, 't_id': pk})


def assign_tour(request, pk, g_id):
    print("inside tour")
    if request.method == 'POST':
        cursor = connection.cursor()
        stmt = "SELECT u_id FROM employee where username = '"+request.session['username']+"';"
        cursor.execute(stmt)
        e_id = cursor.fetchone()[0]

        stmt = "SELECT t_start_date FROM tour where t_id = '"+str(pk)+"';"
        cursor.execute(stmt)
        startDate = cursor.fetchone()[0]
        stmt = "SELECT t_end_date FROM tour where t_id = '"+str(pk)+"';"
        cursor.execute(stmt)
        endDate = cursor.fetchone()[0]

        parameters = [pk, startDate, endDate, g_id, str(e_id)]
        cursor.execute("INSERT INTO assign(t_id, t_start_date, t_end_date, g_id, e_id) VALUES(%s,%s,%s,%s,%s);", parameters)
        cursor.close()
        connection.commit()
        cursor = connection.cursor()

    r = cursor.fetchall()
    cursor.close()

    return HttpResponseRedirect(reverse('travel:tours'))

def guide_tours(request):
    if request.method == "GET":
        cursor = connection.cursor()
        stmt = "SELECT u_id FROM guide where username = '"+request.session['username']+"';"
        cursor.execute(stmt)
        g_id = cursor.fetchone()[0]
        stmt = "SELECT a.t_id, t_name, a.t_start_date, a.t_end_date, t_start_location, accepted FROM tour t, assign a, guide g where t.t_id = a.t_id and g.u_id = '"+str(g_id)+"' and g.u_id = a.g_id;"
        cursor.execute(stmt)
        connection.commit()
        r = cursor.fetchall()
        print(r)
        cursor.close()
        return render(request, 'travel/guide_tours.html', {'tours': r})
    if request.method == "POST":
        post = request.POST
        cursor = connection.cursor()
        stmt2 = "SELECT u_id FROM guide where username = '"+request.session['username']+"';"
        cursor.execute(stmt2)
        g_id = cursor.fetchone()[0]
        stmt2 = "SELECT a.t_id, t_name, a.t_start_date, a.t_end_date, t_start_location, accepted FROM tour t, assign a, guide g where t.t_id = a.t_id and g.u_id = '"+str(g_id)+"' and g.u_id = a.g_id;"
        cursor.execute(stmt2)
        connection.commit()
        r = cursor.fetchall()
        print(r)
        cursor.close()
        return render(request, 'travel/guide_tours.html', {'tours': r})

def tour_accepted(request,pk):
    if request.method == "POST":
        post = request.POST
        cursor = connection.cursor()
        stmt2 = "SELECT u_id FROM guide where username = '"+request.session['username']+"';"
        cursor.execute(stmt2)
        g_id = cursor.fetchone()[0]
        stmt2 = "UPDATE assign SET accepted = true where g_id ='"+str(g_id)+"' and t_id = '"+str(pk)+"';"
        cursor.execute(stmt2)
        connection.commit()
        r = cursor.fetchall()
        print(r)
        cursor.close()
        return render(request, 'travel/guide_feedback.html', {'tours': r, 't_id': pk})

def tour_declined(request,pk):
    if request.method == "POST":
        post = request.POST
        cursor = connection.cursor()
        stmt2 = "SELECT u_id FROM guide where username = '"+request.session['username']+"';"
        cursor.execute(stmt2)
        g_id = cursor.fetchone()[0]
        stmt2 = "UPDATE assign SET accepted = false where g_id ='"+str(g_id)+"' and t_id = '"+str(pk)+"';"
        cursor.execute(stmt2)
        connection.commit()
        r = cursor.fetchall()
        print(r)
        cursor.close()
        return render(request, 'travel/state_reason.html', {'tours': r, 't_id': pk})

def state_reason(request,pk):
    print("inside state")
    if request.method == 'POST':
        cursor = connection.cursor()
        stmt = "SELECT u_id FROM guide where username = '"+request.session['username']+"';"
        cursor.execute(stmt)
        g_id = cursor.fetchone()[0]
        stmt = "SELECT t_start_date FROM tour where t_id = '"+str(pk)+"';"
        cursor.execute(stmt)
        startDate = cursor.fetchone()[0]
        stmt = "SELECT t_end_date FROM tour where t_id = '"+str(pk)+"';"
        cursor.execute(stmt)
        endDate = cursor.fetchone()[0]
        post = request.POST
        reason = post["reason"]
        parameters = [pk, startDate, endDate, str(g_id), request.session['reason'],]
        cursor.execute("INSERT INTO feedback(t_id, t_start_date, t_end_date, g_id, f_text) VALUES(%s,%s,%s,%s,%s);", parameters)
        cursor.close()
        connection.commit()
        cursor = connection.cursor()

    r = cursor.fetchall()
    cursor.close()

    return render(request, 'travel/state_reason.html')


def guide_feedback(request,pk):
    if request.method == "GET":
        return render(request, 'travel/guide_feedback.', {'t_id': pk})
    if request.method == "POST":
        post = request.POST
        gfeedback = post["gfeedback"]
        cursor = connection.cursor()
        stmt = "SELECT u_id FROM guide where username = '"+request.session['username']+"';"
        cursor.execute(stmt)
        g_id = cursor.fetchone()[0]

        stmt = "SELECT t_start_date FROM tour where t_id = '"+str(pk)+"';"
        cursor.execute(stmt)
        startDate = cursor.fetchone()[0]
        stmt = "SELECT t_end_date FROM tour where t_id = '"+str(pk)+"';"
        cursor.execute(stmt)
        endDate = cursor.fetchone()[0]

        try:
            cursor.execute("INSERT INTO feedback(t_id, t_start_date, t_end_date, g_id, f_text) VALUES(" + str(pk) + ", '" + startDate +"','" + endDate +"', " + str(g_id)  + gfeedback  +");",)
        except:
            print("There is already a comment submitted")
        return render(request, 'travel/guide_feedback.html')


def booking_detail(request, b_id, h_id, r_id):
    if request.method == "POST":
        stmt = "SELECT * FROM book_room WHERE b_id = "+str(b_id)+" AND h_id = "+str(h_id)+" AND r_number = "+str(r_id)+";"
        stmt1 = "SELECT no_of_people FROM booking WHERE b_id = "+str(b_id)+";"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchone()
        cursor.execute(stmt1)
        no_of_people = cursor.fetchone()[0]
        cursor.close()
        context = {
            'res_code':r[0],
            'hotel_id':r[1],
            'start':r[2],
            'end':r[3],
            'c_id':r[4],
            'r_id':r[6],
            'status':r[7],
            'comment':r[8],
            'people':no_of_people,
        }
        return render(request, 'travel/update_booking.html', {'context': context})



def tour_details(request, pk):
    if request.method == "POST":
        print("inside post")
        cursor = connection.cursor()
        stmt3 = "SELECT COUNT(ea.a_id) FROM tour as t NATURAL JOIN places_activities as p NATURAL JOIN activity as a NATURAL JOIN extra_activity as ea WHERE ea.a_id = a.a_id and p.a_id = a.a_id and t.t_id == '" + str(pk)+ "'; "
        cursor.execute(stmt3)
        ea_count = cursor.fetchone()[0]
        if ea_count > 0:
            checked = request.POST.getlist('checks[]')
            #insert checked extra activities to the buys
            for c in checked:
                r_id = (cursor.execute("SELECT COUNT(*) from buys")).fetchone()[0]
                r_id = r_id + 1
                parameters = [r_id, c , request.session['u_id'] ]
                cursor.execute("INSERT INTO buys(receipt_id, a_id, c_id) VALUES(%s,%s,%s);", parameters)
            cursor.close()
            connection.commit()
    stmt = "SELECT a.a_id, a.a_name, a.a_date, a.a_capacity FROM tour as t NATURAL JOIN places_activities as p NATURAL JOIN (SELECT * FROM activity WHERE a_id NOT IN (SELECT a_id from extra_activity)) as a WHERE p.a_id = a.a_id and t.t_id == '" + str(pk)+ "'; "
    cursor = connection.cursor()
    cursor.execute(stmt)
    r = cursor.fetchall()


    stmt3 = "SELECT ea.a_id,a.a_name, ea.a_date, a.a_capacity, ea.price FROM tour as t NATURAL JOIN places_activities as p NATURAL JOIN activity as a NATURAL JOIN (SELECT * FROM extra_activity WHERE a_id NOT IN (SELECT a_id from buys WHERE c_id = " + str(request.session['u_id'])+ ")) as ea WHERE ea.a_id = a.a_id and p.a_id = a.a_id and t.t_id == '" + str(pk)+ "'; "
    cursor.execute(stmt3)
    ea = cursor.fetchall()

    stmt2 = "SELECT t_id, t_start_location, t_description, t_price, t_start_date, t_end_date, t_capacity FROM tour WHERE t_id == '" + str(pk)+ "'; "
    cursor.execute(stmt2)
    h = cursor.fetchone()
    cursor.close()
    context = {
        't_id':h[0],
        't_start_location':h[1],
        't_description':h[2],
        't_price':h[3],
        't_start_date':h[4],
        't_end_date':h[5],
        't_capacity':h[6]
    }
    return render(request, 'travel/Tour-details.html', {'context': context, 'activities': r, 'eactivity': ea})

def make_reservation(request, t_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * from tour where t_id =" + str(t_id)+";")
    tour = cursor.fetchone()
    cursor.execute("SELECT a.a_name, ea.price from extra_activity as ea NATURAL JOIN buys as b NATURAL JOIN activity as a NATURAL JOIN places_activities as p where a.a_id = ea.a_id and a.a_id = p.a_id and ea.a_id = b.a_id and b.c_id = " + str(request.session['u_id'])+" AND p.t_id = " + str(t_id)+ " ;")
    ea = cursor.fetchall()
    cursor.close()
    total = tour[6]
    for a in ea:
        total += a[1]

    if request.method == 'POST':
        if 'Employee' in request.session:
            #make booking accordingly
            cursor = connection.cursor()
            c_id = (cursor.execute("SELECT u_id FROM customer WHERE username = '" + request.POST.get("name", "") + "';")).fetchone()[0]

            print(c_id)
            b_id = (cursor.execute("SELECT COUNT(*) from booking")).fetchone()[0]
            b_id = b_id + 1
            parameters = [b_id,request.POST.get("check_in", ""), request.POST.get("check_out", ""), request.POST.get("number", "")]
            print(parameters)

            cursor.execute("INSERT INTO booking(b_id,b_start_date, b_end_date, no_of_people) VALUES(%s,%s,%s,%s);", parameters)
            parameters = [b_id, pk, request.POST.get("check_in", ""), request.POST.get("check_out", ""), c_id, request.session['u_id'], r_id, 'true', 'created by employee']
            cursor.execute("INSERT INTO book_room VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);", parameters)
            cursor.close()
            connection.commit()

        if 'Customer' in request.session:
            cursor = connection.cursor()
            r_id = (cursor.execute("SELECT COUNT(*) from reserves")).fetchone()[0]
            r_id = r_id + 1

            #Insert into reservation Table
            cursor.execute("SELECT t_start_date, t_end_date from tour where t_id =" + str(t_id)+";")
            tour = cursor.fetchone()
            t_price = (cursor.execute("SELECT t_price from tour WHERE t_id = " + str(t_id) + ";")).fetchone()[0]
            ea_price = 0
            parameters = [r_id,tour[0],tour[1], str(t_price + ea_price), request.POST.get("number", "")]
            cursor.execute("INSERT INTO reservation(r_id, r_start_date, r_end_date,r_price,r_customer_num) VALUES(%s,%s,%s,%s,%s);", parameters)

            #Insert into reserves Table
            cursor.execute("SELECT * from tour where t_id =" + str(t_id)+";")
            t = cursor.fetchone()
            parameters = [r_id,t_id, tour[0],tour[1],request.session['u_id']]
            cursor.execute("INSERT INTO reserves(r_id, t_id, t_start_date, t_end_date, c_id) VALUES(%s,%s,%s,%s,%s);", parameters)

            #update wallet
            cursor.execute("SELECT c_wallet from customer where u_id = " + str(request.session['u_id'])+";")
            oldW = cursor.fetchone()[0]
            newWallet = oldW - (int(request.POST.get("number", ""))*total)
            stmt = "UPDATE customer SET c_wallet = "+ str(newWallet)+" WHERE u_id = " +str(request.session['u_id']) + ";"
            cursor.execute(stmt)
            cursor.close()
            connection.commit()

    return render(request, 'travel/done_reservation.html', {'tour' : tour, 'extra' : ea, 'tot': total})

def flight_booking(request):
    return render(request, 'travel/Flight-Booking.html')

def give_feedback(request, pk):
    if request.method == "GET":
        return render(request, 'travel/Give_feedback.html')
    if request.method == "POST":
        post = request.POST
        rate = post["rate"]
        comment = post["comment"]
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO evaluate_hotel(h_id, c_id, h_comment, h_rate) VALUES(" + str(pk) + ", " + str(request.session['u_id']) + ", '" + comment +"', " + str(rate) +");",)
        except:
            print("There is already a comment submitted")
        return render(request, 'travel/Give_feedback.html')

def give_feedback_tour(request, pk):
    if request.method == "GET":
        return render(request, 'travel/Give_feedback_tour.html')
    if request.method == "POST":
        post = request.POST
        rate = post["rate"]
        comment = post["comment"]
        rateg = post["rateg"]
        commentg = post["commentg"]
        stmt = "SELECT g_id FROM assign a, tour t WHERE t.t_id = a.t_id;"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchone()
        try:
            cursor.execute("INSERT INTO evaluate_guide(g_id, c_id, g_comment, g_rate) VALUES(" + str(pk) + ", " + str(request.session['u_id']) + ", '" + commentg +"', " + str(rateg) +");",)
            cursor.execute("INSERT INTO evaluate_tour(t_id, c_id, t_comment, t_rate) VALUES(" + str(pk) + ", " + str(request.session['u_id']) + ", '" + comment +"', " + str(rate) +");",)
            stmt = "SELECT Count(*) as count FROM tour t natural join evaluate_tour WHERE t.t_id = " + pk + ";"
            cursor = connection.cursor()
            cursor.execute(stmt)
            r = cursor.fetchone()
            stmt = "SELECT t_rate FROM tour WHERE t_id = " + pk + ";"
            cursor.execute(stmt)
            x = cursor.fetchone()
            if r != 0:
                temp = r
                r =  r * x + rate
                res = r / (temp + 1)
                stmt = "UPDATE tour SET t_rate = '"+ res +"' WHERE t_id = "+str(pk)+";"
                cursor.execute(stmt)
            else:
                stmt = "UPDATE tour SET t_rate = '"+ rate +"' WHERE t_id = "+str(pk)+";"
                cursor.execute(stmt)
        except:
            print("There is already a comment submitted")


        return render(request, 'travel/Give_feedback_tour.html')

def previous_trips(request):
    cursor = connection.cursor()
    #Hotel Bookings
    stmt = "SELECT * FROM booking NATURAL JOIN book_room NATURAL JOIN hotel WHERE c_id = %s AND is_accepted = '1' AND b_end_date < '2023-01-30';"
    cursor.execute(stmt, [request.session['u_id']] )
    a_b = cursor.fetchall()

    stmt = "SELECT * FROM booking NATURAL JOIN book_room NATURAL JOIN hotel WHERE c_id = %s AND is_accepted = '0' AND b_end_date < '2023-01-30';"
    cursor.execute(stmt, [request.session['u_id']] )
    d_b = cursor.fetchall()
    print(d_b)
    stmt = "SELECT * FROM booking NATURAL JOIN book_room NATURAL JOIN hotel WHERE c_id = %s AND is_accepted IS NULL AND b_end_date < '2023-01-30';"
    cursor.execute(stmt, [request.session['u_id']] )
    w_b = cursor.fetchall()

    #Tours
    stmt = "SELECT * FROM tour NATURAL JOIN reserves NATURAL JOIN reservation WHERE c_id = %s AND is_accepted = '1' AND t_end_date < '2022-01-30';"
    cursor.execute(stmt, [request.session['u_id']] )
    a_t = cursor.fetchall()

    stmt = "SELECT * FROM tour NATURAL JOIN reserves NATURAL JOIN reservation WHERE c_id = %s AND is_accepted = '0' AND t_end_date < '2022-01-30';"
    cursor.execute(stmt, [request.session['u_id']] )
    d_t = cursor.fetchall()

    stmt = "SELECT * FROM tour NATURAL JOIN reserves NATURAL JOIN reservation WHERE c_id = %s AND is_accepted IS NULL AND t_end_date < '2022-01-30';"
    cursor.execute(stmt, [request.session['u_id']] )
    w_t = cursor.fetchall()

    cursor.close()
    return render(request, 'travel/Previous-Trips.html', {'a_hotel_booking': a_b , 'd_hotel_booking' : d_b, 'w_hotel_booking' : w_b, 'a_tour': a_t , 'd_tour' : d_t, 'w_tour' : w_t})

def friends(request):
    return render(request, 'travel/Friends.html')

def my_profile(request):
    cursor = connection.cursor()
    stmt = "SELECT * FROM "+request.session['type']+" WHERE username = '"+ request.session['username']+"';"
    cursor.execute(stmt)
    p = cursor.fetchone()
    cursor.close()
    return render(request, 'travel/My-Profile.html', {'profile': p})

#Only for Employee
def manage_booking(request):
    if request.method == "GET":
        stmt = "SELECT * FROM book_room"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/manage_booking.html', {'reservations': r})
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
        stmt4 = "SELECT b_id FROM book_room NATURAL JOIN customer WHERE name = '"+p_name+"'"
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

        return render(request, 'travel/manage_booking.html', {'reservations': r})

def booking_detail(request, b_id, h_id, r_id):
    if request.method == "POST":
        stmt = "SELECT * FROM book_room WHERE b_id = "+str(b_id)+" AND h_id = "+str(h_id)+" AND r_number = "+str(r_id)+";"
        stmt1 = "SELECT no_of_people FROM booking WHERE b_id = "+str(b_id)+";"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchone()
        cursor.execute(stmt1)
        no_of_people = cursor.fetchone()[0]
        cursor.close()
        context = {
            'res_code':r[0],
            'hotel_id':r[1],
            'start':r[2],
            'end':r[3],
            'c_id':r[4],
            'r_id':r[6],
            'status':r[7],
            'comment':r[8],
            'people':no_of_people,
        }
        return render(request, 'travel/update_booking.html', {'context': context})

def update_booking(request):
    if request.method == "POST":
        post = request.POST
        cursor = connection.cursor()
        comment = request.POST.get("comment", "")
        stmt = "SELECT u_id FROM Employee where username = '"+request.session['username']+"';"
        cursor.execute(stmt)
        e_id = cursor.fetchone()[0]
        stmt  = "UPDATE book_room SET b_start_date = '"+str(post['check_in'])+"', b_end_date = '"+str(post['check_out'])+"', explanation = '"+comment+"', is_accepted = "+post['is_accepted']+", e_id = '"+str(e_id)+"' WHERE h_id = "+post['hotel_id']+" AND b_id = "+post['b_id']+" AND r_number = "+post['r_id']+";"
        cursor.execute(stmt)
        connection.commit()
        stmt = "UPDATE booking SET b_start_date = '"+str(post['check_in'])+"', b_end_date = '"+str(post['check_out'])+"', no_of_people = "+str(post['number'])+" WHERE b_id = "+str(post['b_id'])+";"
        cursor.execute(stmt)
        connection.commit()
        cursor.close()
        context = {

        }
        return HttpResponseRedirect(reverse('travel:manage_booking'))

def manage_reservation(request):
    if request.method == "GET":
        stmt = "SELECT * FROM reserves"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        print(r)
        return render(request, 'travel/manage_reservation.html', {'reservations': r})
    else:
        post = request.POST
        check_in = post["check_in"]
        check_out = post["check_out"]
        res_code = post["res_code"]
        rating = post["rating"]
        p_name = post["p_name"]
        ok = False
        stmt = ""
        stmt1 = "SELECT t_id FROM reserves WHERE t_id = "+ res_code
        stmt2 = "SELECT t_id FROM reserves WHERE t_start_date = '"+ check_in +"' AND t_end_date = '" + check_out+"'"
        stmt3 = "SELECT t_id FROM reserves NATURAL JOIN evaluate_tour WHERE t_rate = "+rating
        stmt4 = "SELECT t_id FROM reserves AS r JOIN customer AS c ON c.u_id = r.c_id WHERE name = '"+p_name+"'"
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
            stmt = "SELECT * FROM reserves where t_id IN("+stmt+");"

        else:
            stmt = "SELECT * FROM reserves"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchall()
        cursor.close()
        return render(request, 'travel/manage_reservation.html', {'reservations': r})

def reservation_detail(request,t_id,e_id,c_id, r_id):
    if request.method == "POST":
        stmt = "SELECT * FROM reserves WHERE r_id = "+str(r_id)+" AND t_id = "+str(t_id)+" AND c_id = "+str(c_id)+" AND e_id = "+str(e_id)+";"
        cursor = connection.cursor()
        cursor.execute(stmt)
        r = cursor.fetchone()
        cursor.close()
        context = {
            'r_id':r[0],
            't_id':r[1],
            'start':r[2],
            'end':r[3],
            'e_id':r[4],
            'c_id':r[5],
            'comment':r[6],
            'status':r[7]
        }
        return render(request, 'travel/reservation_detail.html', {'context': context})

def update_reservation(request):
    if request.method == "POST":
            post = request.POST
            cursor = connection.cursor()
            comment = request.POST.get("comment", "")
            stmt = "SELECT u_id FROM Employee where username = '"+request.session['username']+"';"
            cursor.execute(stmt)
            e_id = cursor.fetchone()[0]
            #######################################################################
            # e_id SHOULDN'T be a primary key in reserves, as it is not in book_room #
            #######################################################################
            stmt  = "UPDATE reserves SET t_start_date = '"+str(post['check_in'])+"', t_end_date = '"+str(post['check_out'])+"', explanation = '"+comment+"', is_accepted = "+post['is_accepted']+" WHERE t_id = "+post['t_id']+" AND r_id = "+post['r_id']+" AND c_id = "+post['c_id']+";"
            cursor.execute(stmt)
            connection.commit()
            cursor.close()
            context = {

            }
            return HttpResponseRedirect(reverse('travel:manage_reservation'))

def login(request):
    if request.method == 'POST':
        # get username and password from front-end
        post = request.POST
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        t = request.POST.get("type", "")
        # check if user exists if exists and password is correct send to index, if not show a warning
        try:
            stmt = "SELECT u_id, username, pw FROM " + t + " WHERE username = '" + username + "' AND pw = '" + password +"'"
            cursor = connection.cursor()
            cursor.execute(stmt)
            r = cursor.fetchone()
            cursor.close()
        except:
            print("db not exist")
            return render(request, 'travel/Login.html')


        if (r != None):
            request.session['username'] = username
            request.session['u_id'] = r[0]
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
    stmt = "SELECT h_id, max(h_rate_unq) FROM (SELECT h_id, h_rate_unq FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id));"
    cursor = connection.cursor()
    cursor.execute(stmt)
    mx = cursor.fetchone()
    cursor.close()
    stmt = "SELECT h_id, min(h_rate_unq) FROM (SELECT h_id, h_rate_unq FROM (SELECT h_id, SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id));"
    cursor = connection.cursor()
    cursor.execute(stmt)
    mn = cursor.fetchone()
    stmt = "SELECT h_id, h_name, h_rate_unq FROM (SELECT h_id, h_name,SUM(h_rate)/COUNT(h_rate) AS h_rate_unq FROM hotel NATURAL JOIN evaluate_hotel GROUP BY h_id);"
    cursor = connection.cursor()
    cursor.execute(stmt)
    all_rating = cursor.fetchall()
    return render(request, 'travel/Statistics.html', {'max': mx,'min':mn,'all':all_rating})

def delete_account(request):
    print("inside delete")
    u_id = request.session['u_id']
    print(request.session['type'])
    stmt = "DELETE FROM '"+request.session['type']+"' WHERE u_id = "+str(u_id)+";"
    cursor = connection.cursor()
    request.session.flush()
    cursor.execute(stmt)
    cursor.close()
    connection.commit()
    return HttpResponseRedirect(reverse('travel:login'))

def guide_tours1(request):
    return render(request, 'travel/guide_tours.html')
