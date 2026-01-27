import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_world_records(filter_by=None, search_term=None, **advanced_filters):
    conn = get_connection()

    base_query = """
        SELECT 
            CONCAT(rs.id_konkurencji, '_', rs.id_zawodnika) AS composite_id,
            k.id_konkurencji,
            z.id_zawodnika,
            k.nazwa AS "Konkurencja",
            z.imie || ' ' || z.nazwisko AS "Zawodnik",
            p.nazwa AS "Kraj",
            rs.rezultat AS "Wynik",
            rs.data_rezultatu AS "Data"
        FROM Rekordy_swiata rs
        JOIN Konkurencje k ON rs.id_konkurencji = k.id_konkurencji
        JOIN Zawodnicy z ON rs.id_zawodnika = z.id_zawodnika
        JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
    """
    
    conditions = []
    params = []

   
    if filter_by == 'id' and search_term:
        try:
            id_k, id_z = search_term.split('_')
            conditions.append("rs.id_konkurencji = %s AND rs.id_zawodnika = %s")
            params.extend([id_k, id_z])
        except ValueError:
            pass # Błędny format ID

    if advanced_filters.get('f_konkurencja'):
        conditions.append("k.nazwa ILIKE %s")
        params.append(f"%{advanced_filters['f_konkurencja']}%")
        
    if advanced_filters.get('f_zawodnik'):
        conditions.append("(z.nazwisko ILIKE %s OR z.imie ILIKE %s)")
        val = f"%{advanced_filters['f_zawodnik']}%"
        params.extend([val, val])

    if advanced_filters.get('f_kraj'):
        conditions.append("p.nazwa ILIKE %s")
        params.append(f"%{advanced_filters['f_kraj']}%")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    full_query = base_query + where_clause + " ORDER BY k.nazwa ASC"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(full_query, params)
            return cur.fetchall()
        except Exception as e:
            print(f"SQL Error: {e}")
            return []

def add_world_record(id_konkurencji, id_zawodnika, rezultat, data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Rekordy_swiata (id_konkurencji, id_zawodnika, rezultat, data_rezultatu)
                VALUES (%s, %s, %s, %s)
            """, (id_konkurencji, id_zawodnika, rezultat, data))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        if "unique constraint" in str(e).lower() or "primary key" in str(e).lower():
            return False, "Ten zawodnik ma już rekord świata w tej konkurencji."
        return False, str(e)

def update_world_record(old_composite_id, rezultat, data):
    """
    Edycja pozwala zmienić wynik i datę. 
    Zmiana zawodnika lub konkurencji wymagałaby usunięcia i dodania nowego wpisu (ze względu na PK).
    """
    conn = get_connection()
    try:
        id_k, id_z = old_composite_id.split('_')
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE Rekordy_swiata 
                SET rezultat = %s, data_rezultatu = %s
                WHERE id_konkurencji = %s AND id_zawodnika = %s
            """, (rezultat, data, id_k, id_z))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def delete_world_records(composite_ids):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
         
            for cid in composite_ids:
                id_k, id_z = cid.split('_')
                cur.execute("""
                    DELETE FROM Rekordy_swiata 
                    WHERE id_konkurencji = %s AND id_zawodnika = %s
                """, (id_k, id_z))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def get_options_data():
    conn = get_connection()
    data = {}
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id_konkurencji, nazwa FROM Konkurencje ORDER BY nazwa")
        data['konkurencje'] = cur.fetchall()
        
        cur.execute("SELECT id_zawodnika, imie, nazwisko, p.nazwa as kraj FROM Zawodnicy z JOIN Panstwa p ON z.id_panstwa = p.id_panstwa ORDER BY nazwisko")
        data['zawodnicy'] = cur.fetchall()
    return data

