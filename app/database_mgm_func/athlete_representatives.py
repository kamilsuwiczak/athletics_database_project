import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_athlete_representatives(filter_by=None, search_term=None):
    """
    Pobiera listę przedstawicieli.
    Zwraca słowniki z kluczami: id_przedstawiciela, Imię, Nazwisko
    """
    conn = get_connection()
    
    # Aliasujemy kolumny tak, aby pasowały do Twojego kodu w views/athletes.py
    # (id_reprezentanta -> id_przedstawiciela)
    base_query = """
        SELECT id_reprezentanta AS id_przedstawiciela,
               imie AS "Imię",
               nazwisko AS "Nazwisko",
               adres_email AS "Email"
        FROM Reprezentanci_zawodnikow
    """
    
    conditions = []
    params = []

    # Opcjonalne filtrowanie (dla spójności z resztą systemu)
    if filter_by and search_term:
        if filter_by == 'id':
            conditions.append("id_reprezentanta = %s")
            params.append(search_term)
        elif filter_by == 'nazwisko':
            conditions.append("nazwisko ILIKE %s")
            params.append(f"%{search_term}%")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    full_query = base_query + where_clause + " ORDER BY nazwisko ASC"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(full_query, params)
        return cur.fetchall()

def add_athlete_representative(name, surname):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Reprezentanci_Zawodnikow (imie, nazwisko) 
                VALUES (%s, %s)
                """, (name, surname))
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
        

def update_athlete_representative(id_reprezentanta, name, surname):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Reprezentanci_Zawodnikow 
                SET imie = %s, nazwisko = %s
                WHERE id_reprezentanta = %s
                """, (name, surname, id_reprezentanta))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)