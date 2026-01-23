import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

# @st.cache_resource
def get_connection():
    """returns a connection to database"""
    try:
        conn = psycopg2.connect(
            # host="db", 
            database="athletics_db",
            user="myuser",
            password="mypassword"
        )
        return conn
    except Exception as e:
        st.error(f"Błąd połączenia z bazą danych: {e}")
        return None


# Athletes
def get_athletes(filter_by=None, search_term=None):
    """returns id_zawodnika, imie, nazwisko, data_urodzenia, plec, kraj
        options to filter: name_surname - filtering by name or surname
        gender - plec
    """
    with get_connection() as conn: 
        with conn.cursor() as cur:
            if filter_by == None:
                cur.execute("""
                    SELECT z.id_zawodnika, z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                        z.data_urodzenia AS "Data urodzenia", 
                        z.plec AS "Płeć", p.nazwa AS "Kraj"
                    FROM Zawodnicy z 
                    JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
                    ORDER BY z.id_zawodnika DESC
                """)

            elif filter_by == 'name_surname':
                query = """
                SELECT z.id_zawodnika, z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                    z.data_urodzenia AS "Data urodzenia", 
                    z.plec AS "Płeć", p.nazwa AS "Kraj"
                FROM Zawodnicy z 
                JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
                WHERE z.nazwisko ILIKE %s OR z.imie ILIKE %s
                ORDER BY z.nazwisko ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param, param))

            elif filter_by == 'gender':
                query = """
                SELECT z.id_zawodnika, z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                    z.data_urodzenia AS "Data urodzenia", 
                    z.plec AS "Płeć", p.nazwa AS "Kraj"
                FROM Zawodnicy z 
                JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
                WHERE z.plec ILIKE %s
                ORDER BY z.nazwisko ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            
            elif filter_by == 'country':
                query = """
                SELECT z.id_zawodnika, z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                    z.data_urodzenia AS "Data urodzenia", 
                    z.plec AS "Płeć", p.nazwa AS "Kraj"
                FROM Zawodnicy z 
                JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
                WHERE p.nazwa ILIKE %s
                ORDER BY z.nazwisko ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))

            return cur.fetchall()


def add_athlete(imie, nazwisko, data_ur, plec, kod_iso):
    with get_connection() as conn: 
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL dodaj_zawodnika(%s, %s, %s, %s, %s)", 
                        (imie, nazwisko, data_ur, plec, kod_iso))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
    
def delete_athletes(ids_to_delete):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Zawodnicy WHERE id_zawodnika = ANY(%s)", (ids_to_delete,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    

# Countries
def get_countries():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nazwa, kod_iso FROM Panstwa ORDER BY nazwa ASC")
            return cur.fetchall()

def add_country(name, iso_code):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Panstwa (nazwa, kod_iso) VALUES (%s, %s)", (name, iso_code))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_countries(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Panstwa WHERE id_panstwa = ANY(%s)", (ids_to_delete,))
                conn.commit()
        except Exception as e:
            conn.rollback()
            return False, str(e)


#Coaches
def get_coaches(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name_surname':
                query = """
                SELECT id_trenera, imie AS "Imię", nazwisko AS "Nazwisko", adres_email AS "Adres email"
                FROM Trenerzy
                WHERE nazwisko ILIKE %s OR imie ILIKE %s
                ORDER BY nazwisko ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param, param))
            else:
                cur.execute("""
                SELECT id_trenera, imie AS "Imię", nazwisko AS "Nazwisko", adres_email AS "Adres email"
                FROM Trenerzy
                ORDER BY id_trenera DESC
            """)
            return cur.fetchall()

def add_coach(imie, nazwisko, adres_email):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Trenerzy (imie, nazwisko, adres_email) VALUES (%s, %s, %s)", 
                        (imie, nazwisko, adres_email))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg

