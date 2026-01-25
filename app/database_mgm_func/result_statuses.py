import psycopg2
from psycopg2.extras import RealDictCursor
from database_mgm_func.db_connection import get_connection

def get_statuses(filter_by=None, search_term=None):
    conn = get_connection()
    
    # WAŻNE: W bazie masz 'status_wyniku', ale widok oczekuje 'nazwa'.
    # Używamy aliasu, żeby frontend działał bez zmian.
    base_query = """
        SELECT id_statusu, status_wyniku AS "nazwa"
        FROM Statusy_wynikow
    """
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if not filter_by or not search_term:
            cur.execute(base_query + " ORDER BY id_statusu ASC")
        else:
            # Filtrowanie
            filters = {
                'nazwa': ("status_wyniku ILIKE %s", f"%{search_term}%"),
                'id': ("id_statusu = %s", search_term)
            }

            if filter_by in filters:
                where_clause, params = filters[filter_by]
                query = f"{base_query} WHERE {where_clause} ORDER BY status_wyniku ASC"
                cur.execute(query, (params,))
            else:
                cur.execute(base_query + " ORDER BY id_statusu ASC")
                
        return cur.fetchall()

def add_result_status(status_wyniku):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Statusy_wynikow (status_wyniku) VALUES (%s)", (status_wyniku,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def delete_result_statuses(ids_to_delete):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Statusy_wynikow WHERE id_statusu = ANY(%s)", (ids_to_delete,))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)

def update_result_status(id_statusu, status_wyniku):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE Statusy_wynikow 
                    SET status_wyniku = %s
                    WHERE id_statusu = %s
                """, (status_wyniku, id_statusu))
                conn.commit()
                return True, None
        except Exception as e:
            conn.rollback()
            error_msg = str(e).split('CONTEXT:')[0] if 'CONTEXT:' in str(e) else str(e)
            return False, error_msg
