import psycopg2
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)
cursor = conn.cursor()

# URL de la página de sismología
url = "https://www.sismologia.cl/index.html"
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, 'html.parser')

# Buscar la tabla con la clase 'sismologia'
table = soup.find('table', class_='sismologia')

# Insertar datos en la base de datos
insert_query  = """
INSERT INTO sismos (id, fecha_hora, ubicacion, profundidad, magnitud) VALUES (%s, %s, %s, %s, %s)
"""

check_query = """
SELECT 1 FROM sismos WHERE id = %s
"""

for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) == 3:
        link_tag = cols[0].find('a')
        href = link_tag['href']
        id = href.split('/')[-1].split('.')[0]
        fecha_y_lugar = cols[0].text.split('\n')
        fecha_hora = datetime.strptime(fecha_y_lugar[0], '%Y-%m-%d %H:%M:%S')
        ubicacion = fecha_y_lugar[1].strip()
        profundidad = int(cols[1].text.replace(' km', ''))
        magnitud = float(cols[2].text.strip())

        cursor.execute(check_query, (id,))
        if cursor.fetchone() is None:
            # Ejecutar la consulta
            cursor.execute(insert_query , (id, fecha_hora, ubicacion, profundidad, magnitud))

# Commit los cambios y cerrar conexión
conn.commit()
cursor.close()
conn.close()
