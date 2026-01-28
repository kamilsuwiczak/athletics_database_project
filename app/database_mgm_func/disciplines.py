import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error

def get_disciplines(filter_by=None, search_term=None):
    conn = get_connection()
    
    base_query = """
        SELECT id_konkurencji, 
               nazwa, 
               rodzaj
        FROM Konkurencje
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if not filter_by or not search_term:
            cur.execute(base_query + " ORDER BY nazwa ASC")
        else:
   
            filters = {
                'nazwa': ("nazwa ILIKE %s", f"%{search_term}%"),
                'rodzaj': ("rodzaj ILIKE %s", f"%{search_term}%"),
                'id': ("id_konkurencji = %s", search_term) 
            }
            
            if filter_by in filters:
                where_clause, params = filters[filter_by]
                query = f"{base_query} WHERE {where_clause} ORDER BY nazwa ASC"
                cur.execute(query, (params,))
            else:
                cur.execute(base_query + " ORDER BY nazwa ASC")
        return cur.fetchall()

def add_discipline(nazwa, rodzaj):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Konkurencje (nazwa, rodzaj) VALUES (%s, %s)", (nazwa, rodzaj))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)

def delete_disciplines(ids_to_delete):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Konkurencje WHERE id_konkurencji = ANY(%s)", (ids_to_delete,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)

def update_discipline(id_konkurencji, nazwa, rodzaj):
    conn = get_connection()
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
        error_msg = _short_db_error(e)
        return False, error_msg
