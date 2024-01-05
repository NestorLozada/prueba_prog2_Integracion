import http.client
import urllib.parse
import mysql.connector
import json

# Establecer conexión a la base de datos MySQL
db_connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='mi_empresa'
)
db_cursor = db_connection.cursor()

select_query = "SELECT ciudad FROM clientes"

db_cursor.execute(select_query)

results = db_cursor.fetchall()

db_cursor.close()

if results:

    for result in results:
        ciudad = result[0]

        conn = http.client.HTTPConnection('geocode.xyz')
        
        params = urllib.parse.urlencode({
            'auth': '173336102258754186927x71440',
            'locate': f'{ciudad}, Ecuador',
            'region': 'EC',
            'json': 1,
        })

        conn.request('GET', '/?{}'.format(params))

        res = conn.getresponse()
        data = res.read()

        location_info = json.loads(data.decode('utf-8'))

        longitude = location_info.get('longt')
        latitude = location_info.get('latt')


        insert_query = "INSERT INTO ubicaciones (nombre, longitud, latitud) VALUES (%s, %s, %s)"
        insert_values = (ciudad, longitude, latitude)

        db_cursor = db_connection.cursor() 
        db_cursor.execute(insert_query, insert_values)


        db_connection.commit()

        print(f"Longitud y latitud para {ciudad} guardadas en la base de datos.")

db_connection.close()
