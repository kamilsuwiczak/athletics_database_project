import streamlit as st
import psycopg2
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error


def get_athletes(filter_by=None, search_term=None, **advanced_filters):
    """
    Pobiera zawodników z uwzględnieniem filtrów podstawowych (search_term)
    oraz zaawansowanych (**advanced_filters).
    """
    conn = get_connection()

    base_query = """
        SELECT z.id_zawodnika, 
               z.imie AS "Imię", 
               z.nazwisko AS "Nazwisko", 
               z.data_urodzenia AS "Data urodzenia", 
               z.plec AS "Płeć", 
               p.nazwa AS "Kraj",
               COALESCE(STRING_AGG(t.imie || ' ' || t.nazwisko, ', '), 'Brak') AS "Trenerzy",
               COALESCE(r.imie || ' ' || r.nazwisko, 'Brak') AS "Przedstawiciel"
        FROM Zawodnicy z 
        JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
        LEFT JOIN Trenerzy_zawodnicy zt ON z.id_zawodnika = zt.id_zawodnika
        LEFT JOIN Trenerzy t ON zt.id_trenera = t.id_trenera
        LEFT JOIN Reprezentanci_zawodnikow r ON z.id_reprezentanta = r.id_reprezentanta
    """

    conditions = []
    params = []

    if filter_by and search_term:
        search_mapping = {
            'imie': "z.imie ILIKE %s",
            'nazwisko': "z.nazwisko ILIKE %s",
            'kraj': "p.nazwa ILIKE %s",
            'id': "z.id_zawodnika = %s"
        }
        if filter_by in search_mapping:
            conditions.append(search_mapping[filter_by])
            if filter_by == 'id':
                params.append(search_term)
            else:
                params.append(f"%{search_term}%")

    if advanced_filters.get('f_imie'):
        conditions.append("z.imie ILIKE %s")
        params.append(f"%{advanced_filters['f_imie']}%")

    if advanced_filters.get('f_nazwisko'):
        conditions.append("z.nazwisko ILIKE %s")
        params.append(f"%{advanced_filters['f_nazwisko']}%")

    if advanced_filters.get('f_id_panstwa'):
        conditions.append("z.id_panstwa = %s")
        params.append(advanced_filters['f_id_panstwa'])

    if advanced_filters.get('f_plec'):
        conditions.append("z.plec = %s")
        params.append(advanced_filters['f_plec'])

    if advanced_filters.get('f_rok_ur_min'):
        conditions.append("EXTRACT(YEAR FROM z.data_urodzenia) >= %s")
        params.append(advanced_filters['f_rok_ur_min'])

    if advanced_filters.get('f_rok_ur_max'):
        conditions.append("EXTRACT(YEAR FROM z.data_urodzenia) <= %s")
        params.append(advanced_filters['f_rok_ur_max'])

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    group_by_clause = " GROUP BY z.id_zawodnika, p.nazwa, r.imie, r.nazwisko"
    order_by_clause = " ORDER BY z.nazwisko ASC, z.imie ASC"

    full_query = base_query + where_clause + group_by_clause + order_by_clause

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(full_query, params)
            return cur.fetchall()
        except Exception:
            return []


def add_athlete(imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CALL dodaj_zawodnika(%s, %s, %s, %s, %s, %s, %s)
            """, (imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta, None))

            result = cur.fetchone()
            new_id = result[0]

            conn.commit()
            return True, new_id

    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)


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
        return False, _short_db_error(e)


def delete_athletes(ids_to_delete):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Zawodnicy WHERE id_zawodnika = ANY(%s)", (ids_to_delete,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)


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
        return False, _short_db_error(e)