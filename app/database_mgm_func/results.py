import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_results(filter_by=None, search_term=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'athlete':
                query = """
                SELECT r.id_wyniku, r.rezultat, r.miejsce, r.data_rezultatu, z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                    k.nazwa AS "Konkurencja", w.nazwa AS "Zawody", s.status_wyniku
                FROM Wyniki r
                JOIN Zawodnicy z ON r.id_zawodnika = z.id_zawodnika
                JOIN Konkurencje k ON r.id_konkurencji = k.id_konkurencji
                JOIN Statusy_Wynikow s ON r.id_statusu = s.id_statusu
                JOIN zawody w ON r.id_zawody = w.id_zawody
                WHERE z.imie ILIKE %s OR z.nazwisko ILIKE %s
                ORDER BY r.id_wyniku DESC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param, param))
            elif filter_by == 'competition':
                query = """
                SELECT r.id_wyniku, r.rezultat, r.miejsce, r.data_rezultatu, z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                    k.nazwa AS "Konkurencja", w.nazwa AS "Zawody", s.status_wyniku
                FROM Wyniki r
                JOIN Zawodnicy z ON r.id_zawodnika = z.id_zawodnika
                JOIN Konkurencje k ON r.id_konkurencji = k.id_konkurencji
                JOIN Statusy_Wynikow s ON r.id_statusu = s.id_statusu
                JOIN zawody w ON r.id_zawody = w.id_zawody
                WHERE k.nazwa ILIKE %s
                ORDER BY r.id_wyniku DESC
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("""
                    SELECT r.id_wyniku, r.rezultat, r.miejsce, r.data_rezultatu, z.imie AS "Imię", z.nazwisko AS "Nazwisko", 
                        k.nazwa AS "Konkurencja", w.nazwa AS "Zawody", s.status_wyniku
                    FROM Wyniki r
                    JOIN Zawodnicy z ON r.id_zawodnika = z.id_zawodnika
                    JOIN Konkurencje k ON r.id_konkurencji = k.id_konkurencji
                    JOIN Statusy_Wynikow s ON r.id_statusu = s.id_statusu
                    JOIN zawody w ON r.id_zawody = w.id_zawody
                            
                            ORDER BY r.id_wyniku DESC
                """)
            return cur.fetchall()

def delete_results(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Wyniki WHERE id_wyniku = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def add_result(rezultat, miejsce, data_rezultatu, id_zawodnika, id_konkurencji, id_statusu, id_zawody):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Wyniki (rezultat, miejsce, data_rezultatu, id_zawodnika, id_konkurencji, id_statusu, id_zawody) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (rezultat, miejsce, data_rezultatu, id_zawodnika, id_konkurencji, id_statusu, id_zawody))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def update_result(id_wyniku, new_rezultat, new_miejsce, new_data_rezultatu, new_id_zawodnika, new_id_konkurencji, new_id_statusu, new_id_zawody):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Wyniki 
                SET rezultat = %s, miejsce = %s, data_rezultatu = %s, id_zawodnika = %s, 
                    id_konkurencji = %s, id_statusu = %s, id_zawody = %s
                WHERE id_wyniku = %s
                """, (new_rezultat, new_miejsce, new_data_rezultatu, new_id_zawodnika, 
                      new_id_konkurencji, new_id_statusu, new_id_zawody, id_wyniku))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)