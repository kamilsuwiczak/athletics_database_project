DROP TABLE IF EXISTS Zawodnicy CASCADE; 
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
DROP TABLE IF EXISTS Typy_zawodow CASCADE;

CREATE TABLE Reprezentanci_zawodnikow(
    id_reprezentanta SERIAL PRIMARY KEY,
    imie VARCHAR(100) NOT NULL,
    nazwisko VARCHAR(100) NOT NULL,
    adres_email VARCHAR(100) NOT NULL,
    UNIQUE (adres_email)
    );

CREATE TABLE Konkurencje(
    id_konkurencji SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    rodzaj VARCHAR(50) NOT NULL,
    UNIQUE (nazwa)
    );

CREATE TABLE Panstwa(
    id_panstwa SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    kod_iso CHAR(3) NOT NULL,
    kontynent VARCHAR(50) NULL,
    stolica VARCHAR(100) NULL,
    UNIQUE (kod_iso)
    );

CREATE TABLE Trenerzy(
    id_trenera SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    adres_email VARCHAR(100) NOT NULL,
    UNIQUE (adres_email)
    );

CREATE TABLE Zawodnicy(
    id_zawodnika SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    data_urodzenia DATE NOT NULL,
    plec VARCHAR(1) NOT NULL,
    id_panstwa INT REFERENCES Panstwa(id_panstwa) NOT NULL,
    id_reprezentanta INT REFERENCES Reprezentanci_zawodnikow(id_reprezentanta) NULL,
    CONSTRAINT data_urodzenia_check CHECK (data_urodzenia <= CURRENT_DATE),
    CONSTRAINT plec_check CHECK (plec IN ('K', 'M')),
    UNIQUE (imie, nazwisko, data_urodzenia, plec)
    );

CREATE TABLE Rekordy_zyciowe(
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    id_konkurencji INT REFERENCES Konkurencje(id_konkurencji) NOT NULL,
    rezultat NUMERIC(10,2) NOT NULL,
    data_rezultatu DATE NOT NULL,
    wynik_punktowy INT NOT NULL,
    CONSTRAINT wynik_punktowy_check CHECK (wynik_punktowy >= 0),
    CONSTRAINT rezultat_check CHECK (rezultat >= 0),
    CONSTRAINT data_rezultatu_check CHECK (data_rezultatu <= CURRENT_DATE),
    PRIMARY KEY (id_zawodnika, id_konkurencji)
    );

CREATE TABLE Trenerzy_zawodnicy(
    id_trenera INT REFERENCES Trenerzy(id_trenera) NOT NULL,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    PRIMARY KEY (id_trenera, id_zawodnika)
    );

CREATE TABLE Rekordy_swiata(
    id_konkurencji INT REFERENCES Konkurencje(id_konkurencji) NOT NULL,
    rezultat NUMERIC(10,2) NOT NULL,
    data_rezultatu DATE NOT NULL,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    CONSTRAINT rezultat_rekord_swiata_check CHECK (rezultat >= 0),
    PRIMARY KEY (id_konkurencji, id_zawodnika)
    );

CREATE TABLE Stadiony(
    id_stadionu SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    miasto VARCHAR(100) NOT NULL,
    id_panstwa INT REFERENCES Panstwa(id_panstwa) NOT NULL,
    UNIQUE (nazwa)
);
CREATE TABLE Typy_zawodow(
    id_typu_zawodow SERIAL PRIMARY KEY,
    nazwa_typu VARCHAR(100) NOT NULL,
    UNIQUE (nazwa_typu)
);

CREATE TABLE Zawody(
    id_zawody SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    id_typu_zawodow  INT REFERENCES Typy_zawodow(id_typu_zawodow) NOT NULL,
    data_rozpoczecia DATE NOT NULL,
    data_zakonczenia DATE NOT NULL,
    id_panstwa INT REFERENCES Panstwa(id_panstwa) NOT NULL,
    id_stadionu INT REFERENCES Stadiony(id_stadionu) NOT NULL,
    CONSTRAINT data_rozpoczecia_check CHECK (data_rozpoczecia <= CURRENT_DATE),
    CONSTRAINT data_zakonczenia_check CHECK (data_zakonczenia >= data_rozpoczecia),
    UNIQUE (nazwa, data_rozpoczecia)
    );

