import mysql.connector

# Conectar a la base de datos
conn = mysql.connector.connect(
    host='database-test2.cta44ua6myzs.us-east-1.rds.amazonaws.com',
    user='admin',
    password='Barranco2.',
    database='ISI'
)

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Definir comandos SQL para eliminar las tablas si existen
drop_tables = [
    "DROP TABLE IF EXISTS Cuotas",
    "DROP TABLE IF EXISTS Eventos",
    "DROP TABLE IF EXISTS Deportes",
    "DROP TABLE IF EXISTS Bookies"
]

# Ejecutar los comandos SQL para eliminar las tablas
for query in drop_tables:
    cursor.execute(query)
    conn.commit()

# Definir comandos SQL para crear las tablas nuevamente
create_tables = [
    """
    CREATE TABLE Deportes (
        id_deporte INT AUTO_INCREMENT PRIMARY KEY,
        nombre_deporte VARCHAR(255) UNIQUE
    )
    """,
    """
    CREATE TABLE Eventos (
        id_evento INT AUTO_INCREMENT PRIMARY KEY,
        id_deporte INT,
        nombre_evento VARCHAR(255),
        FOREIGN KEY (id_deporte) REFERENCES Deportes(id_deporte)
    )
    """,
    """
    CREATE TABLE Bookies (
        id_bookie INT AUTO_INCREMENT PRIMARY KEY,
        nombre_bookie VARCHAR(255) UNIQUE
    )
    """,
    """
    CREATE TABLE Cuotas (
        id_cuota INT AUTO_INCREMENT PRIMARY KEY,
        id_evento INT,
        id_bookie INT,
        tipo_apuesta VARCHAR(1),
        cuota DECIMAL(10, 2),
        FOREIGN KEY (id_evento) REFERENCES Eventos(id_evento),
        FOREIGN KEY (id_bookie) REFERENCES Bookies(id_bookie)
    )
    """
]

# Ejecutar los comandos SQL para crear las tablas
for query in create_tables:
    cursor.execute(query)
    conn.commit()

# Leer el archivo con los datos de las cuotas
with open('cuotas_totales.txt', 'r', encoding='utf-8') as file:
    deporte = None
    id_deporte = None
    id_evento = None  # Inicializar id_evento
    id_bookie = None  # Inicializar id_bookie
    for line in file:
        # Eliminar los espacios en blanco al principio y al final de la línea
        line = line.strip()
        if line.startswith('Deporte: '):
            # Extraer el nombre del deporte
            deporte = line.split(':')[1].strip()
            # Insertar el deporte en la tabla Deportes si no existe
            cursor.execute("INSERT IGNORE INTO Deportes (nombre_deporte) VALUES (%s)", (deporte,))
            conn.commit()
            # Obtener el ID del deporte insertado o existente
            cursor.execute("SELECT id_deporte FROM Deportes WHERE nombre_deporte = %s", (deporte,))
            id_deporte = cursor.fetchone()[0]
        elif line.startswith('Local:'):
            local = line.split(': ')[1].strip()
        elif line.startswith('Visitante:'):
            visitante = line.split(': ')[1].strip()
            # Insertar el evento en la tabla Eventos
            cursor.execute("INSERT IGNORE INTO Eventos (id_deporte, nombre_evento) VALUES (%s, %s)", (id_deporte, f"{local} vs {visitante}"))
            conn.commit()
            # Obtener el ID del evento insertado o existente
            cursor.execute("SELECT id_evento FROM Eventos WHERE nombre_evento = %s", (f"{local} vs {visitante}",))
            id_evento = cursor.fetchone()[0]
            # Leer el resultado adicional para evitar el error "Unread result found"
            cursor.fetchall()
        elif line.startswith('-'):
            bookie = line.split('-')[1].strip()
            # Insertar la bookie en la tabla Bookies si no existe
            cursor.execute("INSERT IGNORE INTO Bookies (nombre_bookie) VALUES (%s)", (bookie,))
            conn.commit()
            # Obtener el ID de la bookie insertada o existente
            cursor.execute("SELECT id_bookie FROM Bookies WHERE nombre_bookie = %s", (bookie,))
            id_bookie = cursor.fetchone()[0]
        elif line.startswith('1:'):
            cuota = line.split(': ')[1].strip()
            # Insertar la cuota para 1 en la tabla Cuotas
            cursor.execute("INSERT INTO Cuotas (id_evento, id_bookie, tipo_apuesta, cuota) VALUES (%s, %s, %s, %s)", (id_evento, id_bookie, '1', cuota))
            conn.commit()
        elif line.startswith('2:'):
            cuota = line.split(': ')[1].strip()
            # Insertar la cuota para 2 en la tabla Cuotas
            cursor.execute("INSERT INTO Cuotas (id_evento, id_bookie, tipo_apuesta, cuota) VALUES (%s, %s, %s, %s)", (id_evento, id_bookie, '2', cuota))
            conn.commit()
        elif line.startswith('X:'):
            cuota = line.split(': ')[1].strip()
            # Insertar la cuota para X en la tabla Cuotas
            cursor.execute("INSERT INTO Cuotas (id_evento, id_bookie, tipo_apuesta, cuota) VALUES (%s, %s, %s, %s)", (id_evento, id_bookie, 'X', cuota))
            conn.commit()

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

