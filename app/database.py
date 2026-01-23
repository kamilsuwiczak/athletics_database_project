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
                cur.execute("CALL dodaj_trenera(%s, %s, %s)", 
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






