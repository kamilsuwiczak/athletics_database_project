import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="db", 
        database="athletics_db",
        user="myuser",
        password="mypassword"
    )

def get_athletes():
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                   z.data_urodzenia AS "Data urodzenia", 
                   z.plec AS "Płeć", p.nazwa AS "Kraj"
            FROM Zawodnicy z 
            JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
            ORDER BY z.id_zawodnika DESC
        """)
        return cur.fetchall()

def get_athletes_filtered(search_term):
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
            SELECT z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                   z.data_urodzenia AS "Data urodzenia", 
                   z.plec AS "Płeć", p.nazwa AS "Kraj"
            FROM Zawodnicy z 
            JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
            WHERE z.nazwisko ILIKE %s OR z.imie ILIKE %s
            ORDER BY z.nazwisko ASC
        """
        param = f"%{search_term}%"
        cur.execute(query, (param, param))
        return cur.fetchall()

def get_countries():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT nazwa, kod_iso FROM Panstwa ORDER BY nazwa ASC")
        return cur.fetchall()

def add_athlete(imie, nazwisko, data_ur, plec, kod_iso):
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