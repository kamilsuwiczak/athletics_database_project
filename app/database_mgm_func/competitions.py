import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_competitions(filter_by=None, search_term=None):
    conn = get_connection()
    
    base_query = """
        SELECT 
            z.id_zawody,
            z.nazwa,
            tz.nazwa_typu AS "Typ",
            p.nazwa AS "Kraj",
            s.nazwa AS "Stadion",
            z.data_rozpoczecia AS "Start",
            z.data_zakonczenia AS "Koniec"
        FROM Zawody z
        JOIN Typy_zawodow tz ON z.id_typu_zawodow = tz.id_typu_zawodow
        JOIN Panstwa p ON z.id_panstwa = p.id_panstwa
        JOIN Stadiony s ON z.id_stadionu = s.id_stadionu
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if not filter_by or not search_term:
            cur.execute(base_query + " ORDER BY z.data_rozpoczecia DESC")
        else:
            filters = {
                'nazwa': ("z.nazwa ILIKE %s", f"%{search_term}%"),
                'typ': ("tz.nazwa_typu ILIKE %s", f"%{search_term}%"),
                'kraj': ("p.nazwa ILIKE %s", f"%{search_term}%"),
                'id': ("z.id_zawody = %s", search_term),
                'stadion': ("s.nazwa ILIKE %s", f"%{search_term}%")
            }

            if filter_by in filters:
                where_clause, params = filters[filter_by]
                query = f"{base_query} WHERE {where_clause} ORDER BY z.data_rozpoczecia DESC"
                cur.execute(query, (params,))
            else:
                cur.execute(base_query + " ORDER BY z.data_rozpoczecia DESC")
                
        return cur.fetchall()

def get_competition_by_id(id_zawody):
    conn = get_connection()
    query = """
        SELECT id_zawody, nazwa, id_typu_zawodow, data_rozpoczecia, 
               data_zakonczenia, id_panstwa, id_stadionu
        FROM Zawody
        WHERE id_zawody = %s
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (id_zawody,))
        return cur.fetchone()


def add_competition(nazwa, id_typu, start, koniec, id_panstwa, id_stadionu):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Zawody 
                (nazwa, id_typu_zawodow, data_rozpoczecia, data_zakonczenia, id_panstwa, id_stadionu) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nazwa, id_typu, start, koniec, id_panstwa, id_stadionu))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def update_competition(id_zawody, nazwa, id_typu, start, koniec, id_panstwa, id_stadionu):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE Zawody 
                SET nazwa=%s, id_typu_zawodow=%s, data_rozpoczecia=%s, 
                    data_zakonczenia=%s, id_panstwa=%s, id_stadionu=%s
                WHERE id_zawody=%s
            """, (nazwa, id_typu, start, koniec, id_panstwa, id_stadionu, id_zawody))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def delete_competitions(ids):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Zawody WHERE id_zawody = ANY(%s)", (ids,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)