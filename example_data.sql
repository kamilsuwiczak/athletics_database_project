INSERT INTO Plcie (plec, plec_skrot) VALUES
('Mezczyzna', 'M'),
('Kobieta', 'K');

INSERT INTO Konkurencje (nazwa) VALUES
('100m sprint'),
('200m sprint'),
('Maraton'),
('Skok w dal');

INSERT INTO Reprezentanci_zawodnikow (imie, nazwisko, adres_email) VALUES
('Marek', 'Zielinski', 'marek.zielinski@example.com'),
('Ewa', 'Kowalczyk', 'ewa.kowalczyk@example.com'),
('Tomasz', 'Wroblewski', 'tomasz.wroblewski@example.com');

INSERT INTO Panstwa (nazwa, kod_iso, kontynent, stolica) VALUES
('Polska', 'POL', 'Europa', 'Warszawa'),
('Niemcy', 'DEU', 'Europa', 'Berlin'),
('USA', 'USA', 'Ameryka Północna', 'Waszyngton'),
('Japonia', 'JPN', 'Azja', 'Tokio');

INSERT INTO Trenerzy (imie, nazwisko, adres_email) VALUES
('Adam', 'Nowicki', 'adam.nowicki@example.com'),
('Beata', 'Wojcik', 'beata.wojcik@example.com'),
('Cezary', 'Kaczmarek', 'cezary.kaczmarek@example.com');

INSERT INTO Zawodnicy (imie, nazwisko, data_urodzenia, id_plci, id_panstwa,id_reprezentanta) VALUES
('Jan', 'Kowalski', '1990-05-15', 1, 2, 1),
('Anna', 'Nowak', '1988-11-23', 2, 2, 2),
('Piotr', 'Wozniak', '1995-07-30', 1, 1, 1),
('Katarzyna', 'Lewandowska', '1992-03-12', 2, 2, 2);

INSERT INTO Rekordy_zyciowe (id_zawodnika, id_konkurencji, rezultat, data_ustanowienia, wynik_punktowy) VALUES
(1, 3, '2:10:45', '2022-04-10', 950.50),
(2, 1, '11.25s', '2021-06-15', 880.00),
(3, 1, '10.85s', '2023-05-20', 920.75),
(4, 4, '6.75m', '2020-08-30', 870.25);

INSERT INTO Stadiony (nazwa, id_panstwa) VALUES
('Stadion Narodowy', 1),
('Allianz Arena', 2),
('Olympic Stadium', 3);

INSERT INTO Zawody (nazwa, data_rozpoczecia, data_zakonczenia, id_panstwa, id_stadiony) VALUES
('Mistrzostwa Europy 2022', '2022-08-11', '2022-08-21', 1, 1),
('Mistrzostwa Świata 2023', '2023-07-15', '2023-07-25', 2, 2),
('Igrzyska Olimpijskie 2024', '2024-07-26', '2024-08-11', 3, 3);

INSERT INTO Wyniki (id_zawodnika, id_konkurencji, id_zawody, rezultat, miejsce, status_wyniku, data_rezultatu) VALUES
(1, 3, 1, '2:11:30', 2, 'zakwalifikowany', '2022-08-15'),
(2, 1, 1, '11.30s', 3, 'zakwalifikowany', '2022-08-16'),
(3, 1, 2, '10.90s', 1, 'zakwalifikowany', '2023-07-18'),
(4, 4, 2, '6.80m', 2, 'zakwalifikowany', '2023-07-20');

INSERT INTO Trenerzy_zawodnicy (id_trenera, id_zawodnika) VALUES
(1, 1),
(1, 3),
(2, 2),
(2, 4);

INSERT INTO Rekordy_swiata (id_konkurencji, rezultat, data_ustanowienia, id_zawodnika) VALUES
(1, '9.58s', '2009-08-16', 3),
(2, '19.19s', '2009-08-20', 3),
(3, '2:01:39', '2019-09-29', 1),
(4, '8.95m', '1991-08-30', 4);