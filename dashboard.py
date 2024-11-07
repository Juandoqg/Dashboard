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
    dbc.Container([
        # Sección de Consultas Fijas con diseño de cuadrícula
        dbc.Row([ 
            dbc.Col(dbc.Card([ 
                dbc.CardHeader("Consulta 1: Docentes Femeninos con Doctorado (2021-2023)"), 
                dbc.CardBody([ 
                    dcc.Graph(id="grafico-consulta-fija-1"),
                    html.Button("Ejecutar Consulta 1", id="btn-consulta-1", className="btn btn-custom"),
                ]) 
            ]), xs=12, sm=12, md=6, lg=4),
            
            dbc.Col(dbc.Card([ 
                dbc.CardHeader("Consulta 2: Mujeres por Nivel de Formación"), 
                dbc.CardBody([ 
                    dcc.Graph(id="grafico-consulta-fija-2"), 
                    html.Button("Ejecutar Consulta 2", id="btn-consulta-2", className="btn btn-custom"),
                ]) 
            ]), xs=12, sm=12, md=6, lg=4),
            
            dbc.Col(dbc.Card([ 
                dbc.CardHeader("Consulta 3: Total de Docentes por Género"), 
                dbc.CardBody([ 
                    dcc.Graph(id="grafico-consulta-fija-3"), 
                    html.Button("Ejecutar Consulta 3", id="btn-consulta-3", className="btn btn-custom"),
                ]) 
            ]), xs=12, sm=12, md=6, lg=4),
        ], className="g-3"),

        # Sección de Consultas Variables con Dropdown y Checkboxes
        html.Div([ 
            html.H3("Consultas Variables"), 
            dbc.Row([ 
                dbc.Col([ 
                    dcc.Dropdown( 
                        id="filtro-consulta-variable", 
                        options=[ 
                            {"label": "Distribución de Docentes por Género y Nivel", "value": "distribucion_genero_nivel"},
                            {"label": "Total de Docentes por Tipo de Contrato", "value": "total_por_tipo_contrato"},
                            {"label": "Total de Docentes por Municipio", "value": "total_por_municipio"},
                        ], 
                        placeholder="Selecciona una consulta", 
                    ), 
                ], xs=12, sm=12, md=6), 
                dbc.Col([ 
                    dcc.Checklist( 
                        id="checklist-genero", 
                        options=[ 
                            {'label': 'Masculino', 'value': 'MASCULINO'}, 
                            {'label': 'Femenino', 'value': 'FEMENINO'},
                        ], 
                        value=['MASCULINO', 'FEMENINO'], 
                        labelStyle={'display': 'inline-block'}
                    ), 
                ], xs=12, sm=12, md=6),
            ]), 

            # Checklist de Años
            dcc.Checklist(
                id="checklist-anios",
                options=[
                    {"label": "2021", "value": 2021},
                    {"label": "2022", "value": 2022},
                    {"label": "2023", "value": 2023},
                ],
                value=[2021, 2022, 2023],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id="grafico-consulta-variable"),
        ], className="my-4"),

        # Cifras Relevantes
        html.Div(id="cifras-relevantes", className="my-4"),
    ], className="mt-3 mb-3",fluid=True)
])

@app.callback(
    Output("grafico-consulta-fija-1", "figure"),
    Output("grafico-consulta-fija-2", "figure"),
    Output("grafico-consulta-fija-3", "figure"),
    [Input("btn-consulta-1", "n_clicks"),
     Input("btn-consulta-2", "n_clicks"),
     Input("btn-consulta-3", "n_clicks")]
)
def actualizar_graficos_fijos(n1, n2, n3):
    # Consulta 1: Total de Docentes Femeninos con Doctorado en 2021, 2022, 2023
    anios = [2021, 2022, 2023]
    cantidad_femeninos_doctorado = []

    for anio in anios:
        total_femeninos_doctorado = df[(df['genero_docente'] == 'FEMENINO') &
                                        (df['maximo_nivel_formacion_docente'] == 'DOCTORADO') &
                                        (df['año'] == anio)]
        cantidad = total_femeninos_doctorado['numero_docentes'].sum()
        cantidad_femeninos_doctorado.append(cantidad)

    fig1 = px.bar(x=anios, y=cantidad_femeninos_doctorado,
                  title="Docentes Femeninos con Doctorado (2021-2023)",
                  labels={'x': 'Año', 'y': 'Cantidad'},
                  text=cantidad_femeninos_doctorado)
    fig1.update_traces(texttemplate='%{text}', textposition='outside')

    # Consulta 2: Total de Mujeres por Máximo Nivel de Formación (Gráfico de torta)
    mujeres_formacion = df[df['genero_docente'] == 'FEMENINO'].groupby('maximo_nivel_formacion_docente').sum().reset_index()
    fig2 = px.pie(mujeres_formacion, values="numero_docentes", names="maximo_nivel_formacion_docente",
                  title="Total de Mujeres por Nivel de Formación")

    # Consulta 3: Total de Docentes por Género
    fig3 = px.histogram(df, x="genero_docente", y="numero_docentes",
                        title="Total de Docentes por Género", barmode="group")
    fig3.update_layout(
        xaxis_title="Género",
        yaxis_title="Cantidad"
    )

    return fig1, fig2, fig3

