import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_venues(filter_by=None, search_term=None, **advanced_filters):
    conn = get_connection()
  
    base_query = """
        SELECT s.id_stadionu, 
               s.nazwa, 
               s.miasto, 
               p.nazwa AS "Kraj",
               p.id_panstwa
        FROM Stadiony s
        JOIN Panstwa p ON s.id_panstwa = p.id_panstwa
    """
    
    conditions = []
    params = []

    if filter_by == 'id' and search_term:
        conditions.append("s.id_stadionu = %s")
        params.append(search_term)

    if advanced_filters.get('f_nazwa'):
        conditions.append("s.nazwa ILIKE %s")
        params.append(f"%{advanced_filters['f_nazwa']}%")
        
    if advanced_filters.get('f_miasto'):
        conditions.append("s.miasto ILIKE %s")
        params.append(f"%{advanced_filters['f_miasto']}%")

    if advanced_filters.get('f_id_panstwa'):
        conditions.append("s.id_panstwa = %s")
        params.append(advanced_filters['f_id_panstwa'])

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    full_query = base_query + where_clause + " ORDER BY s.nazwa ASC"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(full_query, params)
            return cur.fetchall()
        except Exception as e:
            print(f"SQL Error: {e}")
            return []

# --- Reszta funkcji (add_venue, update_venue, delete_venues) BEZ ZMIAN ---
def add_venue(nazwa, miasto, id_panstwa):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Stadiony (nazwa, miasto, id_panstwa) VALUES (%s, %s, %s)", (nazwa, miasto, id_panstwa))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def update_venue(id_stadionu, nazwa, miasto, id_panstwa):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE Stadiony SET nazwa=%s, miasto=%s, id_panstwa=%s WHERE id_stadionu=%s", (nazwa, miasto, id_panstwa, id_stadionu))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def delete_venues(ids):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Stadiony WHERE id_stadionu = ANY(%s)", (ids,))
            conn.commit()
            return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)