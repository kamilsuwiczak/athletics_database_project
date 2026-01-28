import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection


def get_athlete_representatives(filter_by=None, search_term=None, **advanced_filters):
    conn = get_connection()

    base_query = """
        SELECT id_reprezentanta, 
               imie AS "Imię", 
               nazwisko AS "Nazwisko", 
               adres_email AS "Email"
        FROM Reprezentanci_Zawodnikow
    """
    
    conditions = []
    params = []

    if filter_by and search_term:
        mapping = {
            'imie': "imie ILIKE %s",
            'nazwisko': "nazwisko ILIKE %s",
            'email': "adres_email ILIKE %s",
            'id': "id_reprezentanta = %s"
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
    



def add_athlete_representative(name, surname, email):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Reprezentanci_Zawodnikow (imie, nazwisko, adres_email) 
                VALUES (%s, %s, %s)
                """, (name, surname, email))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_athlete_representatives(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Reprezentanci_Zawodnikow WHERE id_reprezentanta = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            return False, "Nie można usunąć reprezentanta, ponieważ jest przypisany do jednego lub więcej zawodników."
        except Exception:
            conn.rollback()
            return False, 'Bład podczas usuwania reprezentantów'
        

def update_athlete_representative(id_reprezentanta, name, surname,email):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Reprezentanci_Zawodnikow 
                SET imie = %s, nazwisko = %s, adres_email = %s
                WHERE id_reprezentanta = %s
                """, (name, surname, email, id_reprezentanta))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)