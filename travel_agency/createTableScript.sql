DROP TABLE IF EXISTS book_flight;
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
DROP TABLE IF EXISTS has;
DROP TABLE IF EXISTS places_activities;
DROP TABLE IF EXISTS place;
DROP TABLE IF EXISTS activity;
DROP TABLE IF EXISTS extra_activity;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS hotel;
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS tour;
DROP TABLE IF EXISTS assign;

CREATE TABLE customer(
u_id INT NOT NULL,
name VARCHAR(50) NOT NULL,
username VARCHAR(50) NOT NULL,
c_bdate Date,
c_address VARCHAR(250),
c_sex VARCHAR(10),
c_wallet INT NOT NULL,
pw VARCHAR(50) NOT NULL,
phone NUMERIC(11,0),
PRIMARY KEY (u_id));

CREATE TABLE employee(
u_id INT NOT NULL,
name CHAR(50) NOT NULL,
username VARCHAR(50) NOT NULL,
phone NUMERIC(11,0),
pw VARCHAR(50) NOT NULL,
e_salary INT,
PRIMARY KEY (u_id));

CREATE TABLE guide(
u_id INT NOT NULL,
name CHAR(50) NOT NULL,
username VARCHAR(50) NOT NULL,
phone NUMERIC(11,0),
pw VARCHAR(50) NOT NULL,
g_salary INT,
g_points INT,
g_rating INT,
PRIMARY KEY (u_id));

CREATE TABLE booking(
b_id INT NOT NULL,
b_start_date DATE NOT NULL,
b_end_date DATE NOT NULL,
no_of_people INT,
PRIMARY KEY (b_id));

CREATE TABLE tour(
t_id INT NOT NULL,
t_name CHAR(50),
t_start_date DATE NOT NULL,
t_end_date DATE NOT NULL,
t_start_location VARCHAR(50),
t_description VARCHAR(250),
t_price INT,
t_rating INT,
t_capacity INT,
PRIMARY KEY (t_id));

CREATE TABLE place(
p_id INT NOT NULL,
p_name VARCHAR(50),
p_location VARCHAR(50),
PRIMARY KEY (p_id));

CREATE TABLE activity(
a_id INT NOT NULL,
a_date DATE NOT NULL,
a_capacity INT,
a_name VARCHAR(50),
PRIMARY KEY (a_id));

CREATE TABLE extra_activity(
a_id INT NOT NULL,
a_date DATE NOT NULL,
price INT,
PRIMARY KEY (a_id),
FOREIGN KEY (a_id) REFERENCES activity(a_id));

CREATE TABLE hotel(
h_id INT NOT NULL,
h_name VARCHAR(50),
h_address VARCHAR(50),
h_description VARCHAR(250),
h_phone NUMERIC(11,0),
h_capacity INT,
PRIMARY KEY (h_id));

CREATE TABLE room(
h_id INT NOT NULL,
r_number INT NOT NULL,
bed_capacity INT,
r_type CHAR(50),
r_price INT,
PRIMARY KEY (h_id, r_number),
FOREIGN KEY (h_id) REFERENCES hotel(h_id));

CREATE TABLE flight(
f_id INT NOT NULL,
f_date DATE NOT NULL,
f_price INT,
f_departure VARCHAR(50),
f_arrival VARCHAR(50),
PRIMARY KEY (f_id));

CREATE TABLE reservation(
r_id INT NOT NULL,
r_start_date DATE,
r_end_date DATE,
r_price INT,
r_customer_num INT,
PRIMARY KEY (r_id));

CREATE TABLE  evaluate_guide(
g_id INT NOT NULL,
c_id INT NOT NULL,
g_comment VARCHAR(50),
g_rate INT,
PRIMARY KEY(g_id, c_id),
FOREIGN KEY(g_id) REFERENCES guide(u_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id));

CREATE TABLE evaluate_tour(
t_id INT NOT NULL,
t_start_date DATE NOT NULL,
t_end_date DATE NOT NULL,
c_id INT NOT NULL,
t_comment CHAR(250),
t_rate INT,
PRIMARY KEY(t_id,  c_id),
FOREIGN KEY(t_id) REFERENCES tour(t_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id) );