# Callback para las consultas variables
@app.callback(
    Output("grafico-consulta-variable", "figure"),
    [Input("filtro-consulta-variable", "value"),
     Input("checklist-anios", "value"),
     Input("checklist-genero", "value")]
)
def actualizar_grafico_variable(seleccion, anios_seleccionados, genero_seleccionado):
    datos_filtrados = df[(df['año'].isin(anios_seleccionados)) & (df['genero_docente'].isin(genero_seleccionado))]
    
    if seleccion == "distribucion_genero_nivel":
        fig = px.histogram(datos_filtrados, x="genero_docente", y="numero_docentes",  color="maximo_nivel_formacion_docente", 
                           title="Distribución de Docentes por Género y Nivel de Formación",
                           labels={'genero_docente': 'Género', 'maximo_nivel_formacion_docente': 'Nivel de Formación'})
        fig.update_layout(yaxis_title="Cantidad")
    
    elif seleccion == "total_por_tipo_contrato":
        fig = px.bar(datos_filtrados, x="tipo_contrato_docente", y="numero_docentes", 
                     title="Docentes por Tipo de Contrato",
                     labels={'tipo_contrato_docente': 'Tipo de Contrato', 'numero_docentes': 'Cantidad de Docentes'})

    elif seleccion == "total_por_municipio":
        fig = px.bar(datos_filtrados, x="municipio_domicilio_ies", y="numero_docentes", 
                     title="Docentes por Municipio",
                     labels={'municipio_domicilio_ies': 'Municipio', 'numero_docentes': 'Cantidad de Docentes'})
    
    else:
        fig = {}  
    
    return fig

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
    nivel_formacion_comun = df['maximo_nivel_formacion_docente'].mode()[0]
    total_docentes_doctorado = df[df['maximo_nivel_formacion_docente'] == 'DOCTORADO']['numero_docentes'].sum()
    total_mujeres_doctorado = df[(df['genero_docente'] == 'FEMENINO') & 
                                 (df['maximo_nivel_formacion_docente'] == 'DOCTORADO')]['numero_docentes'].sum()
    total_hombres_doctorado = df[(df['genero_docente'] == 'MASCULINO') & 
                                 (df['maximo_nivel_formacion_docente'] == 'DOCTORADO')]['numero_docentes'].sum()

    tarjetas = [
        dbc.Card([
            dbc.CardBody([
                html.H5("Total de Docentes", className="card-title"),
                html.P(f"{total_docentes}", className="card-text")
            ])
        ], color="primary", inverse=True, className="m-3"),
        
        dbc.Card([
            dbc.CardBody([
                html.H5("Total de Hombres", className="card-title"),
                html.P(f"{total_hombres}", className="card-text")
            ])
        ], color="info", inverse=True, className="m-3"),
        
        dbc.Card([
            dbc.CardBody([
                html.H5("Total de Mujeres", className="card-title"),
                html.P(f"{total_mujeres}", className="card-text")
            ])
        ], color="danger", inverse=True, className="m-3"),
        
        dbc.Card([
            dbc.CardBody([
                html.H5("Nivel de Formación más Común", className="card-title"),
                html.P(nivel_formacion_comun, className="card-text")
            ])
        ], color="warning", inverse=True, className="m-3"),
        
        dbc.Card([
            dbc.CardBody([
                html.H5("Total de Docentes con Doctorado", className="card-title"),
                html.P(f"{total_docentes_doctorado}", className="card-text")
            ])
        ], color="success", inverse=True, className="m-3"),
        
        dbc.Card([
            dbc.CardBody([
                html.H5("Total de Mujeres con Doctorado", className="card-title"),
                html.P(f"{total_mujeres_doctorado}", className="card-text")
            ])
        ], color="secondary", inverse=True, className="m-3"),
        
        dbc.Card([
            dbc.CardBody([
                html.H5("Total de Hombres con Doctorado", className="card-title"),
                html.P(f"{total_hombres_doctorado}", className="card-text")
            ])
        ], color="dark", inverse=True, className="m-3"),
    ]

    # Agrupar tarjetas en una fila con diseño de cuadrícula, asegurando que haya 3 tarjetas por fila en pantallas grandes y se ajusten en pantallas más pequeñas
    return dbc.Row([dbc.Col(card, xl=4, lg=4, md=6, sm=12, xs=12) for card in tarjetas], className="g-3 justify-content-start")




if __name__ == "__main__":
    app.run_server(debug=True)
