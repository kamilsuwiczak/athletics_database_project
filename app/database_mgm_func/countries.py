import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error

def get_countries(filter_by=None, search_term=None, **advanced_filters):
    conn = get_connection()
    
    base_query = """
        SELECT id_panstwa, 
               nazwa, 
               kod_iso, 
               kontynent, 
               stolica 
        FROM Panstwa
    """
    
    conditions = []
    params = []

    if filter_by == "id_panstwa" and search_term:
        conditions.append("id_panstwa = %s")
        params.append(search_term)

    if advanced_filters.get('f_nazwa'):
        conditions.append("nazwa ILIKE %s")
        params.append(f"%{advanced_filters['f_nazwa']}%")
        
    if advanced_filters.get('f_kod'):
        conditions.append("kod_iso ILIKE %s")
        params.append(f"%{advanced_filters['f_kod']}%")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    full_query = base_query + where_clause + " ORDER BY nazwa ASC"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(full_query, params)
            return cur.fetchall()
        except Exception as e:
            print(f"SQL Error: {e}")
            return []

def update_country(id_panstwa, new_name, new_iso_code):
    conn = get_connection()
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
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Panstwa (nazwa, kod_iso) VALUES (%s, %s)", (name, iso_code))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def delete_countries(ids_to_delete):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Panstwa WHERE id_panstwa = ANY(%s)", (ids_to_delete,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)