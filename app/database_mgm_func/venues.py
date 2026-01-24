import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection


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

def update_venue(id_stadionu, nazwa, miasto, id_panstwa):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
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
