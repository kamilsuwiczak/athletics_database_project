import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error


def get_personal_bests(id_zawodnika):
    """Pobiera obecne rekordy życiowe zawodnika"""
    conn = get_connection()
    query = """
        SELECT k.id_konkurencji, 
               k.nazwa AS "Konkurencja",
               rz.rezultat AS "Wynik",
               rz.data_rezultatu AS "Data",
               rz.wynik_punktowy AS "Punkty"
        FROM Rekordy_zyciowe rz
        JOIN Konkurencje k ON rz.id_konkurencji = k.id_konkurencji
        WHERE rz.id_zawodnika = %s
        ORDER BY k.nazwa ASC
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (id_zawodnika,))
        return cur.fetchall()

def get_all_disciplines():
    """Pobiera listę wszystkich dostępnych konkurencji"""
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id_konkurencji, nazwa FROM Konkurencje ORDER BY nazwa ASC")
        return cur.fetchall()

def upsert_personal_best(id_zawodnika, id_konkurencji, rezultat, data, punkty):
    """
    Dodaje nowy rekord lub aktualizuje istniejący (ON CONFLICT).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO Rekordy_zyciowe (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_zawodnika, id_konkurencji) 
                DO UPDATE SET 
                    rezultat = EXCLUDED.rezultat,
                    data_rezultatu = EXCLUDED.data_rezultatu,
                    wynik_punktowy = EXCLUDED.wynik_punktowy
            """
            cur.execute(query, (id_zawodnika, id_konkurencji, rezultat, data, punkty))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)

def delete_personal_best(id_zawodnika, id_konkurencji):
    """Usuwa rekord życiowy w danej konkurencji"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM Rekordy_zyciowe 
                WHERE id_zawodnika = %s AND id_konkurencji = %s
            """, (id_zawodnika, id_konkurencji))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)