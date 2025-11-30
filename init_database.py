import psycopg2

def create_database(cursor, creation_file_path='schema.sql'):
    with open(creation_file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        cursor.execute(sql_script)

def load_data(cursor, data_file_path='example_data.sql'):
    with open(data_file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        cursor.execute(sql_script)
        
if __name__ == '__main__':
    with psycopg2.connect(
        dbname='athletics_db',
        user='myuser',
        password='mypassword',
        host='localhost',
        port='5432') as conn:
        conn.set_client_encoding('UTF8')
        cursor = conn.cursor()
        create_database(cursor)
        load_data(cursor)
        cursor.execute("SELECT * from wyniki LEFT JOIN statusy_wynikow ON wyniki.id_statusu = statusy_wynikow.id_statusu LEFT JOIN Zawodnicy ON wyniki.id_zawodnika = Zawodnicy.id_zawodnika;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
