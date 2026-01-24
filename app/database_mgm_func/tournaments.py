import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_tournaments(filter_by = None, search_term = None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'name':
                query = """
                SELECT t.id_zawody, t.nazwa, t.data_rozpoczecia, t.data_zakonczenia,tt.nazwa_typu as typ_zawodow, 
                            p.nazwa AS panstwo, s.nazwa AS stadion FROM Zawody t 
                            JOIN Panstwa p ON t.id_panstwa = p.id_panstwa 
                            JOIN Stadiony s ON t.id_stadionu = s.id_stadionu 
                            JOIN Typy_zawodow tt ON t.id_typu_zawodow = tt.id_typu_zawodow
                            WHERE t.nazwa ILIKE %s
                            ORDER BY t.data_rozpoczecia DESC;
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            elif filter_by == 'country':
                query = """
                SELECT t.id_zawody, t.nazwa, t.data_rozpoczecia, t.data_zakonczenia,tt.nazwa_typu as typ_zawodow, 
                            p.nazwa AS panstwo, s.nazwa AS stadion FROM Zawody t 
                            JOIN Panstwa p ON t.id_panstwa = p.id_panstwa 
                            JOIN Stadiony s ON t.id_stadionu = s.id_stadionu 
                            JOIN Typy_zawodow tt ON t.id_typu_zawodow = tt.id_typu_zawodow
                            WHERE p.nazwa ILIKE %s
                            ORDER BY t.data_rozpoczecia DESC;
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            elif filter_by == 'tournament_type':
                query = """
                SELECT t.id_zawody, t.nazwa, t.data_rozpoczecia, t.data_zakonczenia,tt.nazwa_typu as typ_zawodow, 
                            p.nazwa AS panstwo, s.nazwa AS stadion FROM Zawody t 
                            JOIN Panstwa p ON t.id_panstwa = p.id_panstwa 
                            JOIN Stadiony s ON t.id_stadionu = s.id_stadionu 
                            JOIN Typy_zawodow tt ON t.id_typu_zawodow = tt.id_typu_zawodow
                            WHERE tt.nazwa_typu ILIKE %s
                            ORDER BY t.data_rozpoczecia DESC;
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            
            else:
                cur.execute("""
                SELECT t.id_zawody, t.nazwa, t.data_rozpoczecia, t.data_zakonczenia,tt.nazwa_typu as typ_zawodow, 
                            p.nazwa AS panstwo, s.nazwa AS stadion FROM Zawody t 
                            JOIN Panstwa p ON t.id_panstwa = p.id_panstwa 
                            JOIN Stadiony s ON t.id_stadionu = s.id_stadionu 
                            JOIN Typy_zawodow tt ON t.id_typu_zawodow = tt.id_typu_zawodow
                            ORDER BY t.data_rozpoczecia DESC;
             """)
            return cur.fetchall()
        
def add_tournament(nazwa, data_rozpoczecia, data_zakonczenia, id_typu_zawodow, id_panstwa, id_stadionu):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Zawody (nazwa, data_rozpoczecia, data_zakonczenia, id_typu_zawodow, id_panstwa, id_stadionu) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (nazwa, data_rozpoczecia, data_zakonczenia, id_typu_zawodow, id_panstwa, id_stadionu))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
        
def delete_tournaments(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Zawody WHERE id_zawody = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)


