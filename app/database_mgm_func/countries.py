import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_countries():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT nazwa, kod_iso FROM Panstwa ORDER BY nazwa ASC")
            return cur.fetchall()

def update_coutry(id_panstwa, new_name, new_iso_code):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE Panstwa SET nazwa = %s, kod_iso = %s WHERE id_panstwa = %s", 
                        (new_name, new_iso_code, id_panstwa))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

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