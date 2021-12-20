DROP TABLE IF EXISTS general_user;
DROP TABLE IF EXISTS book_flights;
DROP TABLE IF EXISTS evaluate_guide;
DROP TABLE IF EXISTS evaluate_hotel;
DROP TABLE IF EXISTS book_room;
DROP TABLE IF EXISTS reserves;
DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS evaluate_tour;
DROP TABLE IF EXISTS buys;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS guide;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS includes;
DROP TABLE IF EXISTS places_activities;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS extra_activities;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS hotel;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS tour;
DROP TABLE IF EXISTS assign;


CREATE TABLE tour (t_id INT, 
t_start_date DATE, 
t_end_date DATE, 
t_start_location VARCHAR(10), 
t_description VARCHAR(50), 
t_price INT,
t_rating INT,
t_capacity INT, 
PRIMARY KEY (t_id,t_start_date, t_end_date));

CREATE TABLE general_user (
u_id INT NOT NULL, 
name CHAR(50),
username CHAR(20),
pw VARCHAR(50),
phone NUMERIC(11,0),
PRIMARY KEY (u_id));

CREATE TABLE customer (u_id INT, 
name CHAR(50),
username CHAR(20),
c_bdate Date, 
c_address VARCHAR(50), 
c_sex CHAR(10), 
c_wallet INT,
pw NUMERIC(11,0),
phone INT, 
PRIMARY KEY (u_id));

CREATE TABLE employee (u_id INT,
name CHAR(50),
username CHAR(20),
phone INT,
pw NUMERIC(11,0),
e_salary INT, 
PRIMARY KEY (u_id));

CREATE TABLE guide(u_id INT, 
name VARCHAR(50),
username CHAR(20), 
phone INT, 
pw NUMERIC(11,0), 
g_salary INT,
g_rating INT,
PRIMARY KEY (u_id));

CREATE TABLE booking (b_id INT, 
b_start_date DATE,
b_end_date DATE,
no_of_people INT,
PRIMARY KEY (b_id, b_start_date, b_end_date));

CREATE TABLE places (p_id INT, 
p_name VARCHAR(8), 
p_location VARCHAR(50), 
PRIMARY KEY (p_id));

CREATE TABLE activities (a_id INT,
a_date Date, 
a_capacity INT, 
a_name VARCHAR(20), 
PRIMARY KEY (a_id, a_date));

CREATE TABLE extra_activities (a_id INT, 
a_date Date, 
a_capacity INT, 
a_name VARCHAR(20), 
price INT, 
PRIMARY KEY (a_id, a_date));

CREATE TABLE hotel(h_id INT, 
h_name VARCHAR(50), 
h_address VARCHAR(50),
h_phone NUMERIC(11,0),
h_capacity INT, 
PRIMARY KEY (h_id));

CREATE TABLE room(h_id INT, 
r_number INT, 
bed_capacity INT, 
r_type CHAR(12), 
r_price INT, 
PRIMARY KEY (h_id, r_number), 
FOREIGN KEY (h_id) REFERENCES hotel(h_id) );

CREATE TABLE flights(f_id INT, 
f_date DATE, 
f_price INT, 
f_departure VARCHAR(50),
f_arrival VARCHAR(50), 
PRIMARY KEY (f_id, f_date));

CREATE TABLE reservation(r_id INT, 
t_id INT,
t_start_date DATE, 
t_end_date DATE, 
u_id INT, 
b_id INT, 
b_start_date DATE, 
b_end_date DATE, 
r_start_date DATE, 
r_end_date DATE, 
r_price INT, 
r_customer_num INT,
PRIMARY KEY (r_id), 
FOREIGN KEY (t_id, t_start_date, t_end_date) REFERENCES tour(t_id, t_start_date, t_end_date), 
FOREIGN KEY (u_id) REFERENCES customer(u_id), 
FOREIGN KEY (b_id, b_start_date, b_end_date) REFERENCES booking(b_id, b_start_date, b_end_date));

CREATE TABLE evaluate_guide ( g_id INT,
c_id INT,
g_comment CHAR(50),
g_rate INT,
PRIMARY KEY(g_id, c_id),
FOREIGN KEY(g_id) REFERENCES guide(u_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id));

CREATE TABLE evaluate_tour ( t_id INT,
t_start_date DATE,
t_end_date DATE,
c_id INT,
t_comment CHAR(50),
t_rate INT,
PRIMARY KEY(t_id, t_start_date, t_end_date,c_id),
FOREIGN KEY(t_id, t_start_date, t_end_date) REFERENCES tour(t_id, t_start_date, t_end_date),
FOREIGN KEY(c_id) REFERENCES customer(u_id) );

