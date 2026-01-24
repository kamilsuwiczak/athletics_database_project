import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_world_records(filter_by = None, search_term = None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if filter_by == 'competition':
                query = """
                SELECT wr.rezultat, wr.data_rezultatu, z.imie, z.nazwisko , k.nazwa FROM Rekordy_Swiata wr 
                            JOIN Zawodnicy z ON wr.id_zawodnika = z.id_zawodnika 
                            JOIN Konkurencje k ON wr.id_konkurencji = k.id_konkurencji 
                            WHERE k.nazwa ILIKE %s
                            ORDER BY wr.rezultat DESC;
                """
                param = f"%{search_term}%"
                cur.execute(query, (param,))
            else:
                cur.execute("""
                SELECT wr.rezultat, wr.data_rezultatu, z.imie, z.nazwisko , k.nazwa FROM Rekordy_Swiata wr 
                            JOIN Zawodnicy z ON wr.id_zawodnika = z.id_zawodnika 
                            JOIN Konkurencje k ON wr.id_konkurencji = k.id_konkurencji ORDER BY wr.rezultat DESC;
             """)
            return cur.fetchall()

def add_world_record(rezultat, data_rezultatu, id_zawodnika, id_konkurencji):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Rekordy_swiata (rezultat, data_rezultatu, id_zawodnika, id_konkurencji) 
                VALUES (%s, %s, %s, %s)
                """, (rezultat, data_rezultatu, id_zawodnika, id_konkurencji))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_world_records(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Rekordy_swiata WHERE id_rekordu = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
        
def update_world_record(id_rekordu, new_rezultat, new_data_rezultatu, new_id_zawodnika, new_id_konkurencji):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Rekordy_swiata 
                SET rezultat = %s, data_rezultatu = %s, id_zawodnika = %s, id_konkurencji = %s 
                WHERE id_rekordu = %s
                """, (new_rezultat, new_data_rezultatu, new_id_zawodnika, new_id_konkurencji, id_rekordu))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

