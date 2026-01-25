import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_competition_types(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name':
                query = """
                SELECT id_typu_zawodow, nazwa_typu
                FROM Typy_zawodow
                WHERE nazwa_typu ILIKE %s
                ORDER BY nazwa_typu ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("SELECT id_typu_zawodow, nazwa_typu FROM Typy_zawodow ORDER BY nazwa_typu ASC")
            return cur.fetchall()
        
def add_competition_type(nazwa_typu):
    with get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("INSERT INTO Typy_zawodow (nazwa_typu) VALUES (%s)", (nazwa_typu,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_competition_types(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("DELETE FROM Typy_zawodow WHERE id_typu_zawodow = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def update_competition_type(id_typu_zawodow, nazwa_typu):
    with get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    UPDATE Typy_zawodow 
                    SET nazwa_typu = %s
                    WHERE id_typu_zawodow = %s
                """, (nazwa_typu, id_typu_zawodow))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