CREATE TABLE Statusy_wynikow(
    id_statusu SERIAL PRIMARY KEY,
    status_wyniku VARCHAR(50) NOT NULL
);

CREATE TABLE Wyniki(
    id_wyniku SERIAL PRIMARY KEY,
    id_zawodnika INT REFERENCES Zawodnicy(id_zawodnika) NOT NULL,
    id_konkurencji INT REFERENCES Konkurencje(id_konkurencji) NOT NULL,
    id_zawody INT REFERENCES Zawody(id_zawody) NOT NULL,
    id_statusu INT REFERENCES Statusy_wynikow(id_statusu) NOT NULL,
    rezultat NUMERIC(10,2) NULL,
    miejsce INT NULL,
    data_rezultatu DATE NOT NULL,
    CONSTRAINT miejsce_check CHECK (miejsce > 0),
    CONSTRAINT rezultat_check_wyniki CHECK (rezultat >= 0),
    CONSTRAINT data_rezultatu_check_wyniki CHECK (data_rezultatu <= CURRENT_DATE),
    UNIQUE (id_zawodnika, id_konkurencji, id_zawody, id_statusu)
);


CREATE OR REPLACE PROCEDURE dodaj_zawodnika(
    p_imie VARCHAR,
    p_nazwisko VARCHAR,
    p_data_urodzenia DATE,
    p_plec CHAR,
    p_kod_iso_panstwa CHAR,
    p_id_reprezentanta INT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_panstwa INT;
    v_nowy_id_zawodnika INT;
BEGIN
    
    SELECT id_panstwa INTO v_id_panstwa
    FROM Panstwa
    WHERE kod_iso = UPPER(p_kod_iso_panstwa); 
    
    
    IF v_id_panstwa IS NULL THEN
        RAISE EXCEPTION 'Błąd: Kraj o kodzie ISO "%" nie istnieje w bazie danych.', p_kod_iso_panstwa;
    END IF;

    
    IF p_plec NOT IN ('K', 'M') THEN
        RAISE EXCEPTION 'Błąd: Płeć musi być "K" lub "M".';
    END IF;

    
    INSERT INTO Zawodnicy (
        imie, 
        nazwisko, 
        data_urodzenia, 
        plec, 
        id_panstwa, 
        id_reprezentanta
    ) VALUES (
        p_imie,
        p_nazwisko,
        p_data_urodzenia,
        p_plec,
        v_id_panstwa,
        p_id_reprezentanta
    ) RETURNING id_zawodnika INTO v_nowy_id_zawodnika;

    RAISE NOTICE 'Pomyślnie dodano nowego zawodnika: % % (ID: %).', 
                 p_imie, p_nazwisko, v_nowy_id_zawodnika;

END;
$$;

CREATE OR REPLACE FUNCTION zlicz_medale_w_typie_zawodow(
    p_id_zawodnika INT,
    p_nazwa_typu_zawodow VARCHAR
)
RETURNS INT AS $$
DECLARE
    v_liczba_medali INT;
BEGIN
    SELECT COUNT(*) INTO v_liczba_medali
    FROM Wyniki w
    JOIN Zawody z ON w.id_zawody = z.id_zawody
    JOIN Typy_zawodow tz ON z.id_typu_zawodow = tz.id_typu_zawodow
    WHERE w.id_zawodnika = p_id_zawodnika
      AND w.miejsce IN (1, 2, 3)
      AND tz.nazwa_typu = p_nazwa_typu_zawodow;
      
    RETURN v_liczba_medali;
END;
$$ LANGUAGE plpgsql;