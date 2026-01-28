import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection
from database_mgm_func.error_handler import _short_db_error

def get_results(filter_by=None, search_term=None, **advanced_filters):
    conn = get_connection()
    base_query = """
        SELECT w.id_wyniku,
               z.imie || ' ' || z.nazwisko AS "Zawodnik",
               k.nazwa AS "Konkurencja",
               zw.nazwa AS "Zawody",
               s.status_wyniku AS "Status",
               w.rezultat AS "Rezultat", w.miejsce AS "Miejsce", w.data_rezultatu AS "Data"
        FROM Wyniki w
        JOIN Zawodnicy z ON w.id_zawodnika = z.id_zawodnika
        JOIN Konkurencje k ON w.id_konkurencji = k.id_konkurencji
        JOIN Zawody zw ON w.id_zawody = zw.id_zawody
        JOIN Statusy_wynikow s ON w.id_statusu = s.id_statusu
    """
    conditions = []
    params = []

    if filter_by == 'id':
        conditions.append("w.id_wyniku = %s")
        params.append(search_term)

    if advanced_filters.get('f_zawodnik'): 
        conditions.append("(z.nazwisko ILIKE %s OR z.imie ILIKE %s)")
        params.extend([f"%{advanced_filters['f_zawodnik']}%", f"%{advanced_filters['f_zawodnik']}%"])

    if advanced_filters.get('f_id_konkurencji'):
        conditions.append("w.id_konkurencji = %s")
        params.append(advanced_filters['f_id_konkurencji'])

    if advanced_filters.get('f_id_zawody'):
        conditions.append("w.id_zawody = %s")
        params.append(advanced_filters['f_id_zawody'])
        
    if advanced_filters.get('f_miejsce_min'):
        conditions.append("w.miejsce <= %s") 
        params.append(advanced_filters['f_miejsce_min'])

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    full_query = base_query + where_clause + " ORDER BY w.data_rezultatu DESC"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(full_query, params)
        return cur.fetchall()

def add_result(id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Wyniki 
                (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        if "unique constraint" in str(e).lower():
            return False, "Ten zawodnik ma już wpisany wynik w tej konkurencji na tych zawodach."
        return False, _short_db_error(e)

def update_result(id_wyniku, id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE Wyniki 
                SET id_zawodnika=%s, id_konkurencji=%s, id_zawody=%s, id_statusu=%s, 
                    rezultat=%s, miejsce=%s, data_rezultatu=%s
                WHERE id_wyniku=%s
            """, (id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data, id_wyniku))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)

def delete_results(ids):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Wyniki WHERE id_wyniku = ANY(%s)", (ids,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, _short_db_error(e)

def get_raw_result(id_wyniku):
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu
            FROM Wyniki WHERE id_wyniku = %s
        """, (id_wyniku,))
        return cur.fetchone()