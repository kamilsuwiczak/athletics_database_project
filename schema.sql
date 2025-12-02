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
DROP TABLE IF EXISTS Statusy_wynikow CASCADE;

CREATE TABLE Plcie(
    plec VARCHAR(10) PRIMARY KEY NOT NULL,
    plec_skrot CHAR(1) NOT NULL
    );

CREATE TABLE Reprezentanci_zawodnikow(
    id_reprezentanta SERIAL PRIMARY KEY,
    imie VARCHAR(100) NOT NULL,
    nazwisko VARCHAR(100) NOT NULL,
    adres_email VARCHAR(100) NOT NULL
    );


CREATE TABLE Konkurencje(
    nazwa VARCHAR(100) PRIMARY KEY NOT NULL,
    rodzaj VARCHAR(50) NOT NULL
    );

CREATE TABLE Panstwa(
    kod_iso CHAR(3) PRIMARY KEY NOT NULL,
    nazwa VARCHAR(100) NOT NULL,
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
    plec VARCHAR(10) REFERENCES Plcie(plec) NOT NULL,
    id_reprezentanta INT REFERENCES Reprezentanci_zawodnikow(id_reprezentanta) NOT NULL,
    kod_iso_panstwa CHAR(3) REFERENCES Panstwa(kod_iso) NOT NULL,
    CONSTRAINT data_urodzenia_check CHECK (data_urodzenia <= CURRENT_DATE)
    );

CREATE TABLE Rekordy_zyciowe(
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    nazwa_konkurencji VARCHAR(100) REFERENCES Konkurencje(nazwa) NOT NULL,
    rezultat NUMERIC(10,2) NOT NULL,
    data_rezultatu DATE NOT NULL,
    wynik_punktowy INT NOT NULL,
    CONSTRAINT rekordy_zyciowe_pkey PRIMARY KEY (id_zawodnika, nazwa_konkurencji),
    CONSTRAINT wynik_punktowy_check CHECK (wynik_punktowy >= 0),
    CONSTRAINT rezultat_check CHECK (rezultat >= 0),
    CONSTRAINT data_rezultatu_check CHECK (data_rezultatu <= CURRENT_DATE)
    );

CREATE TABLE Trenerzy_zawodnicy(
    id_trenera INT REFERENCES Trenerzy(id_trenera) NOT NULL,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    CONSTRAINT trenerzy_zawodnicy_pkey PRIMARY KEY (id_trenera, id_zawodnika)
    );

CREATE TABLE Rekordy_swiata(
    nazwa_konkurencji VARCHAR(100) REFERENCES Konkurencje(nazwa) NOT NULL,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    rezultat NUMERIC(10,2) NOT NULL,
    data_rezultatu DATE NOT NULL,
    CONSTRAINT rekordy_swiata_pkey PRIMARY KEY (nazwa_konkurencji, id_zawodnika),
    CONSTRAINT rezultat_rekord_swiata_check CHECK (rezultat >= 0)
    );

CREATE TABLE Stadiony(
    id_stadionu SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    miasto VARCHAR(100) NOT NULL,
    nazwa_panstwa CHAR(3) REFERENCES Panstwa(kod_iso) NOT NULL
    );

CREATE TABLE Zawody(
    nazwa VARCHAR(100) NOT NULL,
    data_rozpoczecia DATE NOT NULL,
    data_zakonczenia DATE NOT NULL,
    id_panstwa CHAR(3) REFERENCES Panstwa(kod_iso) NOT NULL,
    id_stadionu INT REFERENCES Stadiony(id_stadionu) NOT NULL,
    CONSTRAINT zawody_pkey PRIMARY KEY (nazwa, data_rozpoczecia),
    CONSTRAINT data_rozpoczecia_check CHECK (data_rozpoczecia <= CURRENT_DATE),
    CONSTRAINT data_zakonczenia_check CHECK (data_zakonczenia >= data_rozpoczecia)
    );

CREATE TABLE Statusy_wynikow(
    status_wyniku VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE Wyniki(
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    nazwa_konkurencji VARCHAR(100) REFERENCES Konkurencje(nazwa) NOT NULL,
    nazwa_zawody VARCHAR(100) NOT NULL,
    data_rozpoczecia_zawody DATE NOT NULL,
    status_wyniku VARCHAR(50) REFERENCES Statusy_wynikow(status_wyniku) NOT NULL,
    rezultat NUMERIC(10,2) NULL,
    miejsce INT NULL,
    data_rezultatu DATE NOT NULL,

    CONSTRAINT wyniki_pkey 
        PRIMARY KEY (id_zawodnika, nazwa_konkurencji, nazwa_zawody, data_rozpoczecia_zawody),

    CONSTRAINT fk_wyniki_zawody
        FOREIGN KEY (nazwa_zawody, data_rozpoczecia_zawody)
        REFERENCES Zawody(nazwa, data_rozpoczecia),

    CONSTRAINT miejsce_check CHECK (miejsce > 0),
    CONSTRAINT rezultat_check_wyniki CHECK (rezultat >= 0),
    CONSTRAINT data_rezultatu_check_wyniki CHECK (data_rezultatu <= CURRENT_DATE)
);

