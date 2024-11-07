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
archivos = ['Docentes_2021.xlsx', 'Docentes_2022.xlsx', 'Docentes_2023.xlsx']

# Definir el query de inserción
insert_query = """
INSERT INTO datos (
    codigo_institucion, ies_padre, institucion_educacion_superior, principal_o_seccional, id_sector_ies ,sector_ies, id_caracter_ies,
    caracter_ies, id_departamento_domicilio_ies, departamento_domicilio_ies, codigo_municipio, municipio_domicilio_ies, id_genero , genero_docente,
    id_maximo_nivel_formacion_docente, maximo_nivel_formacion_docente, id_tiempo_dedicacion_docente, tiempo_dedicacion_docente, id_tipo_contrato_docente, tipo_contrato_docente,
    año, semestre, numero_docentes
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


for archivo in archivos:
    # Leer el archivo Excel
    df = pd.read_excel(archivo)
    
    # Convertir cada fila en una tupla y ejecutarla en el query de inserción
    for _, fila in df.iterrows():
        cursor.execute(insert_query, tuple(fila))
    conexion.commit()
    print(f"Carga de {archivo} completada.")

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
print("Conexión cerrada.")

