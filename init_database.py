import psycopg2

def create_database(cursor, creation_file_path='schema.sql', data_file_path='example_data.sql'):
    with open(creation_file_path, 'r') as f:
        sql_script = f.read()
        cursor.execute(sql_script)

    with open(data_file_path, 'r') as f:
        sql_script = f.read()
        cursor.execute(sql_script)
        
if __name__ == '__main__':
    with psycopg2.connect(
        dbname='athletics_db',
        user='myuser',
        password='mypassword',
        host='localhost',
        port='5432') as conn:
        cursor = conn.cursor()
        create_database(cursor)
        cursor.execute("SELECT * FROM Zawodnicy LEFT JOIN Plcie ON Zawodnicy.id_plci = Plcie.id_plci LEFT JOIN Reprezentanci_zawodnikow ON Zawodnicy.id_reprezentanta = Reprezentanci_zawodnikow.id_reprezentanta;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
