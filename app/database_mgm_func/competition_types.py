import streamlit as st
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error

def get_competition_types(filter_by=None, search_term=None):
    conn = get_connection()
    
    base_query = """
        SELECT id_typu_zawodow, 
               nazwa_typu
        FROM Typy_zawodow
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if not filter_by or not search_term:
            cur.execute(base_query + " ORDER BY nazwa_typu ASC")
        else:
            filters = {
                'nazwa_typu': ("nazwa_typu ILIKE %s", f"%{search_term}%")
            }
            
            if filter_by in filters:
                where_clause, params = filters[filter_by]
                query = f"{base_query} WHERE {where_clause} ORDER BY nazwa_typu ASC"
                cur.execute(query, (params,))
            else:
                cur.execute(base_query + " ORDER BY nazwa_typu ASC")
                
        return cur.fetchall()
    
def add_competition_type(nazwa_typu):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("INSERT INTO Typy_zawodow (nazwa_typu) VALUES (%s)", (nazwa_typu,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)

def delete_competition_types(ids_to_delete):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("DELETE FROM Typy_zawodow WHERE id_typu_zawodow = ANY(%s)", (ids_to_delete,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)

def update_competition_type(id_typu_zawodow, nazwa_typu):
    conn = get_connection()
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
        error_msg = _short_db_error(e)
        return False, error_msg
