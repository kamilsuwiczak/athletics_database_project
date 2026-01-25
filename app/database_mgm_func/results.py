import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_results(filter_by=None, search_term=None):
    conn = get_connection()
    
    # Łączymy tabelę Wyniki z resztą tabel.
    # Dostosowano nazwy kolumn do Twojego schematu SQL:
    # s.status_wyniku, k.nazwa, zw.nazwa
    base_query = """
        SELECT w.id_wyniku,
               z.imie || ' ' || z.nazwisko AS "Zawodnik",
               k.nazwa AS "Konkurencja",
               zw.nazwa AS "Zawody",
               s.status_wyniku AS "Status",
               w.rezultat AS "Rezultat",
               w.miejsce AS "Miejsce",
               w.data_rezultatu AS "Data"
        FROM Wyniki w
        JOIN Zawodnicy z ON w.id_zawodnika = z.id_zawodnika
        JOIN Konkurencje k ON w.id_konkurencji = k.id_konkurencji
        JOIN Zawody zw ON w.id_zawody = zw.id_zawody
        JOIN Statusy_wynikow s ON w.id_statusu = s.id_statusu
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if not filter_by or not search_term:
            cur.execute(base_query + " ORDER BY w.data_rezultatu DESC, w.id_wyniku DESC")
        else:
            filters = {
                'zawodnik': ("(z.nazwisko ILIKE %s OR z.imie ILIKE %s)", [f"%{search_term}%", f"%{search_term}%"]),
                'zawody': ("zw.nazwa ILIKE %s", f"%{search_term}%"),
                'konkurencja': ("k.nazwa ILIKE %s", f"%{search_term}%"),
                'id': ("w.id_wyniku = %s", search_term)
            }

            if filter_by in filters:
                where_clause, params = filters[filter_by]
                query = f"{base_query} WHERE {where_clause} ORDER BY w.data_rezultatu DESC"
                
                if isinstance(params, list):
                    cur.execute(query, tuple(params))
                else:
                    cur.execute(query, (params,))
            else:
                cur.execute(base_query + " ORDER BY w.data_rezultatu DESC")

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
        # Obsługa Unique Constraint z Twojego schematu
        if "unique constraint" in str(e).lower():
            return False, "Ten zawodnik ma już wpisany wynik w tej konkurencji na tych zawodach."
        return False, str(e)

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
        return False, str(e)

def delete_results(ids):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Wyniki WHERE id_wyniku = ANY(%s)", (ids,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def get_raw_result(id_wyniku):
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Pobieramy IDki do edycji
        cur.execute("""
            SELECT id_zawodnika, id_konkurencji, id_zawody, id_statusu, rezultat, miejsce, data_rezultatu
            FROM Wyniki WHERE id_wyniku = %s
        """, (id_wyniku,))
        return cur.fetchone()