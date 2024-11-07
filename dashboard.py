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
        user="root", 
        password="",  
        database="dashboard"  
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
        
        # Nueva fila para consultas variables con estilo similar a los gráficos fijos
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Consulta 4: Distribución de Docentes por Tipo de Contrato"),
                dbc.CardBody([
                    dcc.Graph(id="grafico-consulta-fija-4"),
                    html.Button("Ejecutar Consulta 4", id="btn-consulta-4", className="btn btn-custom"),
                ])
            ]), xs=12, sm=12, md=6, lg=4),

            # Consultas Variables con el mismo estilo
            dbc.Col(dbc.Card([
                dbc.CardHeader("Consultas Variables"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="filtro-consulta-variable",
                                options=[
                                    {"label": "Distribución de Docentes por Género y Nivel", "value": "distribucion_genero_nivel"},
                                    {"label": "Total de Docentes por Tipo de Contrato", "value": "total_por_tipo_contrato"},
                                    {"label": "Total de Docentes por Municipio", "value": "total_por_municipio"},
                                    {"label": "Total de Docentes por Año y Tipo de Dedicación", "value": "total_por_anio_tipo_dedicacion"},
                                    {"label": "Distribución de Docentes por Departamento", "value": "distribucion_por_departamento"},
                                ],
                                placeholder="Selecciona una consulta",
                            ),
                        ], xs=12, sm=12, md=5),
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
                        ], xs=12, sm=12, md=3),
                        dbc.Col([
                            dcc.Checklist(
                                id="checklist-anios",
                                options=[
                                    {"label": "2021", "value": 2021},
                                    {"label": "2022", "value": 2022},
                                    {"label": "2023", "value": 2023},
                                ],
                                value=[2021, 2022, 2023],
                                labelStyle={'display': 'inline-block'}
                            )
                        ], xs=12, sm=12, md=4),
                    ]),
                    # Gráfico y cifras relevantes
                    dcc.Graph(id="grafico-consulta-variable"),
                ])
            ]), xs=12, sm=12, md=6, lg=8),
        ], className="g-3"),

        html.Div(id="cifras-relevantes", className="my-4"),
    ], className="mt-3 mb-3", fluid=True)
])



@app.callback(
    Output("grafico-consulta-fija-1", "figure"),
    Output("grafico-consulta-fija-2", "figure"),
    Output("grafico-consulta-fija-3", "figure"),
    Output("grafico-consulta-fija-4", "figure"),
    [Input("btn-consulta-1", "n_clicks"),
     Input("btn-consulta-2", "n_clicks"),
     Input("btn-consulta-3", "n_clicks"),
     Input("btn-consulta-4", "n_clicks")]
)
def actualizar_graficos_fijos(n1, n2, n3, n4):
    # Consulta 1: Total de Docentes Femeninos con Doctorado en 2021, 2022, 2023
    anios = [2021, 2022, 2023]
    cantidad_femeninos_doctorado = []

    for anio in anios:
        total_femeninos_doctorado = df[(df['genero_docente'] == 'FEMENINO') & 
                                        (df['maximo_nivel_formacion_docente'] == 'DOCTORADO') & 
                                        (df['año'] == anio)]
        cantidad = total_femeninos_doctorado['numero_docentes'].sum()
        cantidad_femeninos_doctorado.append(cantidad)

    fig1 = px.line(x=anios, y=cantidad_femeninos_doctorado,
               title="Docentes Femeninos con Doctorado (2021-2023)",
               labels={'x': 'Año', 'y': 'Cantidad'},
               text=cantidad_femeninos_doctorado)
    fig1.update_traces(texttemplate='%{text}', textposition='top center')


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

    # Consulta 4: Distribución de Docentes por Tipo de Contrato (Gráfico de torta)
    if 'tipo_contrato_docente' in df.columns:
        distribucion_tipo_contrato = df.groupby('tipo_contrato_docente')['numero_docentes'].sum().reset_index()
        print(distribucion_tipo_contrato)  # Imprime los datos agrupados
        fig4 = px.pie(distribucion_tipo_contrato, values="numero_docentes", names="tipo_contrato_docente",
                      title="Docentes por Tipo de Contrato")
    else:
        fig4 = px.pie(pd.DataFrame(), title="Distribución de Docentes por Tipo de Contrato")

    return fig1, fig2, fig3, fig4


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
        datos_agrupados = datos_filtrados.groupby(['genero_docente', 'maximo_nivel_formacion_docente'])['numero_docentes'].sum().reset_index()
        fig = px.histogram(datos_agrupados, x="genero_docente", y="numero_docentes", color="maximo_nivel_formacion_docente",
                           title="Distribución de Docentes por Género y Nivel de Formación",
                           labels={'genero_docente': 'Género', 'maximo_nivel_formacion_docente': 'Nivel de Formación'})
        fig.update_layout(yaxis_title="Cantidad")

    elif seleccion == "total_por_tipo_contrato":
        datos_agrupados = datos_filtrados.groupby('tipo_contrato_docente')['numero_docentes'].sum().reset_index()
        fig = px.bar(datos_agrupados, x="tipo_contrato_docente", y="numero_docentes",
                     title="Docentes por Tipo de Contrato",
                     labels={'tipo_contrato_docente': 'Tipo de Contrato', 'numero_docentes': 'Cantidad de Docentes'})

    elif seleccion == "total_por_municipio":
        datos_agrupados = datos_filtrados.groupby('municipio_domicilio_ies')['numero_docentes'].sum().reset_index()
        fig = px.bar(datos_agrupados, x="municipio_domicilio_ies", y="numero_docentes",
                     title="Docentes por Municipio",
                     labels={'municipio_domicilio_ies': 'Municipio', 'numero_docentes': 'Cantidad de Docentes'})

    elif seleccion == "total_por_anio_tipo_dedicacion":
        datos_agrupados = datos_filtrados.groupby(['año', 'tiempo_dedicacion_docente'])['numero_docentes'].sum().reset_index()
        fig = px.bar(datos_agrupados, x="año", y="numero_docentes", color="tiempo_dedicacion_docente",
                      title="Total de Docentes por Año y Tipo de Dedicación",
                      labels={'año': 'Año', 'tiempo_dedicacion_docente': 'Tipo de Dedicación', 'numero_docentes': 'Cantidad de Docentes'})

    elif seleccion == "distribucion_por_departamento":
        datos_agrupados = datos_filtrados.groupby('departamento_domicilio_ies')['numero_docentes'].sum().reset_index()
        fig = px.bar(datos_agrupados, x="departamento_domicilio_ies", y="numero_docentes",
                     title="Distribución de Docentes por Departamento",
                     labels={'departamento_domicilio_ies': 'Departamento', 'numero_docentes': 'Cantidad de Docentes'})

    else:
        fig = {}  # Gráfica vacía en caso de que no haya coincidencias con la selección

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

    return dbc.Row([dbc.Col(card, xl=4, lg=4, md=6, sm=12, xs=12) for card in tarjetas], className="g-3 justify-content-start")




if __name__ == "__main__":
    app.run_server(debug=True)
