DROP TABLE IF EXISTS Zawodnicy;
DROP TABLE IF EXISTS Plcie;

CREATE TABLE Plcie(
    id_plci SERIAL PRIMARY KEY,
    plec VARCHAR(10) NOT NULL,
    plec_skrot CHAR(1) NOT NULL
    );

CREATE TABLE Zawodnicy(
    id_zawodnika SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    data_urodzenia DATE,
    id_plci INT REFERENCES Plcie(id_plci) 
    );

