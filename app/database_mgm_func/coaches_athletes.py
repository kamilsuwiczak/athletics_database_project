import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_coaches_athletes(filter_by = None, search_term = None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'coach_name_surname':
                query = """
                SELECT tz.id_trenera, t.imie AS imie_trenera, t.nazwisko AS nazwisko_trenera,
                       tz.id_zawodnika, z.imie AS imie_zawodnika, z.nazwisko AS nazwisko_zawodnika
                FROM Trenerzy_zawodnicy tz
                JOIN Trenerzy t ON tz.id_trenera = t.id_trenera
                JOIN Zawodnicy z ON tz.id_zawodnika = z.id_zawodnika
                WHERE t.nazwisko ILIKE %s or t.imie ILIKE %s
                ORDER BY t.nazwisko, z.nazwisko;
                """
                param = f"%{search_term}%"
                cur.execute(query, (param, param))
            cur.execute("""
            SELECT tz.id_trenera, t.imie AS imie_trenera, t.nazwisko AS nazwisko_trenera,
                   tz.id_zawodnika, z.imie AS imie_zawodnika, z.nazwisko AS nazwisko_zawodnika
            FROM Trenerzy_zawodnicy tz
            JOIN Trenerzy t ON tz.id_trenera = t.id_trenera
            JOIN Zawodnicy z ON tz.id_zawodnika = z.id_zawodnika
            ORDER BY t.nazwisko, z.nazwisko;
            """)
            return cur.fetchall()

def add_coach_athlete(id_trenera, id_zawodnika):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Trenerzy_zawodnicy (id_trenera, id_zawodnika) 
                VALUES (%s, %s)
                """, (id_trenera, id_zawodnika))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_coaches_athletes(pairs_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                for id_trenera, id_zawodnika in pairs_to_delete:
                    cur.execute("DELETE FROM Trenerzy_zawodnicy WHERE id_trenera = %s AND id_zawodnika = %s", (id_trenera, id_zawodnika))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def update_coach_athlete(old_id_trenera, old_id_zawodnika, new_id_trenera, new_id_zawodnika):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Trenerzy_zawodnicy 
                SET id_trenera = %s, id_zawodnika = %s 
                WHERE id_trenera = %s AND id_zawodnika = %s
                """, (new_id_trenera, new_id_zawodnika, old_id_trenera, old_id_zawodnika))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)