import psycopg2
import streamlit as st
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection


def get_coaches(filter_by=None, search_term=None):
    conn = get_connection()
    
    # Bazowe zapytanie - stałe nazwy kolumn dla widoku
    base_query = """
        SELECT id_trenera, 
               imie AS "Imię", 
               nazwisko AS "Nazwisko", 
               adres_email AS "Adres email"
        FROM Trenerzy
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if not filter_by or not search_term:
            # Domyślne sortowanie
            cur.execute(base_query + " ORDER BY id_trenera DESC")
        
        else:
            # Mapowanie filtrów (musi pasować do search_cfg w widoku)
            filters = {
                'imie': ("imie ILIKE %s", f"%{search_term}%"),
                'nazwisko': ("nazwisko ILIKE %s", f"%{search_term}%"),
                'email': ("adres_email ILIKE %s", f"%{search_term}%"),
                # Potrzebne do pobrania jednego trenera w edit_modal:
                'id': ("id_trenera = %s", search_term) 
            }

            if filter_by in filters:
                where_clause, params = filters[filter_by]
                query = f"{base_query} WHERE {where_clause} ORDER BY nazwisko ASC"
                
                cur.execute(query, (params,))
            else:
                cur.execute(base_query + " ORDER BY id_trenera DESC")

        return cur.fetchall()
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
