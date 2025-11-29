DROP TABLE IF EXISTS Zawodnicy CASCADE; 
DROP TABLE IF EXISTS Plcie CASCADE;
DROP TABLE IF EXISTS Konkurencje CASCADE;
DROP TABLE IF EXISTS Reprezentanci_zawodnikow CASCADE;
DROP TABLE IF EXISTS Panstwa CASCADE;
DROP TABLE IF EXISTS Trenerzy CASCADE;
DROP TABLE IF EXISTS Trenerzy_zawodnicy CASCADE;
DROP TABLE IF EXISTS Rekordy_swiata CASCADE;
DROP TABLE IF EXISTS Rekordy_zyciowe CASCADE;
DROP TABLE IF EXISTS Stadiony CASCADE;
DROP TABLE IF EXISTS Zawody CASCADE;
DROP TABLE IF EXISTS Wyniki CASCADE;

CREATE TABLE Plcie(
    id_plci SERIAL PRIMARY KEY,
    plec VARCHAR(10) NOT NULL,
    plec_skrot CHAR(1) NOT NULL
    );

CREATE TABLE Reprezentanci_zawodnikow(
    id_reprezentanta SERIAL PRIMARY KEY,
    imie VARCHAR(100) NOT NULL,
    nazwisko VARCHAR(100) NOT NULL,
    adres_email VARCHAR(100) NOT NULL
    );

CREATE TABLE Konkurencje(
    id_konkurencji SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL
    );

CREATE TABLE Panstwa(
    id_panstwa SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    kod_iso CHAR(3) NOT NULL,
    kontynent VARCHAR(50) NULL,
    stolica VARCHAR(100) NULL
    );

CREATE TABLE Trenerzy(
    id_trenera SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    adres_email VARCHAR(100) NOT NULL
    );

CREATE TABLE Zawodnicy(
    id_zawodnika SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    data_urodzenia DATE,
    id_plci INT REFERENCES Plcie(id_plci) NOT NULL,
    id_panstwa INT REFERENCES Panstwa(id_panstwa) NOT NULL,
    id_reprezentanta INT REFERENCES Reprezentanci_zawodnikow(id_reprezentanta) NULL
    );

CREATE TABLE Rekordy_zyciowe(
    id_rekordu_zyciowego SERIAL PRIMARY KEY,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    id_konkurencji INT REFERENCES Konkurencje(id_konkurencji) NOT NULL,
    rezultat VARCHAR(20) NOT NULL,
    data_ustanowienia DATE NOT NULL,
    wynik_punktowy NUMERIC(10,2) NOT NULL
    );

CREATE TABLE Trenerzy_zawodnicy(
    id_trenera_zawodnicy SERIAL PRIMARY KEY,
    id_trenera INT REFERENCES Trenerzy(id_trenera) NOT NULL,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL
    );

CREATE TABLE Rekordy_swiata(
    id_rekordu SERIAL PRIMARY KEY,
    id_konkurencji INT REFERENCES Konkurencje(id_konkurencji) NOT NULL,
    rezultat VARCHAR(20) NOT NULL,
    data_ustanowienia DATE NOT NULL,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NULL
    );

CREATE TABLE Stadiony(
    id_stadiony SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    id_panstwa INT REFERENCES Panstwa(id_panstwa) NOT NULL
);

CREATE TABLE Zawody(
    id_zawody SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    data_rozpoczecia DATE NOT NULL,
    data_zakonczenia DATE NOT NULL,
    id_panstwa INT REFERENCES Panstwa(id_panstwa) NOT NULL,
    id_stadiony INT REFERENCES Stadiony(id_stadiony) NULL
    );

CREATE TABLE Wyniki(
    id_wyniku SERIAL PRIMARY KEY,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    id_konkurencji INT REFERENCES Konkurencje(id_konkurencji) NOT NULL,
    id_zawody INT REFERENCES Zawody(id_zawody) NOT NULL,
    rezultat VARCHAR(20) NOT NULL,
    miejsce INT NOT NULL,
    status_wyniku VARCHAR(50) NOT NULL,
    data_rezultatu DATE NOT NULL
);