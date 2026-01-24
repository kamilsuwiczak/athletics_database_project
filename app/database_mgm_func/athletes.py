import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

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

def update_athlete(id_zawodnika, imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta=None):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE Zawodnicy 
                    SET imie = %s, nazwisko = %s, data_urodzenia = %s, plec = %s, id_panstwa = %s, id_reprezentanta = %s
                    WHERE id_zawodnika = %s
                """, (imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta, id_zawodnika))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
    
def delete_athletes(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Zawodnicy WHERE id_zawodnika = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
