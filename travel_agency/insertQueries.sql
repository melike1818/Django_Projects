INSERT INTO guide (u_id, name, username, phone, pw, g_salary, g_points, g_rating)
VALUES
       (1, 'Ahmet', 'ahmet', 5398743564, '123', 100, null, null),
       (2, 'Ceyda', 'ceyda', 5324563421, '123', 100, null, null),
       (3, 'Ayşe', 'ayse', 5324563421, '123', 100, null, null),
       (4, 'Mustafa', 'mustafa', 5324563421, '123', 100, null, null),
       (5, 'Hazal', 'hazal', 5324563421, '123', 100, null, null),
       (6, 'Berkay', 'berkay', 5324563421, '123', 100, null, null);

INSERT INTO tour (t_id, t_name, t_start_date, t_end_date, t_start_location, t_description, t_price, t_rating,
                  t_capacity)
VALUES
       (1, 'Karadeniz', '2022-01-03', '2022-01-12', 'Artvin', 'Yayla', 300, null, 100),
       (2, 'Buzpateni', '2022-01-03', '2022-01-03', 'Bahçelievler', 'This is tour description', 50, null, 100),
       (3, 'Göbeklitepe', '2022-01-05', '2022-01-06', 'Urfa', 'Tarihi gezi', 350, null, 100),
       (4, 'Piknik', '2022-01-04', '2022-01-04', 'Kızılcahamam', 'Mangal, orman havası', 150, null, 100),
       (5, 'Bodrum Kalesi', '2022-05-12', '2022-01-12', 'Bodrum', 'Tarihi gezi', 300, null, 100),
       (6, 'Sörf', '2022-03-05', '2022-03-10', 'Alaçatı', 'Spor, hobi', 400, null, 100),
       (7, 'Şarap Tadımı', '2022-01-08', '2022-01-10', 'Ayvalık', 'Lezzet Turu', 200, null, 100),
       (8, 'Koç Müzesi', '2022-01-05', '2022-01-06', 'İstanbul', 'Müze gezisi', 100, null, 100);

INSERT INTO employee (u_id, name, username, phone, pw, e_salary)
VALUES
       (1, 'tanay', 'tanay', null, '123', null),
       (2, 'kimya', 'kimya', null, '123', null),
       (3, 'ırmak', 'ırmak', null, '123', null),
       (4, 'melike', 'melike', null, '123', null),
       (5, 'can', 'can', null, '123', null);

INSERT INTO customer (u_id, name, username, phone, pw, e_salary)
VALUES
       (6, 'ırmo', 'iii', null, null, null, 10000, 'asdf', null),

INSERT INTO assign (t_id, t_start_date, t_end_date, g_id, e_id, accepted)
VALUES
       (3, '2022-01-05', '2022-01-06', 2, 2, null),
       (4, '2022-01-04', '2022-01-04', 4, 1, null),
       (7, '2022-01-08', '2022-01-10', 2, 2, null);


INSERT INTO activity (a_id, a_date, a_capacity, a_name) 
VALUES 
       ('1', '2022-01-03', '10', 'fruit collection'),
       ('2', '2022-01-03', '5', 'walk'),
       ('3', '2022-01-05', '50', 'church visit'),
       ('4', '2022-01-04', '8', 'voleyball'),
       ('5', '2022-05-12', '70', 'castle visit'),
       ('6', '2022-03-05', '10', 'wind surf'),
       ('7', '2022-01-08', '10', 'kebap'),
       ('8', '2022-01-05', '80', 'dolmabahçe'),
       ('9', '2022-01-05', '80', 'arkeoloji');

INSERT INTO places_activities (t_id, t_start_date, t_end_date, a_id, a_date, p_id, num_customer) 
VALUES 
       ('1', '2022-01-03', '2022-01-12', '1', '2022-01-03', '1', '0'),
       ('2', '2022-01-03', '2022-01-03', '2', '2022-01-03', '2', '0'),
       ('3', '2022-01-05', '2022-01-06', '3', '2022-01-05', '1', '0'),
       ('4', '2022-01-04', '2022-01-04', '4', '2022-01-04', '1', '0'),
       ('5', '2022-05-12', '2022-05-12', '5', '2022-05-12', '1', '0'),
       ('6', '2022-03-05', '2022-03-10', '6', '2022-03-05', '2', '0'),
       ('7', '2022-01-08', '2022-01-10', '7', '2022-01-08', '1', '0'),
       ('8', '2022-01-05', '2022-01-06', '8', '2022-01-05', '1', '0'),
       ('8', '2022-01-05', '2022-01-06', '9', '2022-01-05', '2', '0');

INSERT INTO extra_activity (a_id, a_date, price) 
VALUES 
       ('9', '2022-01-05', '10');

INSERT INTO hotel ("h_id","h_name","h_address","h_description","h_phone","h_capacity") 
VALUES
       (1, 'hilton', 'ankara', 'bisey bisey', '123', 300),
       (2, 'hilton', 'izmir', 'bisey bisey', '123', 100),
       (3, 'hilton', 'bodrum', 'bisey bisey', '123', 200),
       (4, 'aasad', 'Corum', 'bisey bisey', '123', 350),
       (5, 'asjkfg', 'London', 'description', '123', 3000),
       (6, 'sdgsd', 'ankara', 'bisey bisey', '123', 300),
       (7, 'fhdh', 'ankara', 'bisey bisey', '123', 300),
       (8, 'dhfh', 'ankara', 'bisey bisey', '123', 300);

INSERT INTO room ("h_id","r_number","bed_capacity","r_type","r_price")
VALUES
       (1, 1, 2, 'bisey bisey', 300),
       (1, 2, 3, 'bisey bisey', 100),
       (1, 3, 3, 'bisey bisey', 200),
       (2, 1, 1, 'bisey bisey', 350),
       (2, 2, 2, 'description', 3000),
       (2, 3, 2, 'bisey bisey', 300),
       (2, 4, 5, 'bisey bisey', 300),
       (2, 5, 5, 'bisey bisey', 300);



