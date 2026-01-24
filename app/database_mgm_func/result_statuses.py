import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_result_statuses(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if filter_by == 'name':
                query = """
                SELECT id_statusu, status_wyniku
                FROM Statusy_wynikow
                WHERE status_wyniku ILIKE %s
                ORDER BY status_wyniku ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("SELECT id_statusu, status_wyniku FROM Statusy_wynikow ORDER BY status_wyniku ASC")
            return cur.fetchall()

def add_result_status(status_wyniku):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Statusy_wynikow (status_wyniku) VALUES (%s)", (status_wyniku,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_result_statuses(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Statusy_wynikow WHERE id_statusu = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def update_result_status(id_statusu, status_wyniku):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE Statusy_wynikow 
                    SET status_wyniku = %s
                    WHERE id_statusu = %s
                """, (status_wyniku, id_statusu))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
