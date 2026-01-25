import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_athletes(filter_by=None, search_term=None):
    conn = get_connection()

    base_query = """
        SELECT z.id_zawodnika, 
               z.imie AS "Imię", 
               z.nazwisko AS "Nazwisko", 
               z.data_urodzenia AS "Data urodzenia", 
               z.plec AS "Płeć", 
               p.nazwa AS "Kraj",
               COALESCE(STRING_AGG(t.imie || ' ' || t.nazwisko, ', '), 'Brak') AS "Trenerzy"
        FROM Zawodnicy z 
        JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
        LEFT JOIN Trenerzy_zawodnicy zt ON z.id_zawodnika = zt.id_zawodnika
        LEFT JOIN Trenerzy t ON zt.id_trenera = t.id_trenera
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        group_by_clause = " GROUP BY z.id_zawodnika, p.nazwa"
        
        if not filter_by or not search_term:
            cur.execute(base_query + group_by_clause + " ORDER BY z.id_zawodnika DESC")
        else:
            filters = {
                'imie': ("z.imie ILIKE %s", f"%{search_term}%"),
                'nazwisko': ("z.nazwisko ILIKE %s", f"%{search_term}%"),
                'kod_iso': ("p.kod_iso ILIKE %s", f"%{search_term}%"),
                'id': ("z.id_zawodnika = %s", search_term),
                'trener': ("t.nazwisko ILIKE %s", f"%{search_term}%"),
                'kraj': ("p.nazwa ILIKE %s", f"%{search_term}%")
            }

            if filter_by in filters:
                where_clause, params = filters[filter_by]
                query = f"{base_query} WHERE {where_clause} {group_by_clause} ORDER BY z.nazwisko ASC"
                cur.execute(query, (params,))
            else:
                cur.execute(base_query + group_by_clause + " ORDER BY z.id_zawodnika DESC")

        return cur.fetchall()

def add_athlete(imie, nazwisko, data_ur, plec, kod_iso):
    conn = get_connection() 
    try:
        with conn.cursor() as cur:
            cur.execute("CALL dodaj_zawodnika(%s, %s, %s, %s, %s)", 
                        (imie, nazwisko, data_ur, plec, kod_iso))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
        return False, error_msg

def update_athlete(id_zawodnika, imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE Zawodnicy 
                SET imie = %s, nazwisko = %s, data_urodzenia = %s, plec = %s, id_panstwa = %s, id_reprezentanta = %s
                WHERE id_zawodnika = %s
            """, (imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta, id_zawodnika))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
        return False, error_msg

def delete_athletes(ids_to_delete):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Zawodnicy WHERE id_zawodnika = ANY(%s)", (ids_to_delete,))
            conn.commit()
            return True, None
    except psycopg2.errors.ForeignKeyViolation:
        conn.rollback()
        return False, 'Nie można usunąć zawodnika, ponieważ jest przypisany do jednego lub więcej wyników.'
    except Exception:
        conn.rollback()
        return False, 'Błąd podczas usuwania zawodników'
    

def get_athlete_coaches_ids(id_zawodnika):
    """Pobiera listę samych ID trenerów przypisanych do zawodnika"""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id_trenera FROM Trenerzy_zawodnicy WHERE id_zawodnika = %s", (id_zawodnika,))
        return [row[0] for row in cur.fetchall()]

def update_athlete_coaches(id_zawodnika, list_of_coach_ids):
    """Synchronizuje tabelę łączącą - usuwa stare i wstawia nowe relacje"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Trenerzy_zawodnicy WHERE id_zawodnika = %s", (id_zawodnika,))
            for id_t in list_of_coach_ids:
                cur.execute(
                    "INSERT INTO Trenerzy_zawodnicy (id_zawodnika, id_trenera) VALUES (%s, %s)",
                    (id_zawodnika, id_t)
                )
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)