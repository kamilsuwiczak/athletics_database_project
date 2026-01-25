import streamlit as st
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection


def get_coaches(filter_by=None, search_term=None):
    conn = get_connection()
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
    conn = get_connection()
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
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Trenerzy WHERE id_trenera = ANY(%s)", (ids_to_delete,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def update_coach(id_trenera, imie, nazwisko, adres_email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE Trenerzy 
                SET imie = %s, nazwisko = %s, adres_email = %s
                WHERE id_trenera = %s
            """, (imie, nazwisko, adres_email, id_trenera))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
        return False, error_msg
