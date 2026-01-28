import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error

def get_competitions(filter_by=None, search_term=None, **advanced_filters):
    conn = get_connection()
   
    base_query = """
        SELECT z.id_zawody,
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
    
    conditions = []
    params = []

    if filter_by == 'id' and search_term:
        conditions.append("z.id_zawody = %s")
        params.append(search_term)

    if advanced_filters.get('f_nazwa'):
        conditions.append("z.nazwa ILIKE %s")
        params.append(f"%{advanced_filters['f_nazwa']}%")

    if advanced_filters.get('f_id_typu'):
        conditions.append("z.id_typu_zawodow = %s")
        params.append(advanced_filters['f_id_typu'])

    if advanced_filters.get('f_id_panstwa'):
        conditions.append("z.id_panstwa = %s")
        params.append(advanced_filters['f_id_panstwa'])

    if advanced_filters.get('f_rok'):
        conditions.append("EXTRACT(YEAR FROM z.data_rozpoczecia) = %s")
        params.append(advanced_filters['f_rok'])

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    full_query = base_query + where_clause + " ORDER BY z.data_rozpoczecia DESC"
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(full_query, params)
            return cur.fetchall()
        except Exception as e:
            print(f"SQL Error: {e}")
            return []

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
        return False, _short_db_error(e)

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
        return False, _short_db_error(e)

def delete_competitions(ids):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Zawody WHERE id_zawody = ANY(%s)", (ids,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)