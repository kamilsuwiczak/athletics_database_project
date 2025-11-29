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
('Ewa', 'Kowalczyk', 'ewa.kowalczyk@example.com');

INSERT INTO Panstwa (nazwa, kod_iso, kontynent, stolica) VALUES
('Polska', 'POL', 'Europa', 'Warszawa'),
('Niemcy', 'DEU', 'Europa', 'Berlin'),
('USA', 'USA', 'Ameryka Północna', 'Waszyngton'),
('Japonia', 'JPN', 'Azja', 'Tokio');

INSERT INTO Trenerzy (imie, nazwisko, adres_email) VALUES
('Adam', 'Nowicki', 'adam.nowicki@example.com'),
('Beata', 'Wojcik', 'beata.wojcik@example.com');

INSERT INTO Zawodnicy (imie, nazwisko, data_urodzenia, id_plci, id_panstwa,id_reprezentanta) VALUES
('Jan', 'Kowalski', '1990-05-15', 1, 2, 1),
('Anna', 'Nowak', '1988-11-23', 2, 2, 2),
('Piotr', 'Wozniak', '1995-07-30', 1, 1, 1),
('Katarzyna', 'Lewandowska', '1992-03-12', 2, 2, 2);
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