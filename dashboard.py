import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import mysql.connector
from dash.dependencies import Input, Output
import plotly.express as px

# Conectar a MySQL y cargar los datos
def cargar_datos():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto por tu usuario de MySQL
        password="",  # Cambia esto por tu contraseña de MySQL
        database="dashboard"  # Cambia esto por tu nombre de base de datos
    )
    query = "SELECT * FROM datos"
    df = pd.read_sql(query, conexion)
    conexion.close()
    return df

# Cargar datos en DataFrame
df = cargar_datos()

# Inicializar la app de Dash con un tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout del Dashboard
app.layout = html.Div([
    html.H1("Dashboard de Docentes", style={'textAlign': 'center', 'color': '#007bff'}),

    # Sección de Consultas Fijas
    html.Div([
        dbc.Card([
            dbc.CardHeader("Consulta 1: Total de Docentes Femeninos con Doctorado en 2014", style={'fontWeight': 'bold'}),
            dbc.CardBody([
                dcc.Graph(id="grafico-consulta-fija-1"),
                html.Button("Ejecutar Consulta 1", id="btn-consulta-1", className="btn btn-custom"),
            ])
        ]),
        dbc.Card([
            dbc.CardHeader("Consulta 2: Total de Mujeres por Máximo Nivel de Formación", style={'fontWeight': 'bold'}),
            dbc.CardBody([
                dcc.Graph(id="grafico-consulta-fija-2"),
                html.Button("Ejecutar Consulta 2", id="btn-consulta-2", className="btn btn-custom"),
            ])
        ]),
        dbc.Card([
            dbc.CardHeader("Consulta 3: Total de Docentes por Género", style={'fontWeight': 'bold'}),
            dbc.CardBody([
                dcc.Graph(id="grafico-consulta-fija-3"),
                html.Button("Ejecutar Consulta 3", id="btn-consulta-3", className="btn btn-custom"),
            ])
        ]),
    ], style={'margin': '20px'}),

    # Sección de Consultas Variables
    html.Div([
        html.H3("Consultas Variables"),
        dcc.Dropdown(
            id="filtro-consulta-variable",
            options=[
                {"label": "Distribución de Docentes por Género y Nivel de Formación", "value": "distribucion_genero_nivel"},
                {"label": "Total de Docentes por Tipo de Contrato", "value": "total_por_tipo_contrato"},
                {"label": "Total de Docentes por Municipio", "value": "total_por_municipio"},
            ],
            placeholder="Selecciona una consulta",
            style={'color': '#495057'}
        ),
        dcc.Graph(id="grafico-consulta-variable"),
    ]),

    # Cifras Relevantes
    html.Div(id="cifras-relevantes"),
])

# Callback para las consultas fijas
@app.callback(
    Output("grafico-consulta-fija-1", "figure"),
    Output("grafico-consulta-fija-2", "figure"),
    Output("grafico-consulta-fija-3", "figure"),
    [Input("btn-consulta-1", "n_clicks"),
     Input("btn-consulta-2", "n_clicks"),
     Input("btn-consulta-3", "n_clicks")]
)
def actualizar_graficos_fijos(n1, n2, n3):
    # Consulta 1: Total de Docentes Femeninos con Doctorado en 2014, 2015 y 2016
    anios = [2021, 2022, 2023]
    cantidad_femeninos_doctorado = []

    for anio in anios:
        total_femeninos_doctorado = df[(df['genero_docente'] == 'FEMENINO') &
                                        (df['maximo_nivel_formacion_docente'] == 'DOCTORADO') &
                                        (df['año'] == anio)]
        cantidad = total_femeninos_doctorado['numero_docentes'].sum()
        cantidad_femeninos_doctorado.append(cantidad)

    # Cambiar años a cadenas para evitar el problema de los números continuos
    anios_str = [str(anio) for anio in anios]

    fig1 = px.bar(x=anios_str, y=cantidad_femeninos_doctorado,
                  title="Cantidad de Docentes Femeninos con Doctorado en 2014, 2015 y 2016",
                  labels={'x': 'Año', 'y': 'Cantidad de Docentes'},
                  text=cantidad_femeninos_doctorado)
    fig1.update_traces(texttemplate='%{text}', textposition='outside')
    fig1.update_layout(yaxis_title='Cantidad de Docentes', xaxis_title='Año')
    # Consulta 2: Total de Mujeres por Máximo Nivel de Formación
    fig2 = px.bar(df[df['genero_docente'] == 'FEMENINO'],
                  x="maximo_nivel_formacion_docente", y="numero_docentes", title="Total de Mujeres por Máximo Nivel de Formación")

    # Consulta 3: Total de Docentes por Género
    fig3 = px.histogram(df, x="genero_docente", y="numero_docentes", 
                        title="Total de Docentes por Género", barmode="group")

    return fig1, fig2, fig3

# Callback para las consultas variables
@app.callback(
    Output("grafico-consulta-variable", "figure"),
    [Input("filtro-consulta-variable", "value")]
)
def actualizar_grafico_variable(seleccion):
    if seleccion == "distribucion_genero_nivel":
        fig = px.histogram(df, x="genero_docente", color="maximo_nivel_formacion_docente", 
                           title="Distribución de Docentes por Género y Máximo Nivel de Formación")
    elif seleccion == "total_por_tipo_contrato":
        fig = px.bar(df, x="tipo_contrato_docente", y="numero_docentes", 
                     title="Total de Docentes por Tipo de Contrato")
    elif seleccion == "total_por_municipio":
        fig = px.bar(df, x="municipio_domicilio_ies", y="numero_docentes", 
                     title="Total de Docentes por Municipio")
    else:
        fig = {}
    
    return fig

# Callback para cifras relevantes
@app.callback(
    Output("cifras-relevantes", "children"),
    [Input("btn-consulta-1", "n_clicks"),
     Input("btn-consulta-2", "n_clicks"),
     Input("btn-consulta-3", "n_clicks")]
)
def mostrar_cifras_relevantes(n1, n2, n3):
    total_docentes = df['numero_docentes'].sum()
    total_hombres = df[df['genero_docente'] == 'MASCULINO']['numero_docentes'].sum()
    total_mujeres = df[df['genero_docente'] == 'FEMENINO']['numero_docentes'].sum()
    promedio_nivel_formacion = df['maximo_nivel_formacion_docente'].mode()[0]  # Modo como promedio representativo
    total_por_municipio = df.groupby('municipio_domicilio_ies')['numero_docentes'].sum()

    return [
        html.Div(f"Total de Docentes: {total_docentes}", style={'fontWeight': 'bold'}),
        html.Div(f"Total de Hombres: {total_hombres}", style={'fontWeight': 'bold'}),
        html.Div(f"Total de Mujeres: {total_mujeres}", style={'fontWeight': 'bold'}),
        html.Div(f"Máximo Nivel de Formación más Común: {promedio_nivel_formacion}", style={'fontWeight': 'bold'}),
        html.Div(f"Docentes por Municipio: {total_por_municipio.to_dict()}", style={'fontWeight': 'bold'}),
    ]

# Ejecutar la app
if __name__ == "__main__":
    app.run_server(debug=True)
