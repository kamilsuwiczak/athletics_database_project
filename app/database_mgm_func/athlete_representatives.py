import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_athlete_representatives(filter_by = None, search_term = None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name_surname':
                query = """
                SELECT ar.id_reprezentanta, ar.imie, ar.nazwisko
                FROM Reprezentanci_Zawodnikow ar
                WHERE ar.nazwisko ILIKE %s
                ORDER BY ar.nazwisko;
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("""
                SELECT ar.id_reprezentanta, ar.imie, ar.nazwisko
                FROM Reprezentanci_Zawodnikow ar
                ORDER BY ar.nazwisko;
                """)
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