CREATE TABLE evaluate_hotel ( h_id INT,
c_id INT,
h_comment CHAR(50),
h_rate INT,
PRIMARY KEY(h_id, c_id),
FOREIGN KEY(h_id) REFERENCES hotel(h_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id) );

CREATE TABLE buys ( receipt_id INT,
a_id INT,
a_date DATE,
price INT,
c_id INT,
PRIMARY KEY(receipt_id),
FOREIGN KEY(a_id, a_date) REFERENCES extra_activities(a_id, a_date),
FOREIGN KEY(c_id) REFERENCES customer(u_id) );

CREATE TABLE reserves ( r_id INT, 
t_id INT,
t_start_date DATE,
t_end_date DATE,
b_start_date DATE,
b_end_date DATE,
b_id INT, 
e_id INT,
c_id INT,
explanation CHAR(50),
is_accepted BOOLEAN,
PRIMARY KEY(r_id, e_id, c_id),
FOREIGN KEY(r_id) REFERENCES reservation(r_id),
FOREIGN KEY(t_id, t_start_date, t_end_date) REFERENCES tour(t_id, t_start_date, t_end_date),
FOREIGN KEY(b_id, b_start_date, b_end_date) REFERENCES booking(b_id, b_start_date, b_end_date), 
FOREIGN KEY(e_id) REFERENCES employee(u_id), 
FOREIGN KEY(c_id) REFERENCES customer(u_id) );

CREATE TABLE includes ( h_id INT, 
r_number INT, 
PRIMARY KEY(h_id, r_number),
FOREIGN KEY(h_id) REFERENCES hotel(h_id),
FOREIGN KEY(h_id, r_number) REFERENCES room(h_id, r_number) );

CREATE TABLE book_room ( b_id INT,
b_start_date DATE,
b_end_date DATE,
c_id INT,
h_id INT, 
e_id INT,
r_number INT,
is_accepted BOOLEAN,
explanation CHAR(250),
PRIMARY KEY(b_id, b_start_date, b_end_date, h_id, r_number, c_id, e_id),
FOREIGN KEY(b_id, b_start_date, b_end_date) REFERENCES booking(b_id, b_start_date, b_end_date),
FOREIGN KEY(h_id) REFERENCES hotel(h_id),
FOREIGN KEY(h_id, r_number) REFERENCES room(h_id,r_number),
FOREIGN KEY(c_id) REFERENCES customer(u_id),
FOREIGN KEY(e_id) REFERENCES employee(u_id) );

CREATE TABLE book_flights ( f_id INT,
f_date DATE,
c_id INT,
e_id INT,
f_booking_id INT,
is_accepted BOOLEAN,
explanation CHAR(250),
PRIMARY KEY(f_booking_id),
FOREIGN KEY(f_id,f_date) REFERENCES flights(f_id, f_date),
FOREIGN KEY(c_id) REFERENCES customer(u_id),
FOREIGN KEY(e_id) REFERENCES employee(u_id) );

CREATE TABLE  places_activities ( t_id INT,
t_start_date Date,
t_end_date Date,
a_id INT,
a_date DATE,
p_id INT,
num_customer INT,
PRIMARY KEY(t_id, t_start_date, t_end_date, a_id, a_date, p_id),
FOREIGN KEY(t_id, t_start_date, t_end_date) REFERENCES tour(t_id, t_start_date, t_end_date),
FOREIGN KEY(a_id, a_date) REFERENCES activities(a_id, a_date),
FOREIGN KEY(p_id) REFERENCES places(p_id));

CREATE TABLE  feedback ( t_id INT, 
t_start_date DATE, 
t_end_date DATE, 
g_id INT,
f_text VARCHAR(250),
PRIMARY KEY(t_id, t_start_date, t_end_date, g_id),
FOREIGN KEY(t_id, t_start_date, t_end_date) REFERENCES tour(t_id, t_start_date, t_end_date),
FOREIGN KEY(g_id) REFERENCES guide(u_id));

CREATE TABLE  assign ( t_id INT, 
t_start_date DATE, 
t_end_date DATE, 
g_id INT,
e_id INT,
accepted BOOLEAN,
PRIMARY KEY(t_id, t_start_date, t_end_date, g_id, e_id),
FOREIGN KEY(t_id,t_start_date, t_end_date) REFERENCES tour(t_id, t_start_date, t_end_date),
FOREIGN KEY(e_id) REFERENCES employee(u_id);