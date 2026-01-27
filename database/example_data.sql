BEGIN;
INSERT INTO Panstwa (nazwa, kod_iso, kontynent, stolica) VALUES
('Polska', 'POL', 'Europa', 'Warszawa'),
('Stany Zjednoczone', 'USA', 'Ameryka Północna', 'Waszyngton'),
('Francja', 'FRA', 'Europa', 'Paryż'),
('Szwecja', 'SWE', 'Europa', 'Sztokholm'),
('Włochy', 'ITA', 'Europa', 'Rzym'),
('Indie', 'IND', 'Azja', 'New Delhi'),
('Wenezuela', 'VEN', 'Ameryka Południowa', 'Caracas'),
('Katar', 'QAT', 'Azja', 'Doha'),
('Ukraina', 'UKR', 'Europa', 'Kijów'),
('Kanada', 'CAN', 'Ameryka Północna', 'Ottawa'),
('Grecja', 'GRE', 'Europa', 'Ateny'),
('Niemcy', 'GER', 'Europa', 'Berlin'),
('Grenada', 'GRN', 'Ameryka Północna', NULL), 
('Refugee Olympic Team', 'EOR', NULL, NULL);

INSERT INTO Reprezentanci_zawodnikow (imie, nazwisko, adres_email) VALUES
('Jan', 'Kowalski', 'jan.kowalski@agency.com'),
('Mino', 'Raiola', 'mino.r@superagent.it'),
('Czesław', 'Manager', 'czeslaw@sport.pl'),
('John', 'Smith', 'john.smith@usa.tf');

INSERT INTO Trenerzy (imie, nazwisko, adres_email) VALUES
('Greg', 'Duplantis', 'greg@polevault.com'),
('Czesław', 'Cybulski', 'czeslaw@legend.pl'),
('Witold', 'Suski', 'witold.suski@pzla.pl'),
('Gerd', 'Kanter', 'gerd@throw.ee'),
('Malwina', 'Wojtulewicz', 'malwina@javelin.pl'),
('Aleksander', 'Wojtkowski', 'alek@shotput.pl');

INSERT INTO Stadiony (nazwa, miasto, id_panstwa) VALUES
('Stadion Śląski', 'Chorzów', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL')),
('Stadion Narodowy', 'Warszawa', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL')),
('Stade de France', 'Paryż', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'FRA')),
('Hayward Field', 'Eugene', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'USA')),
('Stadion Olimpijski w Tokio', 'Tokio', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'USA')),
('Stadion Narodowy w Budapeszcie', 'Budapeszt', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL')),
('Letzigrund', 'Zurych', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'SWE'));

INSERT INTO Konkurencje (nazwa, rodzaj) VALUES
('Skok o tyczce', 'Skok'),
('Skok wzwyż', 'Skok'),
('Trójskok', 'Skok'),
('Skok w dal', 'Skok'),
('Pchnięcie kulą', 'Pchnięcie'),
('Rzut młotem', 'Rzut'),
('Rzut oszczepem', 'Rzut'),
('Rzut dyskiem', 'Rzut');

INSERT INTO Typy_zawodow (nazwa_typu) VALUES
('Igrzyska Olimpijskie'),
('Mistrzostwa Świata'),
('Diamentowa Liga'),
('Mityng Krajowy');

INSERT INTO Statusy_wynikow (status_wyniku) VALUES
('Ukończono'),
('DNS'),
('NM'),
('DQ');

INSERT INTO Zawodnicy (imie, nazwisko, data_urodzenia, plec, id_panstwa, id_reprezentanta) VALUES
('Armand', 'Duplantis', '1999-11-10', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'SWE'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Raiola')),
('Piotr', 'Lisek', '1992-08-16', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Kowalski')),
('Sam', 'Kendricks', '1992-09-07', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'USA'), NULL),
('Anita', 'Włodarczyk', '1985-08-08', 'K', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), NULL),
('Wojciech', 'Nowicki', '1989-02-22', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Manager')),
('Paweł', 'Fajdek', '1989-06-04', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Manager')),
('Ethan', 'Katzberg', '2002-04-05', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'CAN'), NULL),
('Ryan', 'Crouser', '1992-12-18', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'USA'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Smith')),
('Joe', 'Kovacs', '1989-06-28', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'USA'), NULL),
('Konrad', 'Bukowiecki', '1997-03-17', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Kowalski')),
('Michał', 'Haratyk', '1992-04-10', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), NULL),
('Yaroslava', 'Mahuchikh', '2001-09-19', 'K', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'UKR'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Raiola')),
('Gianmarco', 'Tamberi', '1992-06-01', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'ITA'), NULL),
('Mutaz Essa', 'Barshim', '1991-06-24', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'QAT'), NULL),
('Neeraj', 'Chopra', '1997-12-24', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'IND'), NULL),
('Maria', 'Andrejczyk', '1996-03-09', 'K', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Kowalski')),
('Johannes', 'Vetter', '1993-03-26', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'GER'), NULL),
('Yulimar', 'Rojas', '1995-10-21', 'K', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'VEN'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Raiola')),
('Miltiadis', 'Tentoglou', '1998-03-18', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'GRE'), NULL),
('Ivana', 'Vuleta', '1990-05-10', 'K', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'GER'), NULL),
('Kristjan', 'Ceh', '1999-02-17', 'M', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'GER'), NULL),
('Valarie', 'Allman', '1995-02-23', 'K', (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'USA'), (SELECT id_reprezentanta FROM Reprezentanci_zawodnikow WHERE nazwisko = 'Smith'));

