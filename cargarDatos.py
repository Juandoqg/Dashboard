import pandas as pd
import mysql.connector

# Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dashboard"
)

cursor = conexion.cursor()

# Lista de archivos que deseas cargar
archivos = ['Docentes_2014.xlsx', 'Docentes_2015.xlsx', 'Docentes_2016.xlsx']

# Definir el query de inserción
insert_query = """
INSERT INTO datos (
    codigo_institucion, ies_padre, institucion_educacion_superior, principal_o_seccional, sector_ies,
    caracter_ies, departamento_domicilio_ies, codigo_municipio, municipio_domicilio_ies, genero_docente,
    tipo_documento, maximo_nivel_formacion_docente, tiempo_dedicacion_docente, tipo_contrato_docente,
    año, semestre, numero_docentes
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Cargar cada archivo en la tabla de MySQL
for archivo in archivos:
    # Leer el archivo Excel
    df = pd.read_excel(archivo)
    
    # Convertir cada fila en una tupla y ejecutarla en el query de inserción
    for _, fila in df.iterrows():
        cursor.execute(insert_query, tuple(fila))
    
    # Confirmar los cambios para el archivo actual
    conexion.commit()
    print(f"Carga de {archivo} completada.")

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
print("Conexión cerrada.")

