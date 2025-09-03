import mysql.connector
import csv

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tu_password",
    database="mi_base"
)

cursor = conexion.cursor()

# Insertar clientes desde un CSV
with open("clientes.csv", "r") as archivo:
    lector = csv.reader(archivo)
    next(lector)  # saltar encabezado
    for fila in lector:
        cursor.execute(
            "INSERT INTO clientes (id, nombre, correo) VALUES (%s, %s, %s)",
            fila
        )

# Insertar usuarios desde un CSV
with open("usuarios.csv", "r") as archivo:
    lector = csv.reader(archivo)
    next(lector)
    for fila in lector:
        cursor.execute(
            "INSERT INTO usuarios (id, usuario, contraseña) VALUES (%s, %s, %s)",
            fila
        )

conexion.commit()
cursor.close()
conexion.close()