INSERT INTO Trenerzy_zawodnicy (id_trenera, id_zawodnika) VALUES
((SELECT id_trenera FROM Trenerzy WHERE nazwisko = 'Duplantis'), (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Duplantis')),
((SELECT id_trenera FROM Trenerzy WHERE nazwisko = 'Cybulski'), (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Włodarczyk')),
((SELECT id_trenera FROM Trenerzy WHERE nazwisko = 'Cybulski'), (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Fajdek')),
((SELECT id_trenera FROM Trenerzy WHERE nazwisko = 'Wojtulewicz'), (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Andrejczyk')),
((SELECT id_trenera FROM Trenerzy WHERE nazwisko = 'Wojtkowski'), (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Bukowiecki')),
((SELECT id_trenera FROM Trenerzy WHERE nazwisko = 'Suski'), (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Lisek'));

INSERT INTO Zawody (nazwa, id_typu_zawodow, data_rozpoczecia, data_zakonczenia, id_panstwa, id_stadionu) VALUES
('Igrzyska Olimpijskie Paryż 2024', 
    (SELECT id_typu_zawodow FROM Typy_zawodow WHERE nazwa_typu = 'Igrzyska Olimpijskie'), 
    '2024-08-01', '2024-08-11', 
    (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), 
    (SELECT id_stadionu FROM Stadiony WHERE nazwa = 'Stade de France')),
    
('Mistrzostwa Świata Oregon 2022', 
    (SELECT id_typu_zawodow FROM Typy_zawodow WHERE nazwa_typu = 'Mistrzostwa Świata'), 
    '2022-07-15', '2022-07-24', 
    (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'USA'), 
    (SELECT id_stadionu FROM Stadiony WHERE nazwa = 'Hayward Field')),
    
('Diamentowa Liga Chorzów 2023', 
    (SELECT id_typu_zawodow FROM Typy_zawodow WHERE nazwa_typu = 'Diamentowa Liga'), 
    '2023-07-16', '2023-07-16', 
    (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), 
    (SELECT id_stadionu FROM Stadiony WHERE nazwa = 'Stadion Śląski')),
    
('Mityng w Zurychu 2023', 
    (SELECT id_typu_zawodow FROM Typy_zawodow WHERE nazwa_typu = 'Diamentowa Liga'), 
    '2023-08-31', '2023-08-31', 
    (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'SWE'), 
    (SELECT id_stadionu FROM Stadiony WHERE nazwa = 'Letzigrund')),
    
('Memoriał Kamili Skolimowskiej 2021', 
    (SELECT id_typu_zawodow FROM Typy_zawodow WHERE nazwa_typu = 'Mityng Krajowy'), 
    '2021-09-05', '2021-09-05', 
    (SELECT id_panstwa FROM Panstwa WHERE kod_iso = 'POL'), 
    (SELECT id_stadionu FROM Stadiony WHERE nazwa = 'Stadion Śląski'));


INSERT INTO Wyniki (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu) VALUES
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Duplantis'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 6.25, 1, '2024-08-05'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Kendricks'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 5.95, 2, '2024-08-05'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Lisek'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 5.75, 6, '2024-08-05'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Katzberg'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 84.12, 1, '2024-08-04'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Nowicki'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 77.42, 7, '2024-08-04'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Fajdek'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 78.80, 5, '2024-08-04'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Mahuchikh'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok wzwyż'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 2.00, 1, '2024-08-04'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Tentoglou'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok w dal'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 8.48, 1, '2024-08-06');

INSERT INTO Wyniki (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu) VALUES
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Crouser'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 22.94, 1, '2022-07-17'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Kovacs'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 22.89, 2, '2022-07-17'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Bukowiecki'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 20.20, 13, '2022-07-17'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Chopra'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut oszczepem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 88.13, 2, '2022-07-23'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Vetter'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut oszczepem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 3, NULL, NULL, '2022-07-23'), -- NM
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Andrejczyk'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut oszczepem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 55.47, 21, '2022-07-20'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Rojas'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Trójskok'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 15.47, 1, '2022-07-18'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Fajdek'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 81.98, 1, '2022-07-16'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Nowicki'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 81.03, 2, '2022-07-16');

INSERT INTO Wyniki (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu) VALUES
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Barshim'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok wzwyż'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Diamentowa Liga Chorzów 2023'), 1, 2.36, 1, '2023-07-16'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Tamberi'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok wzwyż'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Diamentowa Liga Chorzów 2023'), 1, 2.34, 2, '2023-07-16'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Mahuchikh'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok wzwyż'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Diamentowa Liga Chorzów 2023'), 1, 2.01, 1, '2023-07-16'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Crouser'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Diamentowa Liga Chorzów 2023'), 1, 22.55, 1, '2023-07-16'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Haratyk'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Diamentowa Liga Chorzów 2023'), 1, 20.90, 5, '2023-07-16'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Lisek'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Diamentowa Liga Chorzów 2023'), 1, 5.82, 3, '2023-07-16');

INSERT INTO Wyniki (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu) VALUES
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Duplantis'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mityng w Zurychu 2023'), 1, 6.00, 1, '2023-08-31'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Rojas'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Trójskok'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mityng w Zurychu 2023'), 1, 15.15, 1, '2023-08-31');


INSERT INTO Wyniki (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu) VALUES
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Włodarczyk'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Memoriał Kamili Skolimowskiej 2021'), 1, 74.00, 1, '2021-09-05'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Fajdek'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Diamentowa Liga Chorzów 2023'), 3, NULL, NULL, '2023-07-16'), -- NM

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Bukowiecki'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mityng w Zurychu 2023'), 2, NULL, NULL, '2023-08-31'), -- DNS

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Allman'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut dyskiem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 69.50, 1, '2024-08-05'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Ceh'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut dyskiem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 71.13, 1, '2022-07-19'),

((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Włodarczyk'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 74.23, 4, '2024-08-06'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Crouser'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 22.90, 1, '2024-08-03'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Kovacs'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Igrzyska Olimpijskie Paryż 2024'), 1, 22.15, 2, '2024-08-03'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Haratyk'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Memoriał Kamili Skolimowskiej 2021'), 1, 20.50, 2, '2021-09-05'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Lisek'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Memoriał Kamili Skolimowskiej 2021'), 1, 5.80, 2, '2021-09-05'),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Vuleta'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok w dal'), (SELECT id_zawody FROM Zawody WHERE nazwa = 'Mistrzostwa Świata Oregon 2022'), 1, 7.02, 7, '2022-07-24');


