import psycopg2
import streamlit as st
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error


def get_coaches(filter_by=None, search_term=None, **advanced_filters):
    """
    Pobiera listę trenerów z obsługą filtrów podstawowych i zaawansowanych (sidebar).
    """
    conn = get_connection()
    
    base_query = """
        SELECT id_trenera, 
               imie AS "Imię", 
               nazwisko AS "Nazwisko", 
               adres_email AS "Adres email"
        FROM Trenerzy
    """
    
    conditions = []
    params = []

    if filter_by and search_term:
        mapping = {
            'imie': "imie ILIKE %s",
            'nazwisko': "nazwisko ILIKE %s",
            'email': "adres_email ILIKE %s",
            'id': "id_trenera = %s"
        }
        if filter_by in mapping:
            conditions.append(mapping[filter_by])
            params.append(search_term if filter_by == 'id' else f"%{search_term}%")

    if advanced_filters.get('f_imie'):
        conditions.append("imie ILIKE %s")
        params.append(f"%{advanced_filters['f_imie']}%")
        
    if advanced_filters.get('f_nazwisko'):
        conditions.append("nazwisko ILIKE %s")
        params.append(f"%{advanced_filters['f_nazwisko']}%")
        
    if advanced_filters.get('f_email'):
        conditions.append("adres_email ILIKE %s")
        params.append(f"%{advanced_filters['f_email']}%")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    full_query = base_query + where_clause + " ORDER BY nazwisko ASC, imie ASC"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(full_query, params)
            return cur.fetchall()
        except Exception as e:
            print(f"SQL Error: {e}")
            return []
    

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
    except psycopg2.errors.ForeignKeyViolation:
        conn.rollback()
        return False, "Nie można usunąć trenera, ponieważ jest przypisany do jednego lub więcej zawodników."
    except Exception:
        conn.rollback()
        return False, 'Błąd podczas usuwania trenerów'

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
