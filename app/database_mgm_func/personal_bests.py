import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_personal_bests(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name_surname':
                query = """
                SELECT z.imie as "Imię", z.nazwisko AS "Nazwisko", 
                    d.nazwa AS "Konkurencja", pb.rezultat AS "Rezultat", 
                        pb.data_rezultatu AS "Data rezultatu",pb.wynik_punktowy AS "Wynik punktowy"
                FROM Rekordy_zyciowe pb
                JOIN Zawodnicy z ON pb.id_zawodnika = z.id_zawodnika
                JOIN Konkurencje d ON pb.id_konkurencji = d.id_konkurencji
                WHERE z.nazwisko ILIKE %s OR z.imie ILIKE %s
                ORDER BY z.nazwisko ASC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param, param))
            else:
                cur.execute("""
                    SELECT z.imie as "Imię", z.nazwisko AS "Nazwisko", 
                        d.nazwa AS "Konkurencja", pb.rezultat AS "Rezultat", 
                            pb.data_rezultatu AS "Data rezultatu",pb.wynik_punktowy AS "Wynik punktowy"
                    FROM Rekordy_zyciowe pb
                    JOIN Zawodnicy z ON pb.id_zawodnika = z.id_zawodnika
                    JOIN Konkurencje d ON pb.id_konkurencji = d.id_konkurencji
                """)
            return cur.fetchall()

def add_personal_best(id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Rekordy_zyciowe (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy) VALUES (%s, %s, %s, %s, %s)", 
                        (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg

def delete_personal_bests(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Rekordy_zyciowe WHERE id_rekordu = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def update_personal_best(id_rekordu, id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE Rekordy_zyciowe 
                    SET id_zawodnika = %s, id_konkurencji = %s, rezultat = %s, data_rezultatu = %s, wynik_punktowy = %s
                    WHERE id_rekordu = %s
                """, (id_zawodnika, id_konkurencji, rezultat, data_rezultatu, wynik_punktowy, id_rekordu))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