INSERT INTO Rekordy_zyciowe (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy) VALUES
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Duplantis'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), 6.26, '2024-08-25', 1350),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Włodarczyk'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), 82.98, '2016-08-28', 1300),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Crouser'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), 23.56, '2023-05-27', 1320),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Lisek'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), 6.02, '2019-07-12', 1250),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Andrejczyk'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut oszczepem'), 71.40, '2021-05-09', 1280),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Rojas'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Trójskok'), 15.74, '2022-03-20', 1330),
((SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Mahuchikh'), (SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok wzwyż'), 2.10, '2024-07-07', 1310);


INSERT INTO Rekordy_swiata (id_konkurencji, rezultat, data_rezultatu, id_zawodnika) VALUES
((SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok o tyczce'), 6.26, '2024-08-25', (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Duplantis')),
((SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Rzut młotem'), 82.98, '2016-08-28', (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Włodarczyk')),
((SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Pchnięcie kulą'), 23.56, '2023-05-27', (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Crouser')),
((SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Trójskok'), 15.74, '2022-03-20', (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Rojas')),
((SELECT id_konkurencji FROM Konkurencje WHERE nazwa = 'Skok wzwyż'), 2.10, '2024-07-07', (SELECT id_zawodnika FROM Zawodnicy WHERE nazwisko = 'Mahuchikh'));

COMMIT;