def delete_coaches(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Trenerzy WHERE id_trenera = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
    

#Personal best 
def get_personal_bests(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name_surname':
                query = """
                SELECT z.imie as "Imię", z.nazwisko AS "Nazwisko", 
                    d.nazwa AS "Konkurencja", pb.rezultat AS "Rezultat", 
                        pb.data_rezultatu AS "Data rezultatu",pb.wynik_punktowy AS "Wynik punktowy"
                FROM Rekordy_zyciowe pb
                JOIN Zawodnicy z ON pb.id_zawodnika = z.id_zawodnika
                JOIN Konkurencje d ON pb.id_konkurencji = d.id_konkurencji
                WHERE z.nazwisko ILIKE %s OR z.imie ILIKE %s
                ORDER BY z.nazwisko ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param, param))
            else:
                cur.execute("""
                    SELECT z.imie as "Imię", z.nazwisko AS "Nazwisko", 
                        d.nazwa AS "Konkurencja", pb.rezultat AS "Rezultat", 
                            pb.data_rezultatu AS "Data rezultatu",pb.wynik_punktowy AS "Wynik punktowy"
                    FROM Rekordy_zyciowe pb
                    JOIN Zawodnicy z ON pb.id_zawodnika = z.id_zawodnika
                    JOIN Konkurencje d ON pb.id_konkurencji = d.id_konkurencji
                """)
            return cur.fetchall()

def add_personal_best(id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Rekordy_zyciowe (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy) VALUES (%s, %s, %s, %s, %s)", 
                        (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg

def delete_personal_bests(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Rekordy_zyciowe WHERE id_rekordu = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

# Competitions
def get_competitions(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name':
                query = """
                SELECT id_konkurencji, nazwa AS "Nazwa", rodzaj AS "Rodzaj"
                FROM Konkurencje
                WHERE nazwa ILIKE %s
                ORDER BY nazwa ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("SELECT id_konkurencji, nazwa, rodzaj FROM Konkurencje ORDER BY nazwa ASC")
            return cur.fetchall()

def add_competition(nazwa, rodzaj):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Konkurencje (nazwa, rodzaj) VALUES (%s, %s)", (nazwa, rodzaj))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_competitions(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Konkurencje WHERE id_konkurencji = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

# Venues
def get_venues(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name':
                query = """
                SELECT s.id_stadionu, s.nazwa as Stadion, s.miasto, p.nazwa as Panstwo,p.kod_iso
                FROM stadiony s 
                JOIN Panstwa p on s.id_panstwa = p.id_panstwa
                WHERE s.nazwa ILIKE %s
                ORDER BY s.nazwa ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            elif filter_by == 'country_iso_code':
                query = """
                SELECT s.id_stadionu, s.nazwa as Stadion, s.miasto, p.nazwa as Panstwo,p.kod_iso
                FROM stadiony s 
                JOIN Panstwa p on s.id_panstwa = p.id_panstwa
                WHERE p.kod_iso ILIKE %s OR p.nazwa ILIKE %s
                ORDER BY s.nazwa ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param, param))
            elif filter_by == 'city':
                query = """
                SELECT s.id_stadionu, s.nazwa as Stadion, s.miasto, p.nazwa as Panstwo,p.kod_iso
                FROM stadiony s 
                JOIN Panstwa p on s.id_panstwa = p.id_panstwa
                WHERE s.miasto ILIKE %s
                ORDER BY s.nazwa ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("SELECT s.id_stadionu, s.nazwa as Stadion, s.miasto, p.nazwa as Panstwo,p.kod_iso FROM stadiony s JOIN Panstwa p on s.id_panstwa = p.id_panstwa ORDER BY s.nazwa ASC")
            return cur.fetchall()

def add_venue(nazwa, miasto, kod_iso):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Stadiony (nazwa, miasto, id_panstwa) VALUES (%s, %s, (SELECT id_panstwa FROM Panstwa WHERE kod_iso = %s))", 
                        (nazwa, miasto, kod_iso))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg

def delete_venues(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Stadiony WHERE id_stadionu = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)


