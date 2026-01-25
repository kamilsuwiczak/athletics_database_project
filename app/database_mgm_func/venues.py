import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection


def get_venues():
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id_stadionu, nazwa, miasto, id_panstwa FROM Stadiony ORDER BY nazwa")
        return cur.fetchall()

def add_venue(nazwa, miasto, kod_iso):
    with get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
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

def update_venue(id_stadionu, nazwa, miasto, id_panstwa):
    with get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    UPDATE Stadiony 
                    SET nazwa = %s, miasto = %s, id_panstwa = (SELECT id_panstwa FROM Panstwa WHERE id_panstwa = %s)
                    WHERE id_stadionu = %s
                """, (nazwa, miasto, id_panstwa, id_stadionu))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