CREATE TABLE evaluate_hotel(
h_id INT NOT NULL,
c_id INT NOT NULL,
h_comment CHAR(250),
h_rate INT,
PRIMARY KEY(h_id, c_id),
FOREIGN KEY(h_id) REFERENCES hotel(h_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id));

CREATE TABLE places_activities(
t_id INT NOT NULL,
t_start_date DATE NOT NULL,
t_end_date DATE NOT NULL,
a_id INT NOT NULL,
a_date DATE NOT NULL,
p_id INT NOT NULL,
num_customer INT,
PRIMARY KEY(t_id, a_id, p_id),
FOREIGN KEY(t_id) REFERENCES tour(t_id),
FOREIGN KEY(a_id) REFERENCES activity(a_id),
FOREIGN KEY(p_id) REFERENCES place(p_id));

CREATE TABLE buys(
receipt_id INT NOT NULL,
a_id INT,
a_date DATE,
c_id INT,
PRIMARY KEY(receipt_id),
FOREIGN KEY(a_id) REFERENCES extra_activity(a_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id));

CREATE TABLE reserves(
r_id INT NOT NULL,
t_id INT NOT NULL,
t_start_date DATE NOT NULL,
t_end_date DATE NOT NULL,
e_id INT NOT NULL,
c_id INT NOT NULL,
explanation CHAR(50),
is_accepted BOOLEAN,
PRIMARY KEY(t_id,e_id,c_id, r_id),
FOREIGN KEY(r_id) REFERENCES reservation(r_id),
FOREIGN KEY(t_id) REFERENCES tour(t_id),
FOREIGN KEY(e_id) REFERENCES employee(u_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id));

CREATE TABLE feedback(
t_id INT NOT NULL,
t_start_date DATE NOT NULL,
t_end_date DATE NOT NULL,
g_id INT NOT NULL,
f_text VARCHAR(250),
PRIMARY KEY(t_id, g_id),
FOREIGN KEY(t_id) REFERENCES tour(t_id),
FOREIGN KEY(g_id) REFERENCES guide(u_id));

CREATE TABLE assign(
t_id INT NOT NULL,
t_start_date DATE NOT NULL,
t_end_date DATE NOT NULL,
g_id INT NOT NULL,
e_id INT NOT NULL,
accepted BOOLEAN,
PRIMARY KEY(t_id, g_id, e_id),
FOREIGN KEY(t_id) REFERENCES tour(t_id),
FOREIGN KEY(e_id) REFERENCES employee(u_id),
FOREIGN KEY(g_id) REFERENCES guide(u_id));

CREATE TABLE  book_room(
b_id INT NOT NULL,
h_id INT NOT NULL,
b_start_date DATE NOT NULL,
b_end_date DATE NOT NULL,
c_id INT,
e_id INT,
r_number INT NOT NULL,
is_accepted BOOLEAN,
explanation CHAR(250),
PRIMARY KEY(b_id, h_id, r_number),
FOREIGN KEY(b_id) REFERENCES booking(b_id),
FOREIGN KEY(h_id, r_number) REFERENCES room(h_id, r_number),
FOREIGN KEY(c_id) REFERENCES customer(u_id),
FOREIGN KEY(e_id) REFERENCES employee(u_id));

CREATE TABLE book_flight(
f_booking_id INT NOT NULL,
f_id INT NOT NULL,
f_date DATE NOT NULL,
c_id INT,
e_id INT,
is_accepted BOOLEAN,
explanation CHAR(250),
PRIMARY KEY(f_booking_id, f_id),
FOREIGN KEY(f_id) REFERENCES flight(f_id),
FOREIGN KEY(c_id) REFERENCES customer(u_id),
FOREIGN KEY(e_id) REFERENCES employee(u_id));

CREATE TABLE has(
r_id INT NOT NULL,
b_id INT NOT NULL,
b_start_date DATE NOT NULL,
b_end_date DATE NOT NULL,
PRIMARY KEY(r_id, b_id),
FOREIGN KEY(r_id) REFERENCES reservation(r_id),
FOREIGN KEY(b_id) REFERENCES booking(b_id));
