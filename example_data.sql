-- ======== PLCIE ========
INSERT INTO Plcie (plec, plec_skrot) VALUES
('Mezczyzna', 'M'),
('Kobieta', 'K');

-- ======== REPREZENTANCI ZAWODNIKÓW ========
INSERT INTO Reprezentanci_zawodnikow (imie, nazwisko, adres_email) VALUES
('Adam', 'Nowak', 'adam.nowak@example.com'),
('Ewa', 'Kowalska', 'ewa.kowalska@example.com'),
('Piotr', 'Lewandowski', 'piotr.lew@example.com');

-- ======== KONKURENCJE ========
INSERT INTO Konkurencje (nazwa, rodzaj) VALUES
('100m', 'Bieg'),
('200m', 'Bieg'),
('Skok w dal', 'Skok');

-- ======== PAŃSTWA ========
INSERT INTO Panstwa (kod_iso, nazwa, kontynent, stolica) VALUES
('POL', 'Polska', 'Europa', 'Warszawa'),
('USA', 'Stany Zjednoczone', 'Ameryka Północna', 'Waszyngton'),
('JPN', 'Japonia', 'Azja', 'Tokio');

-- ======== TRENERZY ========
INSERT INTO Trenerzy (imie, nazwisko, adres_email) VALUES
('Marek', 'Zielinski', 'marek.z@example.com'),
('John', 'Smith', 'john.smith@example.com');

-- ======== ZAWODNICY ========
INSERT INTO Zawodnicy (imie, nazwisko, data_urodzenia, plec, id_reprezentanta, kod_iso_panstwa) VALUES
('Kamil', 'Kowalski', '1998-05-12', 'Mezczyzna', 1, 'POL'),
('Anna', 'Nowak', '2000-03-22', 'Kobieta', 2, 'POL'),
('Robert', 'Johnson', '1995-07-10', 'Mezczyzna', 3, 'USA');

-- ======== REKORDY ŻYCIOWE ========
INSERT INTO Rekordy_zyciowe (id_zawodnika, nazwa_konkurencji, rezultat, data_rezultatu, wynik_punktowy) VALUES
(1, '100m', 10.75, '2023-06-10', 950),
(1, '200m', 21.90, '2023-07-15', 900),
(2, '100m', 11.80, '2023-08-01', 880),
(3, 'Skok w dal', 7.45, '2023-04-14', 890);

-- ======== TRENERZY–ZAWODNICY ========
INSERT INTO Trenerzy_zawodnicy (id_trenera, id_zawodnika) VALUES
(1, 1),
(1, 2),
(2, 3);

-- ======== REKORDY ŚWIATA ========
INSERT INTO Rekordy_swiata (nazwa_konkurencji, id_zawodnika, rezultat, data_rezultatu) VALUES
('100m', 3, 9.58, '2009-08-16'),
('Skok w dal', 3, 8.95, '2020-06-12');

-- ======== STADIONY ========
INSERT INTO Stadiony (nazwa, miasto, nazwa_panstwa) VALUES
('PGE Narodowy', 'Warszawa', 'POL'),
('Olympic Stadium', 'Tokio', 'JPN'),
('Hayward Field', 'Eugene', 'USA');

-- ======== ZAWODY ========
INSERT INTO Zawody (nazwa, data_rozpoczecia, data_zakonczenia, id_panstwa, id_stadionu) VALUES
('Mistrzostwa Polski', '2024-05-10', '2024-05-12', 'POL', 1),
('Tokyo Open', '2024-06-20', '2024-06-22', 'JPN', 2),
('US Trials', '2024-07-05', '2024-07-07', 'USA', 3);

-- ======== STATUSY WYNIKÓW ========
INSERT INTO Statusy_wynikow (status_wyniku) VALUES
('Zatwierdzony'),
('Dyskwalifikacja'),
('Niewazny');

-- ======== WYNIKI ========
INSERT INTO Wyniki (
    id_zawodnika, nazwa_konkurencji, nazwa_zawody, data_rozpoczecia_zawody, 
    status_wyniku, rezultat, miejsce, data_rezultatu
) VALUES
(1, '100m', 'Mistrzostwa Polski', '2024-05-10', 'Zatwierdzony', 10.80, 1, '2024-05-10'),
(2, '100m', 'Mistrzostwa Polski', '2024-05-10', 'Zatwierdzony', 11.95, 2, '2024-05-10'),
(3, 'Skok w dal', 'US Trials', '2024-07-05', 'Zatwierdzony', 7.30, 1, '2024-07-05'),
(1, '200m', 'Tokyo Open', '2024-06-20', 'Dyskwalifikacja', NULL, NULL, '2024-06-20');
