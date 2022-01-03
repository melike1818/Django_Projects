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
       (1, 'Karadeniz', '2022-01-03', '2022-01-12', 'Artvin', 'Yayla', 300, null, null),
       (2, 'Buzpateni', '2022-01-03', '2022-01-03', 'Bahçelievler', 'This is tour description', 50, null, null),
       (3, 'Göbeklitepe', '2022-01-05', '2022-01-06', 'Urfa', 'Tarihi gezi', 350, null, null),
       (4, 'Piknik', '2022-01-04', '2022-01-04', 'Kızılcahamam', 'Mangal, orman havası', 150, null, null),
       (5, 'Bodrum Kalesi', '2022-05-12', '2022-01-12', 'Bodrum', 'Tarihi gezi', 300, null, null),
       (6, 'Sörf', '2022-03-05', '2022-03-10', 'Alaçatı', 'Spor, hobi', 400, null, null),
       (7, 'Şarap Tadımı', '2022-01-08', '2022-01-10', 'Ayvalık', 'Lezzet Turu', 200, null, null),
       (8, 'Koç Müzesi', '2022-01-05', '2022-01-06', 'İstanbul', 'Müze gezisi', 100, null, null);

INSERT INTO employee (u_id, name, username, phone, pw, e_salary)
VALUES
       (1, 'tanay', 'tanay', null, '123', null),
       (2, 'kimya', 'kimya', null, '123', null),
       (3, 'ırmak', 'ırmak', null, '123', null),
       (4, 'melike', 'melike', null, '123', null),
       (5, 'can', 'can', null, '123', null);

INSERT INTO assign (t_id, t_start_date, t_end_date, g_id, e_id, accepted)
VALUES
       (3, '2022-01-05', '2022-01-06', 2, 2, null),
       (4, '2022-01-04', '2022-01-04', 4, 1, null),
       (7, '2022-01-08', '2022-01-10', 2, 2, null);