INSERT INTO Plcie (plec, plec_skrot) VALUES
('Mezczyzna', 'M'),
('Kobieta', 'K');

INSERT INTO Reprezentanci_zawodnikow (imie, nazwisko, adres_email) VALUES
('Marek', 'Zielinski', 'marek.zielinski@example.com'),
('Ewa', 'Kowalczyk', 'ewa.kowalczyk@example.com'),
('Tomasz', 'Wroblewski', 'tomasz.wroblewski@example.com'),
('Agnieszka', 'Mazur', 'agnieszka.mazur@example.com');

INSERT INTO Konkurencje (nazwa) VALUES
('Skok w dal'),
('Rzut oszczepem'),
('Rzut dyskiem'),
('Skok wzwyz'),
('Pchnięcie kulą');

INSERT INTO Panstwa (nazwa, kod_iso, kontynent, stolica) VALUES
('Polska', 'POL', 'Europa', 'Warszawa'),
('Niemcy', 'DEU', 'Europa', 'Berlin'),
('USA', 'USA', 'Ameryka Północna', 'Waszyngton'),
('Japonia', 'JPN', 'Azja', 'Tokio'),
('Brazylia', 'BRA', NULL, 'Brasília'),
('Australia', 'AUS', 'Oceania', NULL),
('Kanada', 'CAN', NULL, NULL);

INSERT INTO Trenerzy (imie, nazwisko, adres_email) VALUES
('Adam', 'Nowicki', 'adam.nowicki@example.com'),
('Beata', 'Wojcik', 'beata.wojcik@example.com'),
('Cezary', 'Kaczmarek', 'cezary.kaczmarek@example.com');

INSERT INTO Zawodnicy (imie, nazwisko, data_urodzenia, id_plci, id_panstwa,id_reprezentanta) VALUES
('Jan', 'Kowalski', '1990-05-15', 1, 2, 1),
('Anna', 'Nowak', '1988-11-23', 2, 2, 2),
('Piotr', 'Wozniak', '1995-07-30', 1, 1, 1),
('Katarzyna', 'Lewandowska', '1992-03-12', 2, 2, NULL),
('Michał', 'Szymanski', '1985-09-05', 1, 7, 3),
('Magdalena', 'Krol', '1993-12-19', 2, 6, NULL);

INSERT INTO Rekordy_zyciowe (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy) VALUES
(1, 3, 56.78, '2021-06-15', 850),
(2, 1, 6.45, '2020-08-20', 920),
(3, 2, 75.32, '2019-05-10', 780),
(4, 4, 1.92, '2022-03-25', 880),
(5, 5, 18.67, '2018-11-30', 760),
(6, 1, 5.98, '2021-09-12', 810);

INSERT INTO Trenerzy_zawodnicy (id_trenera, id_zawodnika) VALUES
(1, 1),
(1, 3),
(2, 2),
(2, 4);

INSERT INTO Rekordy_swiata (id_konkurencji, rezultat, data_rezultatu, id_zawodnika) VALUES
(1, 8.95, '1991-08-30', 2),
(2, 98.48, '1986-05-20', 3),
(3, 74.08, '1986-05-20', 5),
(4, 2.45, '1993-07-27', 4);

INSERT INTO Stadiony (nazwa, miasto,id_panstwa) VALUES
('Stadion Narodowy', 'Warszawa', 1),
('Allianz Arena', 'Monachium', 2),
('Olympic Stadium', 'Berlin', 3),
('Tokyo National Stadium', 'Tokio', 4),
('Maracana Stadium', 'Rio de Janeiro', 5);

INSERT INTO Zawody (nazwa, data_rozpoczecia, data_zakonczenia, id_panstwa, id_stadiony) VALUES
('Mistrzostwa Europy 2022', '2022-08-10', '2022-08-20', 2, 2),
('Igrzyska Olimpijskie 2023', '2023-07-15', '2023-07-30', 4, 4),
('Mistrzostwa Swiata 2021', '2021-09-01', '2021-09-15', 3, 3),
('Grand Prix 2022', '2022-05-05', '2022-05-10', 6, 3);

INSERT INTO Statusy_wynikow (status_wyniku) VALUES
('zakwalifikowany'),
('niezakwalifikowany'),
('dyskwalifikowany'),
('nieukończony');

INSERT INTO Wyniki (id_zawodnika, id_konkurencji, id_zawody, rezultat, miejsce, id_statusu, data_rezultatu) VALUES
(1, 3, 1, 57.12, 2, 1, '2022-08-15'),
(2, 1, 1, 6.50, 1, 1, '2022-08-16'),
(3, 2, 2, 76.00, 3, 2, '2023-07-20'),
(4, 4, 2, NULL, NULL, 3, '2023-07-22'),
(5, 5, 3, NULL, 5, 4, '2021-09-05'),
(6, 1, 4, 6.00, 6, 1, '2022-05-07');