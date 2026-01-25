import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_disciplines(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name':
                query = """
                SELECT id_konkurencji, nazwa, rodzaj AS "Rodzaj"
                FROM Konkurencje
                WHERE nazwa ILIKE %s
                ORDER BY nazwa ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("SELECT id_konkurencji, nazwa, rodzaj FROM Konkurencje ORDER BY nazwa ASC")
            return cur.fetchall()

def add_discipline(nazwa, rodzaj):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Konkurencje (nazwa, rodzaj) VALUES (%s, %s)", (nazwa, rodzaj))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_disciplines(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Konkurencje WHERE id_konkurencji = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def update_discipline(id_konkurencji, nazwa, rodzaj):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE Konkurencje 
                    SET nazwa = %s, rodzaj = %s
                    WHERE id_konkurencji = %s
                """, (nazwa, rodzaj, id_konkurencji))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
